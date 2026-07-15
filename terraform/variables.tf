variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Deployment environment name, passed to the Lambda as ENVIRONMENT"
  type        = string
  default     = "dev"
}

variable "function_name" {
  description = "Name of the dummy Lambda function"
  type        = string
  default     = "vpc-assignment-api-hello-world"
}
