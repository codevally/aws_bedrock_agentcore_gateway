#Trust Policy for AgentCore Service
data "aws_iam_policy_document" "agentcore_assume_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["bedrock-agentcore.amazonaws.com"]
      type = "Service"
    }
    condition {
      test     = "StringEquals"
      values = [data.aws_caller_identity.current.id]
      variable = "aws:SourceAccount"
    }
  }
}

#Trust Policy for Lambda
data "aws_iam_policy_document" "lambda_assume_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
    condition {
      test     = "StringEquals"
      values = [data.aws_caller_identity.current.id]
      variable = "aws:SourceAccount"
    }
  }
}

# AgentCore Gateway Role
resource "aws_iam_role" "gateway_role" {
  name               = "${var.project_name}-gateway-execution-role"
  assume_role_policy = data.aws_iam_policy_document.agentcore_assume_policy.json
}

# Lambda Role
resource "aws_iam_role" "lambda_role" {
  name               = "${var.project_name}-lambda-execution-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_policy.json
}

# Basic CloudWatch logging for Lambda
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role        = aws_iam_role.lambda_role.name
  policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

#Gateway Lambda  Invoke role
data "aws_iam_policy_document" "gateway_lambda_invoke_policy" {
  statement {
    sid    = "InvokeWeatherLambda"
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = [
      aws_lambda_function.weather.arn
    ]
  }
}

resource "aws_iam_policy" "gateway_lambda_invoke" {
  name = "${var.project_name}-gateway-lambda-invoke"
  policy = data.aws_iam_policy_document.gateway_lambda_invoke_policy.json
}

resource "aws_iam_role_policy_attachment" "gateway_lambda_invoke" {
  role = aws_iam_role.gateway_role.name
  policy_arn = aws_iam_policy.gateway_lambda_invoke.arn
}