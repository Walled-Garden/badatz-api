import * as cdk from "aws-cdk-lib";
import { App, Stack } from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as route53 from "aws-cdk-lib/aws-route53";
import * as targets from "aws-cdk-lib/aws-route53-targets";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as elbTargets from "aws-cdk-lib/aws-elasticloadbalancingv2-targets";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { Construct } from "constructs";

const BADATZ_VPC_ID = "vpc-000442496728ac699";
const INSIGHTXC_HOSTED_ZONE_ID = "Z03545982I5FRH4AR48BO";
const INSIGHTXC_CRT_ARN =
  "arn:aws:acm:us-east-1:590781477698:certificate/2140f7f3-e699-43f6-9518-fad14c04f100";
const BADATZ_ALB_ARN =
  "arn:aws:elasticloadbalancing:us-east-1:590781477698:loadbalancer/app/badatz-internal-alb/1d3fb2c2a2df313e";

class ApiCorsLambdaStack extends Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Reference the existing Badatz VPC
    const badatzVpc = ec2.Vpc.fromLookup(this, "badatz_vpc", {
      vpcId: BADATZ_VPC_ID,
    });

    // Create a new Lambda function, within Badatz VPC
    // The Lambda function uses the flask app from the ../src directory as the handler
    const badatzLambda = new lambda.Function(this, "badatz_api_lambda", {
      handler: "src/handler.handler",
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset("../app", {
        // bundling: {
        //   image: lambda.Runtime.NODEJS_18_X.bundlingImage,
        //   command: [
        //     "bash",
        //     "-c",
        //     "yarn install -r requirements.txt -t /asset-output && cp -au . /asset-output",
        //   ],
        // },
      }),
      timeout: cdk.Duration.seconds(60),
      vpc: badatzVpc,
    });

    // just so testing locally with `sam local start-api` will work. DO NOT USE IN PRODUCTION
    new apigateway.LambdaRestApi(this, "testAPI", {
      handler: badatzLambda,
    });

    // use ALB instead of API Gateway to route to the lambda directly
    // https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html
    const badatzAlb = elbv2.ApplicationLoadBalancer.fromLookup(
      this,
      "BADATZ_ALB",
      {
        loadBalancerArn: BADATZ_ALB_ARN,
      },
    );
    const badatzListener = elbv2.ApplicationListener.fromLookup(
      this,
      "ALBListener",
      {
        loadBalancerArn: BADATZ_ALB_ARN,
        listenerProtocol: elbv2.ApplicationProtocol.HTTPS,
        listenerPort: 443,
      },
    );

    badatzListener.addTargetGroups("badatz-api", {
      targetGroups: [
        new elbv2.ApplicationTargetGroup(this, "badatz-api-tg", {
          targets: [new elbTargets.LambdaTarget(badatzLambda)],
          vpc: badatzVpc,
        }),
      ],
      conditions: [
        elbv2.ListenerCondition.hostHeaders(["rp.api.insightxc.com"]),
      ],
      priority: 90,
    });

    // add route53 record to the ALB
    const insightxcHostedZone = route53.HostedZone.fromHostedZoneAttributes(
      this,
      "insightxc_hosted_zone",
      {
        hostedZoneId: INSIGHTXC_HOSTED_ZONE_ID,
        zoneName: "insightxc.com",
      },
    );

    // new route53.ARecord(
    //     this,
    //     'rp.api.insightxc.com-to-badatz-alb',
    //     {
    //         zone: insightxc_hosted_zone,
    //         target: route53.RecordTarget.fromAlias(
    //             new route53_targets.LoadBalancerTarget(badatzAlb)
    //         ),
    //         recordName: 'rp.api.insightxc.com',
    //     }
    // );

    // now when user navigates to rp.api.insightxc.com,
    // the request will be routed to the ALB->Lambda->Flask app ../src/app.py !
  }
}

const app = new App();
new ApiCorsLambdaStack(app, "badatz-api-lambda-stack", {
  env: { account: "590781477698", region: "us-east-1" },
});
app.synth();
