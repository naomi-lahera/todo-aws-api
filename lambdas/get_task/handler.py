import os
import boto3
from botocore.exceptions import ClientError
import logging
from utils import create_response

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    """
    Get a task by taskId
    """
    try:
        task_id = event.get("pathParameters", {}).get("taskId")

        if not task_id or not task_id.strip():
            return create_response(
                400,
                message="Missing or invalid taskId in path parameters"
            )
        
        response = table.get_item(Key={"taskId": task_id})
        item = response.get("Item")

        if not item:
            return create_response(
                404,
                message=f"Task with taskId '{task_id}' not found"
            )
        
        return create_response(200, data=item)
    
    except ClientError as err:
        logger.error(
            "Couldn't get task %s. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return create_response(400, {"errors": err.response["Error"]["Message"]})
        
    except Exception as e:
        return create_response(
            500,
            error=str(e)
        )