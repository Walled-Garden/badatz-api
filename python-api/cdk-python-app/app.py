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
    # aws_apigateway,
)
import aws_cdk as cdk


class ApiCorsLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # badatz_lambda = _lambda.Function(
        #     self,
        #     "BadatzApiLambda",
        #     handler="lambda-handler.handler",
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     code=_lambda.Code.from_asset("../src/lambda"),
        # )
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
        _apigw.LambdaRestApi(self, "badatz_api_lambda_rest", handler=badatz_lambda)

        # base_api = _apigw.RestApi(
        #     self,
        #     "BadatzApiGatewayWithCors",
        #     rest_api_name="BadatzApiGatewayWithCors",
        # )
        #
        # example_entity = base_api.root.add_resource(
        #     "example",
        #     default_cors_preflight_options=_apigw.CorsOptions(
        #         allow_methods=["GET", "OPTIONS", "POST"],
        #         allow_origins=_apigw.Cors.ALL_ORIGINS,
        #     ),
        # )
        # example_entity_lambda_integration = _apigw.LambdaIntegration(
        #     badatz_lambda,
        #     proxy=False,
        #     integration_responses=[
        #         _apigw.IntegrationResponse(
        #             status_code="200",
        #             response_parameters={
        #                 "method.response.header.Access-Control-Allow-Origin": "'*'"
        #             },
        #         )
        #     ],
        # )
        # example_entity.add_method(
        #     "GET",
        #     example_entity_lambda_integration,
        #     method_responses=[
        #         _apigw.MethodResponse(
        #             status_code="200",
        #             response_parameters={
        #                 "method.response.header.Access-Control-Allow-Origin": True
        #             },
        #         )
        #     ],
        # )


app = App()
ApiCorsLambdaStack(app, "BadatzApiCorsLambdaStack")
app.synth()
