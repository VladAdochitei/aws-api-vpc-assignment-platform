output "api_endpoint" {
  description = "The API Gateway endpoint URL"
  value       = aws_api_gateway_stage.this.invoke_url
}

output "api_id" {
  description = "The REST API ID"
  value       = aws_api_gateway_rest_api.this.id
}

output "api_execution_arn" {
  description = "The execution ARN of the API"
  value       = aws_api_gateway_rest_api.this.execution_arn
}
