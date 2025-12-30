"""
Utility functions for Lambda handlers
"""
import json
from typing import Any, Optional, Dict


def create_response(
    status_code: int,
    data: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized Lambda response
    
    Args:
        status_code: HTTP status code
        data: Response data (dict or list)
        message: Success/info message
        error: Error message
    
    Returns:
        Dictionary with statusCode and JSON body
        
    Examples:
        # Success response with data
        create_response(201, data={"taskId": "123", "title": "Task"})
        
        # Validation error
        create_response(400, message="Validation error", error="Invalid status")
        
        # Not found
        create_response(404, message="Task not found")
        
        # Server error
        create_response(500, error=str(exception))
    """
    body = {}
    
    # Add message if provided
    if message:
        body["message"] = message
    
    # Add data if provided
    if data:
        body["data"] = data
    
    # Add error if provided
    if error:
        body["error"] = error
    
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }
