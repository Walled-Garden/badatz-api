# #!/usr/bin/env python3
# import os
#
# import aws_cdk as cdk
#
# from cdk_app.cdk_app_stack import CdkAppStack
#
#
# app = cdk.App()
# CdkAppStack(app, "CdkAppStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.
#
#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.
#
#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#
#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */
#
#     #env=cdk.Environment(account='123456789012', region='us-east-1'),
#
#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )
#
# app.synth()

from constructs import Construct
from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_ec2 as _ec2,
    aws_iam as iam,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_certificatemanager as acm,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as elb_targets,
)
import aws_cdk as cdk

BADATZ_VPC_ID = "vpc-000442496728ac699"
ALLOW_RDS_SG_ID = "sg-0d9de38b677cdce5b"
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

        # # # The approach below is not working, because Private API Gateway does not support private dns
        # create a new API-GW VPCE
        # apigw_vpce = _ec2.InterfaceVpcEndpoint(
        #     self,
        #     "apigw_vpce",
        #     vpc=badatz_vpc,
        #     service=_ec2.InterfaceVpcEndpointAwsService.APIGATEWAY,
        #     private_dns_enabled=True,
        #     subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED),
        #     security_groups=[
        #         _ec2.SecurityGroup.from_security_group_id(
        #             self,
        #             "apigw_vpce_sg",
        #             # reference the existing security group that allows access to the RDS
        #             security_group_id=ALLOW_RDS_SG_ID,
        #         )
        #     ],
        # )

        # create a new API Gateway, with the Lambda function as the backend
        # the API Gateway would proxy all requests to the Lambda function
        # badatz_api = _apigw.LambdaRestApi(
        #     self,
        #     "badatz_api_lambda_rest",
        #     handler=badatz_lambda,
        #     integration_options=_apigw.LambdaIntegrationOptions(
        #         timeout=cdk.Duration.seconds(29)
        #     ),
        #     endpoint_configuration=_apigw.EndpointConfiguration(
        #         types=[_apigw.EndpointType.PRIVATE], vpc_endpoints=[apigw_vpce]
        #     ),
        #     # explicitly deny all requests that are not coming from the VPC endpoint
        #     # taken from here:
        #     # https://docs.aws.amazon.com/apigateway/latest/developerguide/private-api-tutorial.html#private-api-tutorial-attach-resource-policy
        #     policy=iam.PolicyDocument.from_json(
        #         {
        #             "Version": "2012-10-17",
        #             "Statement": [
        #                 {
        #                     "Effect": "Deny",
        #                     "Principal": "*",
        #                     "Action": "execute-api:Invoke",
        #                     "Resource": "execute-api:/*",
        #                     "Condition": {
        #                         "StringNotEquals": {
        #                             "aws:sourceVpce": apigw_vpce.vpc_endpoint_id
        #                         }
        #                     },
        #                 },
        #                 {
        #                     "Effect": "Allow",
        #                     "Principal": "*",
        #                     "Action": "execute-api:Invoke",
        #                     "Resource": "execute-api:/*",
        #                 },
        #             ],
        #         }
        #     ),
        #     domain_name=_apigw.DomainNameOptions(
        #         domain_name="rp-api.insightxc.com",
        #         certificate=acm.Certificate.from_certificate_arn(
        #             self,
        #             "badatz-api-insightxc_cert",
        #             certificate_arn=INSIGHTXC_CRT_ARN,
        #         ),
        #     ),
        #     # # old: explicit allow
        #     # policy=iam.PolicyDocument(
        #     #     statements=[
        #     #         iam.PolicyStatement(
        #     #             actions=["execute-api:Invoke"],
        #     #             resources=["execute-api:/*/*/*"],
        #     #             principals=[iam.AnyPrincipal()],
        #     #             conditions={
        #     #                 "StringEquals": {
        #     #                     "aws:sourceVpce": apigw_vpce.vpc_endpoint_id,
        #     #                 }
        #     #             },
        #     #         )
        #     #     ]
        #     # ),
        # )

        # route53.ARecord(
        #     self,
        #     "rp-api.insightxc.com-to-badatz_api",
        #     zone=insightxc_hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.ApiGateway(badatz_api)
        #     ),
        # )

        # public_api = _apigw.LambdaRestApi(
        #     self,
        #     "public_api",
        #     handler=badatz_lambda,
        #     domain_name=_apigw.DomainNameOptions(
        #         domain_name="public-api.insightxc.com",
        #         certificate=acm.Certificate.from_certificate_arn(
        #             self,
        #             "public-api-insightxc_cert",
        #             certificate_arn=INSIGHTXC_CRT_ARN,
        #         ),
        #     ),
        # )

        # route53.ARecord(
        #     self,
        #     "public-api.insightxc.com-to-public_api",
        #     zone=insightxc_hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.ApiGateway(public_api)
        #     ),
        #     record_name="public-api",
        # )

        # route53.ARecord(
        #     self,
        #     "insightxc_api_dns",
        #     zone=insightxc_hosted_zone,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.ApiGatewayDomain(badatz_api.domain_name)
        #     ),
        # )

        # badatz_api.add_resource_permission(
        #     principal=apigateway.ArnPrincipal("arn:aws:iam::123456789012:role/MyRole"),
        #     resource_arn=api.arn_for_execute_api(),
        #     actions=["execute-api:Invoke"],
        # )

        # nlb = elbv2.NetworkLoadBalancer(self, "NLB", vpc=vpc)
        # link = _apigw.VpcLink(self, "link", targets=[nlb])
        #
        # integration = _apigw.Integration(
        #     type=_apigw.IntegrationType.HTTP_PROXY,
        #     integration_http_method="ANY",
        #     options=_apigw.IntegrationOptions(
        #         connection_type=_apigw.ConnectionType.VPC_LINK, vpc_link=link
        #     ),
        # )


app = App()
ApiCorsLambdaStack(
    app,
    "badatz-api-lambda-stack",
    env={"account": "590781477698", "region": "us-east-1"},
)
app.synth()
