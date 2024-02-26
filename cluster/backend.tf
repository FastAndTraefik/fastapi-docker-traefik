terraform {
  backend "s3" {
    bucket         = "stateq-bucket"
    key            = "fast-api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "state-lock"
  }
}
