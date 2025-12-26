"""
Pydantic models for Task validation
"""
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class TaskStatus(str, Enum):
    """Valid task statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class CreateTaskRequest(BaseModel):
    """Validation model for creating a task"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=1, max_length=1000, description="Task description")
    status: TaskStatus = Field(..., description="Task status")

    class Config:
        use_enum_values = True

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v):
        """Validate that status is one of the valid values"""
        if isinstance(v, TaskStatus):
            return v
        
        valid_statuses = [status.value for status in TaskStatus]
        if v not in valid_statuses:
            raise ValueError(
                f"Invalid status '{v}'. Must be one of: {', '.join(valid_statuses)}"
            )
        return v


class TaskResponse(BaseModel):
    """Response model for a task"""
    taskId: str
    title: str
    description: str
    status: str
