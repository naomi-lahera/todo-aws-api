# Task Management Service - AWS Serverless App

A complete serverless application on AWS using AWS CDK with Python. Includes:
- **REST API** with API Gateway
- **Lambda functions** for task CRUD operations
- **DynamoDB** database
- **Lambda Layers** with shared dependencies
- **Automatic deployment**

## Setup Instructions

### Prerequisites

The following must be installed before proceeding:

- **Python 3.11+**
- **AWS CLI**
- **Node.js 14+**
- **AWS Account**: With configured credentials

### Step 1: Extract the Project

The project must be extracted from the .zip file. The extracted folder should be named `tasks-management-api`:

### Step 2: Configure AWS Credentials

AWS credentials must be configured locally:

```bash
aws configure
```

When prompted, the following information must be provided:
- **AWS Access Key ID**: Your access key
- **AWS Secret Access Key**: Your secret key
- **Default region**: Example: `us-east-1`
- **Default output format**: Example: `json`

### Step 3: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Project Dependencies

The project dependencies must be installed by running:

```bash
pip install -r requirements.txt
```

### Step 5: Install AWS CDK Globally (if not already installed)

```bash
npm install -g aws-cdk
```

### Step 6: Create Lambda Layer Dependencies

The Lambda layers must be created with specific dependencies built for the Lambda runtime environment. The following commands must be executed:

**Install Pydantic:**
```bash
pip install pydantic==2.9.2 -t lambdas/layers/dependencies/python --platform manylinux2014_x86_64 --only-binary=:all: --python-version 3.11 --implementation cp --upgrade
```

The following will be accomplished by these commands:
- Packages will be installed to `lambdas/layers/dependencies/python` directory

## How to Deploy the Solution

### Method 1: Deploy Using CDK Commands

**Step 1: Synthesize the CloudFormation Template**

```bash
cdk synth
```

The CloudFormation template must be generated without deploying.

**Step 2: Deploy the Stack**

```bash
cdk deploy
```

The following must occur when deploying:
1. A summary of resources to be created must be shown
2. Confirmation must be requested (type `y` to confirm)
3. The stack must be deployed to the AWS account
4. Stack outputs must be displayed including API endpoint URL

## Cleanup

All AWS resources created by the stack must be removed by running:

```bash
cdk destroy
```

**Warning**: This action is irreversible and the following will be deleted:
- API Gateway
- Lambda functions
- DynamoDB table
- Lambda layers
- IAM roles and policies

Confirmation must be provided by typing `y` when prompted.
