from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigateway,   
    # aws_sqs as sqs,
)
from aws_cdk.aws_lambda import IFunction, LayerVersion
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
        #          LAMBDA LAYERS SETUP
        # =======================================
        common_layer = LayerVersion(
            self,
            "CommonLayer",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "layers", "common")
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
            description="Common layer with models and utilities"
        )

        # Layer de Pydantic
        pydantic_layer = LayerVersion(
            self,
            "PydanticLayer",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "layers", "pydantic_layer")
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
            description="Pydantic dependencies layer"
        )


        # =======================================
        #          LAMBDA FUNCTIONS
        # =======================================

        # Create Task
        create_task_lambda = _lambda.Function(
            self,
            "CreateTaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "create_task")
            ),
            layers=[common_layer, pydantic_layer],
            environment={
                "TASKS_TABLE_NAME": self.tasks_table.table_name
            }
        )
        self.tasks_table.grant_write_data(create_task_lambda)

        # Get Task
        get_task_lambda = _lambda.Function(
            self,
            "GetTaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "get_task")
            ),
            layers=[common_layer],
            environment={
                "TASKS_TABLE_NAME": self.tasks_table.table_name
            }
        )
        self.tasks_table.grant_read_data(get_task_lambda)

        # Update Task
        update_task_lambda = _lambda.Function(
            self,
            "UpdateTaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "update_task")
            ),
            layers=[common_layer, pydantic_layer],
            environment={
                "TASKS_TABLE_NAME": self.tasks_table.table_name
            }
        )
        self.tasks_table.grant_read_write_data(update_task_lambda)

        # Delete Task
        delete_task_lambda = _lambda.Function(
            self,
            "DeleteTaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(
                os.path.join("lambdas", "delete_task")
            ),
            layers=[common_layer, pydantic_layer],
            environment={
                "TASKS_TABLE_NAME": self.tasks_table.table_name
            }
        )
        self.tasks_table.grant_write_data(delete_task_lambda)


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

        # Create Task
        tasks_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(
                cast(IFunction, create_task_lambda))
        )

        # Get Task
        task_id_resource = tasks_resource.add_resource("{taskId}")
        task_id_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                cast(IFunction, get_task_lambda))
        )

        # Update Task 
        task_id_resource.add_method(
            "PUT",
            apigateway.LambdaIntegration(
                cast(IFunction, update_task_lambda))
        )

        task_id_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(
                cast(IFunction, delete_task_lambda)
            )
        )