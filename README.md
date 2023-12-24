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
          iac_path: IAC.    # path where the Terraform code is reside at root of your git repository
        env:    # AWS key need to be added to your Git repo secret to authenticate to AWS Cost API
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        # continue-on-error: true

```
