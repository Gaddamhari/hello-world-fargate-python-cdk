from typing import Optional
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
)

class HelloWorldFargateStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC (2 AZs)
        vpc = ec2.Vpc(self, "Vpc", max_azs=2)

        # ECR repository for the app; CI will push :latest
        repo = ecr.Repository(
            self, "Repo",
            repository_name="hello-world-go",
            image_scan_on_push=True
        )

        # ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Task execution role (for pulling from ECR, CloudWatch logs, etc.)
        exec_role = iam.Role(
            self, "TaskExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )

        # Task definition (Fargate)
        task_def = ecs.FargateTaskDefinition(
            self, "TaskDef",
            cpu=256,
            memory_limit_mib=512,
            execution_role=exec_role,
        )

        container = task_def.add_container(
            "App",
            image=ecs.ContainerImage.from_ecr_repository(repo, "latest"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="hello-world"),
        )
        container.add_port_mappings(
            ecs.PortMapping(container_port=8080, protocol=ecs.Protocol.TCP)
        )

        # Public Application Load Balancer
        lb = elbv2.ApplicationLoadBalancer(
            self, "ALB", vpc=vpc, internet_facing=True
        )
        listener = lb.add_listener("HttpListener", port=80, open=True)

        # Fargate service in public subnets
        service = ecs.FargateService(
            self, "Service",
            cluster=cluster,
            task_definition=task_def,
            desired_count=1,
            assign_public_ip=True,  # Simplifies demo; for prod, use private + NAT/ALB
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # Target group & health check
        tg = listener.add_targets(
            "ECS",
            port=80,
            targets=[service],
            health_check=elbv2.HealthCheck(
                path="/healthz",
                interval=cdk.Duration.seconds(30),
                healthy_http_codes="200",
            ),
        )

        # Outputs for CI and browse
        cdk.CfnOutput(self, "EcrRepoUri", value=repo.repository_uri)
        cdk.CfnOutput(self, "ClusterName", value=cluster.cluster_name)
        cdk.CfnOutput(self, "ServiceName", value=service.service_name)
        cdk.CfnOutput(self, "LoadBalancerDNS", value=lb.load_balancer_dns_name)
