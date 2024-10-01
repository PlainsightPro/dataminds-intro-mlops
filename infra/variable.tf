variable "subscription_id" {
  description = "The Azure subscription ID."
  type        = string
}
variable "region" {
  description = "The Azure region."
  type        = string
  default     = "westeurope"
}
variable "prefix" {
  description = "The prefix to use for all resources."
  type        = string
  default     = "dataMinds"
}
variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "mlops"
}