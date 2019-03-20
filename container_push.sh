# Create ECR (if not already existing)
aws ecr create-repository --repository-name "gpt-2-flask-api"

ACCOUNT_ID=$(aws sts get-caller-identity |  jq -r '.Account')
$(aws ecr get-login --no-include-email --region us-east-1)

docker build -t gpt-2-flask-api .
docker tag gpt-2-flask-api:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/gpt-2-flask-api:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/gpt-2-flask-api:latest
