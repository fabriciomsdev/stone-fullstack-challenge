#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws.cdk_aws_stack import CdkAwsStack


app = core.App()
CdkAwsStack(app, "cdk-aws")

app.synth()
