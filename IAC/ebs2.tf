resource "aws_ebs_volume" "example2" {
  availability_zone = "us-east-2a"  # Specify the availability zone

  size              = 10  # Volume size in gibibytes (GiB)
  encrypted         = true  # Optionally, set to true for encryption

  # Additional optional configurations:
  # type              = "gp2"  # EBS volume type (e.g., "gp2", "io1")
  # kms_key_id        = aws_kms_key.example.arn  # Specify KMS key ID for encryption
  # snapshot_id       = aws_ebs_snapshot.example.id  # Create from a snapshot if required

  tags = {
    Name = "ExampleVolume"
    Environment = "Production"
  }
}
