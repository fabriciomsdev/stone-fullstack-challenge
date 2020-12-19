from aws_cdk import (core, aws_ecs as ecs, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam)
from aws_cdk import core


class CdkAwsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the ECR Repository
        ecr_repository = ecr.Repository(self,
                                        "ecs-devops-stone-repository",
                                        repository_name="ecs-devops-stone-repository")

        # Create the ECS Cluster (and VPC)
        vpc = ec2.Vpc(self,
                      "ecs-devops-stone-vpc",
                      max_azs=3)
        cluster = ecs.Cluster(self,
                              "ecs-devops-stone-cluster",
                              cluster_name="ecs-devops-stone-cluster",
                              vpc=vpc)

        # Create the ECS Task Definition with placeholder container (and named Task Execution IAM Role)
        execution_role = iam.Role(self,
                                  "ecs-devops-stone-execution-role",
                                  assumed_by=iam.ServicePrincipal(
                                      "ecs-tasks.amazonaws.com"),
                                  role_name="ecs-devops-stone-execution-role")
        execution_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
        ))
        task_definition = ecs.FargateTaskDefinition(self,
                                                    "ecs-devops-stone-task-definition",
                                                    execution_role=execution_role,
                                                    family="ecs-devops-stone-task-definition")
        container = task_definition.add_container(
            "ecs-devops-stone",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )

        # Create the ECS Service
        service = ecs.FargateService(self,
                                     "ecs-devops-stone-service",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     service_name="ecs-devops-stone-service")

