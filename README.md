# AWS Cost Predictor 🚀
<img src="https://github.com/salim8898/Images/blob/main/pngwing.com.png" alt="AWS Cost Predictor" width="300">

Welcome to the AWS Cost Predictor! 😎 This GitHub Action is your crystal ball 🔮 for AWS deployment costs. It's like peeking into the future of your AWS expenses before hitting that deploy button. Cool, right? 🌟

## What Does It Do?

The AWS Cost Predictor is your pre-deployment buddy, giving you a cost report for major resources like EC2, RDS, EKS, AutoScalingGroup, and EBS volumes. It checks out your Infrastructure as Code (IAC) and generates a detailed cost report before deploying. No surprises when it comes to your AWS bill! 

## How Does It Work?

It will query your IAC code. Just pass down the IAC path in your repo, and voilà! It generates a cost report for your deployment before it's actually deployed. It's the pre-deployment view of your cost. And currently, it supports IAC code of Terraform. 🌐

## Features

- **Pre-Deployment Insights:** Get a sneak peek 👀 into your AWS costs before actually deploying anything.
- **IAC Compatibility:** Works like a charm with Terraform configurations.
- **Specify Path:** Tell us where your Terraform IAC code lives in your repository.
- **Customizable Reports:** Dive into detailed cost breakdowns for your specific AWS resources.
- **GitHub Actions Friendly:** It’s your friendly neighborhood GitHub Action ready to automate the cost estimating game. 🤖

## Supported AWS Resources & Types

### EC2 Instances 🖥️

- **Instance Types:** t2.micro, m5.large, and more!
- **Sizes & Specifications:** Covering a range of specifications and sizes for your instances.
  
### RDS Databases 🗃️

- **DB Types:** MySQL, PostgreSQL, SQL Server, and more!
- **Storage Options:** Multi-AZ, GP2, Provisioned IOPS, and more!

### EBS Volumes 💾

- **Volume Types:** gp2, gp3, io1, sc1, st1 - catering to diverse storage needs.
- **Sizes:** Choose from various sizes tailored for your applications.

### AutoScaling Groups 🔄

- **Scaling Policies:** Scale in and scale out policies to match your application needs.
- **Load Balancers:** Integrations with Elastic Load Balancers for optimized traffic distribution.

### EKS Clusters 🌐

- **Cluster Configurations:** Flexible configurations for your Kubernetes clusters.

### Workflow Example

To use this action, create a workflow file (e.g., `.github/workflows/aws-cost-predictor.yml`) in your repository:

```
name: AWSCostPredict
on:
  push:
    branches: [ "main" ]  # change trigger as per your branch and event type
    
jobs:
  AWSCostPredict:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2
        
      - name: Predict cost
        uses: salim8898/AWS-Cost-Predictor@v1.0.0
        with:
          iac_path: IAC    # path of IAC folder in your repo
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        # continue-on-error: true

```
### Output Report Sample

```
------------------------------
Cost Predict Output:
+------------------------------------+----------------+-------------+--------------+
+------------------------------------+----------------+-------------+--------------+
| Service Name                       | Instance Class | Hourly Cost | Monthly Cost |
+------------------------------------+----------------+-------------+--------------+
| AmazonRDS/aws_db_instance          | db.t2.micro    |   0.017 USD |    12.41 USD |
| AmazonEC2/aws_ebs_volume           | gp3/50 GB      |    0.08 USD |     4.00 USD |
| AmazonEC2/aws_ebs_volume           | gp2/10 GB      |     0.1 USD |     1.00 USD |
| AmazonEKS/aws_eks_cluster          | my-eks-cluster |     0.1 USD |    73.01 USD |
| AmazonEC2/aws_instance             | m5.large       |   0.096 USD |    70.09 USD |
| AmazonEC2/aws_instance             | t2.micro       |  0.0116 USD |     8.47 USD |
| AmazonEC2/aws_launch_configuration | m7g.large      |  0.0867 USD |    63.30 USD |
| AmazonEC2/aws_launch_configuration | m7g.large      |  0.0867 USD |    63.30 USD |
| ------Total Cost------             |                |    0.58 USD |   295.58 USD |
+------------------------------------+----------------+-------------+--------------+
+------------------------------------+----------------+-------------+--------------+

```
