
resource "aws_instance" "example2" {
  ami           = "ami-0c55b159cbfafe1f0"  # Replace with your AMI ID
  instance_type = "t2.micro"  # Replace with your desired instance type
  key_name      = "your-key-pair"  # Replace with your key pair name

  # Reserved capacity configuration
  capacity_reservation_specification {
    capacity_reservation_preference = "open"  # Options: "open", "none"
    #instance_count                   = 1       # Number of instances to reserve
  }
}
