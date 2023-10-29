# resource "aws_ssm_parameter" "linesdk_channel_access_token" {
#   name  = "/linesdk/channel_access_token"
#   type  = "SecureString"
#   value = var.linesdk_channel_access_token
# }

# resource "aws_ssm_parameter" "linesdk_channel_secret" {
#   name  = "/linesdk/channel_secret"
#   type  = "SecureString"
#   value = var.linesdk_channel_secret
# }

# resource "aws_ssm_parameter" "hotpepper_keyid" {
#   name  = "/hotpepper/keyid"
#   type  = "SecureString"
#   value = var.hotpepper_keyid
# }

# resource "aws_iam_policy" "ssm_access" {
#   name        = "SSMAccess"
#   description = "My policy that grants access to SSM parameters"

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Action = [
#           "ssm:GetParameter",
#           "ssm:GetParameters",
#           "ssm:GetParametersByPath"
#         ],
#         Resource = "*",
#         Effect   = "Allow"
#       }
#     ]
#   })
# }