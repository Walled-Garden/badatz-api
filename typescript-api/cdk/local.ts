import * as cdk from "aws-cdk-lib";
import { App } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { BadatzStack } from "./app";
class TestBadatzStack extends BadatzStack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DO NOT USE IN PRODUCTION:
    // adding this so testing locally with `sam local start-api` will work.
    new apigateway.LambdaRestApi(this, "testAPI", {
      handler: this.badatzLambda,
    });
  }
}

const app = new App();
new TestBadatzStack(app, "local", {
  env: { account: "590781477698", region: "us-east-1" },
});
app.synth();
