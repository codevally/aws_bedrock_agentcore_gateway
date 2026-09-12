resource "aws_bedrockagentcore_gateway" "weather" {
  name            = "agentcore-gateway"
  description     = "Weather AgentCore Gateway"
  role_arn        = aws_iam_role.gateway_role.arn
  authorizer_type = "NONE"
  protocol_type   = "MCP"
  depends_on = [
    aws_iam_role_policy_attachment.gateway_lambda_invoke
  ]
}

#Gateway Lambda Target
resource "aws_bedrockagentcore_gateway_target" "weather" {
  name                = "weather-tools"
  gateway_identifier  = aws_bedrockagentcore_gateway.weather.gateway_id
  description         = "Weather Lambda tools"

  # Gateway assumes its service role when invoking Lambda.
  credential_provider_configuration {
    gateway_iam_role {}
  }

  target_configuration {
    mcp {
      lambda {
        lambda_arn = aws_lambda_function.weather.arn

        # ----------------------------------------------------
        # Tool 1: Current weather
        # ----------------------------------------------------

        tool_schema {
          inline_payload {
            name        = "get_current_weather"
            description = "Get the current weather conditions for a city."

            input_schema {
              type = "object"

              property {
                name        = "city"
                type        = "string"
                description = "City name, for example Melbourne."
                required    = true
              }
            }
          }

          # --------------------------------------------------
          # Tool 2: Historical weather
          # --------------------------------------------------

          inline_payload {
            name        = "get_historical_weather"
            description = "Get historical weather data for a city over a specified date range."

            input_schema {
              type = "object"

              property {
                name        = "city"
                type        = "string"
                description = "City name, for example Melbourne."
                required    = true
              }

              property {
                name        = "start_date"
                type        = "string"
                description = "Start date in YYYY-MM-DD format."
                required    = true
              }

              property {
                name        = "end_date"
                type        = "string"
                description = "End date in YYYY-MM-DD format."
                required    = true
              }
            }
          }
        }
      }
    }
  }

  depends_on = [
    aws_bedrockagentcore_gateway.weather,
    aws_iam_role_policy_attachment.gateway_lambda_invoke
  ]
}