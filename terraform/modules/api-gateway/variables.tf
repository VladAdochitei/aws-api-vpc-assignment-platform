variable "api_name" {
  description = "Name of the REST API"
  type        = string
}

variable "stage_name" {
  description = "API Gateway stage name (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "routes" {
  description = "Map of routes. path is a list of segments; {param} segments become path params."
  type = map(object({
    path                  = list(string)
    http_method           = string
    lambda_function_arn   = string
    lambda_function_name  = string
  }))
}