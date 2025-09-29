#!/usr/bin/env python3
import os
import aws_cdk as cdk
from hello_world_stack import HelloWorldFargateStack

app = cdk.App()

HelloWorldFargateStack(
    app,
    "HelloWorldFargateStack",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
    ),
)

app.synth()
