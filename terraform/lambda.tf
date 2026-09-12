data "archive_file" "weather_lambda" {
  type        = "zip"
  source_file = "${path.module}/../lambda/weather.py"
  output_path = "${path.module}/weather_lambda.zip"
}

resource "aws_lambda_function" "weather" {
  function_name     = "${var.project_name}-lambda-tool"
  description       = "Weather tools for AgentCore Gateway"
  filename          = data.archive_file.weather_lambda.output_path
  source_code_hash  = data.archive_file.weather_lambda.output_base64sha256
  handler           = "weather.lambda_handler"
  runtime           = "python3.12"

  role              = aws_iam_role.lambda_role.arn

  timeout           = 30
  memory_size       = 256

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]
}