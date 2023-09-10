resource "aws_dynamodb_table" "posession" {
  name           = "VehiclePosession"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "UserId"
  range_key      = "VehicleId"

  attribute {
    name = "UserId"
    type = "S"
  }
  attribute {
    name = "VehicleId"
    type = "S"
  }

  tags = {
    Environment = "dev"
  }

}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "post_user_role" {
  name               = "post_user_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_policy_attachment" {
  role       = aws_iam_role.post_user_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_full_access" {
  role       = aws_iam_role.post_user_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

data "archive_file" "lambda_user_post_package" {
  type        = "zip"
  source_dir  = "${path.root}/../functions/user_post"
  output_path = "lambda_user_post.zip"
}

resource "aws_lambda_function" "lambda_user_post" {
  function_name = "user-post"
  filename      = "lambda_user_post.zip"
  source_code_hash = filebase64sha256(data.archive_file.lambda_user_post_package.output_path)
  role          = aws_iam_role.post_user_role.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  layers        = [var.powertools_layer_arn]
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.posession.name,
      LOG_LEVEL  = "INFO"
    }
  }
}
