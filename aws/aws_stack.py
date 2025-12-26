from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigateway,   
    # aws_sqs as sqs,
)
from aws_cdk.aws_lambda import IFunction
import os
from typing import cast
from constructs import Construct

class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =======================================
        #          DATABASE SETUP
        # =======================================
        self.tasks_table = dynamodb.Table(
            self,
            "TasksTable",
            table_name="TasksTable",
            partition_key=dynamodb.Attribute(
                name="taskId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
            )

        # =======================================
        #          LAMBDA FUNCTIONS
        # =======================================
        create_task_lambda = _lambda.Function(
            self,
            "CreateTaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "create_task")
            ),
            environment={
                "TASKS_TABLE_NAME": self.tasks_table.table_name
            }
        )

        self.tasks_table.grant_write_data(create_task_lambda)

        # =======================================
        #          API GATEWAY SETUP
        # =======================================
        api = apigateway.RestApi(
            self,
            "TasksApi",
            rest_api_name="Tasks Service",
            description="Servesless Tasks Service."
        )

        tasks_resource = api.root.add_resource("tasks")
        tasks_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(
                cast(IFunction, create_task_lambda)) #TODO: Check cast
        )


        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
