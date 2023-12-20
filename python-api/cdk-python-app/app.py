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
)
import aws_cdk as cdk

BADATZ_VPC_ID = "vpc-000442496728ac699"
# BADATZ_APIGW_VPCE_ID = "vpce-0f0fed9484d72e5db"
ALLOW_RDS_SG_ID = "sg-0d9de38b677cdce5b"


class ApiCorsLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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
        )

        # # Reference an existing VPCE by providing its ID
        # apigw_vpce = _ec2.InterfaceVpcEndpoint.from_interface_vpc_endpoint_attributes(
        #     self, "apigw_vpce", vpc_endpoint_id=BADATZ_APIGW_VPCE_ID, port=443
        # )

        # # create a new VPCE
        apigw_vpce = _ec2.InterfaceVpcEndpoint(
            self,
            "apigw_vpce",
            vpc=_ec2.Vpc.from_lookup(self, "badatz_vpc", vpc_id=BADATZ_VPC_ID),
            service=_ec2.InterfaceVpcEndpointAwsService.APIGATEWAY,
            private_dns_enabled=True,
            subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED),
            security_groups=[
                _ec2.SecurityGroup.from_security_group_id(
                    self, "apigw_vpce_sg", security_group_id=ALLOW_RDS_SG_ID
                )
            ],
        )

        apigw = _apigw.LambdaRestApi(
            self,
            "badatz_api_lambda_rest",
            handler=badatz_lambda,
            integration_options=_apigw.LambdaIntegrationOptions(
                timeout=cdk.Duration.seconds(29)
            ),
            endpoint_configuration=_apigw.EndpointConfiguration(
                types=[_apigw.EndpointType.PRIVATE], vpc_endpoints=[apigw_vpce]
            ),
            policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["execute-api:Invoke"],
                        resources=["execute-api:/*/*/*"],
                        principals=[iam.AnyPrincipal()],
                        conditions={
                            "StringEquals": {
                                "aws:sourceVpce": apigw_vpce.vpc_endpoint_id,
                            }
                        },
                    )
                ]
            ),
        )
        # apigw.add_resource_permission(
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
