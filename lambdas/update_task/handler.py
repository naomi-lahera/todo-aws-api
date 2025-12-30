import os
import json
import boto3
from utils import create_response
from pydantic import ValidationError
from models import UpdateTaskRequest
import logging
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    """
    Update task
    """
    try:
        task_id = event.get("pathParameters", {}).get("taskId")
        if not task_id:
            return create_response(400, {"message": "taskId is required"})

        body = json.loads(event.get("body", "{}"))
        task_request = UpdateTaskRequest(**body)

        update_expression = []
        expression_values = {}
        expression_names = {}

        for field, value in task_request.model_dump(exclude_none=True).items():
            update_expression.append(f"#{field}=:{field}")
            expression_values[f":{field}"] = value
            expression_names[f"#{field}"] = field

        if not update_expression:
            return create_response(400, {"message": "No fields to update"})

        update_params = {
            "Key": {"taskId": task_id},
            "UpdateExpression": "SET " + ", ".join(update_expression),
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW"
        }
        
        if expression_names:
            update_params["ExpressionAttributeNames"] = expression_names

        response = table.update_item(**update_params)

        return create_response(200, {
            "message": "Task updated successfully",
            "task": response["Attributes"]
        })

    except ValidationError as e:
        return create_response(400, {"errors": e.errors()})
    
    except ClientError as err:
        logger.error(
            "Couldn't update task %s. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return create_response(400, {"errors": err.response["Error"]["Message"]})

    except Exception as e:
        return create_response(500, {"message": str(e)})
