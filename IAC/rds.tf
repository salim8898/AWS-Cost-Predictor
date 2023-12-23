

resource "aws_db_instance" "example_rds" {
  allocated_storage    = 20  # Replace with your desired storage size in GB
  storage_type         = "gp2"  # Replace with your desired storage type
  engine               = "mysql"  # Replace with your desired database engine
  engine_version       = "5.7"  # Replace with your desired database engine version
  instance_class       = "db.t2.micro"  # Replace with your desired instance class
  #name                 = "myexampledb"  # Replace with your desired DB name
  username             = "admin"  # Replace with your desired username
  password             = "yourpassword"  # Replace with your desired password

  # Optional: Customize additional settings as needed
}
