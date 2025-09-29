# hello-world-fargate-python-cdk

# Hello World on AWS ECS Fargate (Go + CDK Python)

This repo builds a tiny Go web app, pushes it to **Amazon ECR**, and serves it via **ECS Fargate** behind an **ALB**, provisioned with **AWS CDK in Python**. CI/CD is **GitHub Actions**.

## Prereqs
- AWS account + IAM user with ECR/ECS/CloudFormation/CDK permissions
- GitHub repo secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`
- Docker, Python 3.11, Node (CI installs CDK)

## Local test
```bash
cd app
docker build -t hello-world-local .
docker run -p 8080:8080 hello-world-local
# open http://localhost:8080 (and /healthz)
