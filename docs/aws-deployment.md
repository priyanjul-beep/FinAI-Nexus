# AWS Cloud Deployment Guide

## Overview

This guide outlines the production architecture for deploying FinAI Nexus on Amazon Web Services (AWS).

```mermaid
graph TD
    User([Users]) --> CloudFront[AWS CloudFront CDN]
    CloudFront --> ALB[Application Load Balancer]
    
    subgraph VPC Public Subnets
        ALB --> FargateFrontend[ECS Fargate - Next.js Frontend]
    end
    
    subgraph VPC Private Subnets
        ALB --> FargateBackend[ECS Fargate - FastAPI Backend]
        FargateBackend --> RDS[(Amazon RDS PostgreSQL + pgvector)]
        FargateBackend --> ElastiCache[(Amazon ElastiCache Redis)]
        FargateBackend --> S3[(Amazon S3 - Policy Documents)]
    end
    
    subgraph Security & Management
        Secrets[AWS Secrets Manager] --> FargateBackend
        CloudWatch[Amazon CloudWatch Metrics & Logs] <-- FargateBackend
    end
```

## Recommended Services

1. **Frontend Deployment**: Next.js app deployed on **AWS ECS Fargate** or **AWS Amplify**, fronted by **Amazon CloudFront**.
2. **Backend Services**: FastAPI containerized application deployed on **AWS ECS Fargate** with Auto Scaling.
3. **Database**: **Amazon RDS for PostgreSQL 16** with `pgvector` extension enabled.
4. **Caching & Redis**: **Amazon ElastiCache for Redis**.
5. **Storage**: **Amazon S3** for uploaded raw PDF policy documents and reports.
6. **Secret Management**: **AWS Secrets Manager** storing API keys and DB credentials.
7. **Monitoring**: **Amazon CloudWatch** for logs and container metrics.

## Deployment Steps

1. **Build and Push Docker Images**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t finai-backend -f infra/docker/backend.Dockerfile .
   docker tag finai-backend:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/finai-backend:latest
   docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/finai-backend:latest
   ```

2. **Provision Infrastructure**: Use AWS CloudFormation or Terraform to create VPC, RDS PostgreSQL, ElastiCache, ECS Cluster, and ALB.

3. **Database Migration**:
   Run database initialization task in ECS task definition to create schemas and run initial seeders.
