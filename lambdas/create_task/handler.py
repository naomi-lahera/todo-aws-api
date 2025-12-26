import json
import os
import uuid
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TASKS_TABLE_NAME"])

VALID_STATUSES = {"pending", "in-progress", "completed"}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        title = body.get("title")
        description = body.get("description")
        status = body.get("status")

        if not title or not description or not status:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing required fields"})
            }

        if status not in VALID_STATUSES:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid status value"})
            }

        task_id = str(uuid.uuid4())

        item = {
            "taskId": task_id,
            "title": title,
            "description": description,
            "status": status
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
