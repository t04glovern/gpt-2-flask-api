#!/bin/sh

BUCKET_NAME=devopstar

## Creates S3 bucket
aws s3 mb s3://$BUCKET_NAME

## S3 cloudformation deployments
### Base
aws s3 cp cloudformation/base/fargate-cluster.yaml s3://$BUCKET_NAME/resources/gpt-2-flask-api/cloudformation/base/fargate-cluster.yaml
aws s3 cp cloudformation/base/fargate-service.yaml s3://$BUCKET_NAME/resources/gpt-2-flask-api/cloudformation/base/fargate-service.yaml
aws s3 cp cloudformation/base/vpc-networking.yaml s3://$BUCKET_NAME/resources/gpt-2-flask-api/cloudformation/base/vpc-networking.yaml
### CI/CD
aws s3 cp cloudformation/cicd/codebuild.yaml s3://$BUCKET_NAME/resources/gpt-2-flask-api/cloudformation/cicd/codebuild.yaml
