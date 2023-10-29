variable "aws_region" {
  description = "AWS region to deploy the infrastructure"
  default     = "ap-northeast-1"
}

variable "powertools_layer_arn" {
  description = "ARN of the Powertools layer"
  default     = "arn:aws:lambda:ap-northeast-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:46"
}

