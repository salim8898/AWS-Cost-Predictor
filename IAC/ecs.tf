
resource "aws_ecs_cluster" "my_cluster" {
  name = "my-ecs-cluster" # Name your ECS cluster

  # Other configurations for the ECS cluster can be added here
  # Tags, capacity providers, etc.
}
