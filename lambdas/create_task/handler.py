import json
import os
import uuid
import boto3
from pydantic import ValidationError
import logging
from botocore.exceptions import ClientError
from models import CreateTaskRequest
from utils import create_response

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    """
    Create a new task
    """
    try:
        body = json.loads(event.get("body", "{}"))
        
        try:
            task_request = CreateTaskRequest(**body)
        except ValidationError as e:
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            return create_response(
                400,
                message="Validation error",
                error="; ".join(error_messages)
            )

        task_id = str(uuid.uuid4())
        item = {
            "taskId": task_id,
            "title": task_request.title,
            "description": task_request.description,
            "status": task_request.status
        }

        table.put_item(Item=item)

        return create_response(201, data=item)

    except ValidationError as e:
        return create_response(400, {"errors": e.errors()})
    
    except ClientError as err:
        logger.error(
            "Couldn't create task %s. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        return create_response(400, {"errors": err.response["Error"]["Message"]})
    
    except Exception as e:
        return create_response(
            500,
            error=str(e)
        )

