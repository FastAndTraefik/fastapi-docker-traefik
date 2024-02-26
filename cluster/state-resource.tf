provider "aws" {
  alias = "default"
  region = "us-east-1"
}

resource "aws_s3_bucket" "s_bucket" {
    bucket = "stateq-bucket"
  
}

resource "aws_dynamodb_table" "terraform_lock" {
    name =  "state-lock"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "LockID"

attribute {
    name = "LockID"
    type = "S"
  }
}
