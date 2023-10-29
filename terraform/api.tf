# resource "aws_api_gateway_rest_api" "api" {
#   name = "sister-gourmet-api"
# }

# resource "aws_api_gateway_resource" "callback_resource" {
#   rest_api_id = aws_api_gateway_rest_api.api.id
#   parent_id   = aws_api_gateway_rest_api.api.root_resource_id
#   path_part   = "callback"
# }

# resource "aws_api_gateway_method" "callback_post" {
#   rest_api_id   = aws_api_gateway_rest_api.api.id
#   resource_id   = aws_api_gateway_resource.callback_resource.id
#   http_method   = "POST"
#   authorization = "NONE"
# }

# resource "aws_api_gateway_integration" "callback_lambda" {
#   rest_api_id = aws_api_gateway_rest_api.api.id
#   resource_id = aws_api_gateway_resource.callback_resource.id
#   http_method = aws_api_gateway_method.callback_post.http_method

#   integration_http_method = "POST"
#   type                    = "AWS_PROXY"
#   uri                     = aws_lambda_function.lambda_function.invoke_arn
# }

# resource "aws_lambda_permission" "apigw" {
#   statement_id  = "AllowAPIGatewayInvoke"
#   action        = "lambda:InvokeFunction"
#   # function_name = module.lambda_function.this_lambda_function_name
#   function_name = aws_lambda_function.lambda_function.function_name
#   principal     = "apigateway.amazonaws.com"
# }

# resource "aws_api_gateway_deployment" "api_deployment" {
#   depends_on  = [aws_api_gateway_integration.callback_lambda]
#   rest_api_id = aws_api_gateway_rest_api.api.id
#   stage_name  = "prod"
# }
