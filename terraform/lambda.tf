# data "aws_iam_policy_document" "assume_role" {
#   statement {
#     effect = "Allow"
#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }
#     actions = ["sts:AssumeRole"]
#   }
# }

resource "aws_iam_role" "lambda_role" {
  name = "vehicle_rental_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_basic_exe_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# resource "aws_iam_role_policy_attachment" "attach_ssm_policy" {
#   role       = aws_iam_role.lambda_role.name
#   policy_arn = aws_iam_policy.ssm_access.arn
# }


# resource "aws_iam_role" "post_user_role" {
#   name               = "post_user_role"
#   assume_role_policy = data.aws_iam_policy_document.assume_role.json
# }

# resource "aws_iam_role_policy_attachment" "lambda_dynamodb_full_access" {
#   role       = aws_iam_role.post_user_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
# }

data "archive_file" "lambda_vehicles" {
  type        = "zip"
  source_dir  = "${path.root}/../src/vehicles"
  output_path = "lambda_vehicles.zip"
}

resource "aws_lambda_function" "vehicles" {
  function_name = "vehicles-handler"
  # filename      = "lambda_vehicles.zip"
  # source_code_hash = filebase64sha256("lambda_vehicles.zip")
  filename      = data.archive_file.lambda_vehicles.output_path
  source_code_hash = filebase64sha256(data.archive_file.lambda_package.output_path)
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  layers        = [var.powertools_layer_arn]
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.vehicle_record.name,
      LOG_LEVEL  = "DEBUG"
    }
  }
}
