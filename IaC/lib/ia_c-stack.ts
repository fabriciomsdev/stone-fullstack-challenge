import * as cdk from '@aws-cdk/core';
import * as rds from '@aws-cdk/aws-rds';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as s3assets from '@aws-cdk/aws-s3-assets';
import * as alasticb from '@aws-cdk/aws-elasticbeanstalk';

const app_prefix = "StoneLogistic";

export class IaCStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const elbZipArchive = new s3assets.Asset(this, 'MyElbAppZip', {
      path: `${__dirname}/../app.zip`,
    });

    const vpc = new ec2.Vpc(this, `${app_prefix}VPC`, {
      cidr: "10.0.0.0/16",
    })

    // Iterate the private subnets
    const selection = vpc.selectSubnets({
      subnetType: ec2.SubnetType.PRIVATE
    });

    const cluster = new rds.DatabaseInstance(this, `${app_prefix}Database`, {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0_20
      }),
      vpc: vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE,
      },
      credentials: rds.Credentials.fromGeneratedSecret(`${app_prefix}DatabaseCredentials`),
    });


    const elasticbean_app = 
  }

}
