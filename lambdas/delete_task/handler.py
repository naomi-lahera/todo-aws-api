import os
import boto3
from utils import create_response
from botocore.exceptions import ClientError
import logging

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    try:
        task_id = event.get("pathParameters", {}).get("taskId")
        if not task_id:
            return create_response(400, {"message": "taskId is required"})
        
        table.delete_item(Key={"taskId": task_id})
        
        return create_response(204, {"message": "No content"})

    except ClientError as err:
        logger.error(
            "Couldn't delete task. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return create_response(400, {"errors": err.response["Error"]["Message"]})
    
    except Exception as e:
        return create_response(
            500,
            error=str(e)
        )
    
    