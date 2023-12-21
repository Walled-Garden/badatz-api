import aws_cdk as cdk
from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,
    aws_ec2 as _ec2,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elb_targets,
)
from constructs import Construct

BADATZ_VPC_ID = "vpc-000442496728ac699"
INSIGHTXC_HOSTED_ZONE_ID = "Z03545982I5FRH4AR48BO"
INSIGHTXC_CRT_ARN = "arn:aws:acm:us-east-1:590781477698:certificate/2140f7f3-e699-43f6-9518-fad14c04f100"
BADATZ_ALB_ARN = "arn:aws:elasticloadbalancing:us-east-1:590781477698:loadbalancer/app/badatz-internal-alb/1d3fb2c2a2df313e"


class ApiCorsLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Reference the existing Badatz VPC
        badatz_vpc = _ec2.Vpc.from_lookup(self, "badatz_vpc", vpc_id=BADATZ_VPC_ID)

        # Create a new Lambda function, within Badatz VPC
        # The Lambda function uses the flask app from the ../src directory as the handler
        badatz_lambda = _lambda.Function(
            self,
            "badatz_api_lambda",
            handler="lambda_handler.handler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset(
                "../src",
                bundling=cdk.BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_10.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            vpc=badatz_vpc,
        )

        # use ALB instead of API Gateway to route to the lambda directly
        # https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html
        badatz_alb = elbv2.ApplicationLoadBalancer.from_lookup(
            self, "BADATZ_ALB", load_balancer_arn=BADATZ_ALB_ARN
        )
        badatz_listener = elbv2.ApplicationListener.from_lookup(
            self,
            "ALBListener",
            load_balancer_arn=BADATZ_ALB_ARN,
            listener_protocol=elbv2.ApplicationProtocol.HTTPS,
            listener_port=443,
        )

        badatz_listener.add_target_groups(
            "badatz-api",
            target_groups=[
                elbv2.ApplicationTargetGroup(
                    self,
                    "badatz-api-tg",
                    targets=[elb_targets.LambdaTarget(badatz_lambda)],
                    vpc=badatz_vpc,
                )
            ],
            conditions=[elbv2.ListenerCondition.host_headers(["rp.api.insightxc.com"])],
            priority=90,
        )

        # add route53 record to the ALB
        insightxc_hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "insightxc_hosted_zone",
            hosted_zone_id=INSIGHTXC_HOSTED_ZONE_ID,
            zone_name="insightxc.com",
        )

        route53.ARecord(
            self,
            "rp.api.insightxc.com-to-badatz_alb",
            zone=insightxc_hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.LoadBalancerTarget(badatz_alb)
            ),
            record_name="rp.api.insightxc.com",
        )
        # now when user navigates to rp.api.insightxc.com,
        # the request will be routed to the ALB->Lambda->Flask app ../src/app.py !


app = App()
ApiCorsLambdaStack(
    app,
    "badatz-api-lambda-stack",
    env={"account": "590781477698", "region": "us-east-1"},
)
app.synth()
