provider "aws" {
  region = "us-west-2"  # Replace with your desired region
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with your desired AMI ID
  instance_type = "m5.large"  # Replace with your desired instance type
  key_name      = "your-key-pair"  # Replace with your key pair name

  # Optional: Add additional configuration like security groups, subnet, etc.
}
