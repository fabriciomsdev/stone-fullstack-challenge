import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as IaC from '../lib/ia_c-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new IaC.IaCStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
