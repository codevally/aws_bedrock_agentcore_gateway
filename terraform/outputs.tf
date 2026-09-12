output "gateway_id" {
  description = "AgentCore Gateway ID."
  value       = aws_bedrockagentcore_gateway.weather.gateway_id
}

output "gateway_arn" {
  description = "AgentCore Gateway ARN."
  value       = aws_bedrockagentcore_gateway.weather.gateway_arn
}

output "gateway_url" {
  description = "AgentCore Gateway MCP endpoint."
  value       = aws_bedrockagentcore_gateway.weather.gateway_url
}

output "lambda_function_name" {
  description = "Weather Lambda function name."
  value       = aws_lambda_function.weather.function_name
}

output "lambda_function_arn" {
  description = "Weather Lambda function ARN."
  value       = aws_lambda_function.weather.arn
}

output "gateway_role_arn" {
  description = "AgentCore Gateway IAM role ARN."
  value       = aws_iam_role.gateway_role.arn
}