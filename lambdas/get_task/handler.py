import json
import os
import boto3
from utils import create_response

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

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
    
    except Exception as e:
        return create_response(
            500,
            error=str(e)
        )