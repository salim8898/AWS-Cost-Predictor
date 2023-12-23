resource "aws_eks_cluster" "example_cluster" {
  name     = "my-eks-cluster" # Name your EKS cluster
  role_arn = aws_iam_role.eks_role.arn # ARN of the IAM role for EKS

  # Version of EKS to use
  version = "1.21"

  vpc_config {
    subnet_ids         = ["subnet-xxxxxxxxxxx", "subnet-yyyyyyyyyyy"] # Subnet IDs for EKS cluster
    security_group_ids = ["sg-xxxxxxxxxxx"] # Security Group IDs for EKS cluster
  }

  tags = {
    Environment = "Production"
    Project     = "MyProject"
  }
}

resource "aws_iam_role" "eks_role" {
  name = "eks-cluster-role"

  # Assume Role Policy for EKS cluster
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = {
        Service = "eks.amazonaws.com"
      },
      Action    = "sts:AssumeRole"
    }]
  })
}

# IAM Role Policy for EKS cluster
resource "aws_iam_policy" "eks_policy" {
  name = "eks-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Action    = ["eks:Describe*", "eks:List*", "eks:AccessKubernetesApi"],
      Resource  = "*"
    }]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "eks_policy_attachment" {
  policy_arn = aws_iam_policy.eks_policy.arn
  role       = aws_iam_role.eks_role.name
}
