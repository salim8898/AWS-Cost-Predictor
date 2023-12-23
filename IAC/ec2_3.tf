resource "aws_launch_configuration" "example3" {
  name                        = "example-config"
  image_id                    = "ami-12345678"
  instance_type               = "m7g.large"
  #security_groups             = [aws_security_group.example.id]
  user_data                   = <<-EOF
                                  #!/bin/bash
                                  echo "Hello, World!" > index.html
                                  nohup python -m SimpleHTTPServer 80 &
                                EOF
}

resource "aws_autoscaling_group" "example3" {
  desired_capacity     = 2
  max_size             = 3
  min_size             = 1
  health_check_type    = "EC2"
  launch_configuration = aws_launch_configuration.example3.id

  tag {
    key                 = "Name"
    value               = "example-asg"
    propagate_at_launch = true
  }

  #vpc_zone_identifier = [aws_subnet.example1.id, aws_subnet.example2.id]
}
