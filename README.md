## SAM Movies API & Resource Policy

SAM Template with Lambda Function to spin up a DynamoDB backed Movies API and Resource Policy to be attached to it.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.

AM Movies API with APIGW Resource Policies

###Pre-Requisites:

aws-cli/1.15.0, jq-1.5, perl v5.18.2, python2.7

Fill in the following variables first and set as Env Vars

```bash

#AWS Region where your API is deployed
REGION=""
#AWS Account who will access your API
AccountA=""
#AWS Account where your API is hosted
AccountB=""
#User in Account A who will access your API
userA=""
#S3 Bucket where the SAM templates will live
S3Bucket=""

Deploy the movies API

mkdir ./build
cp -p -r ./movies ./build/movies
pip install -r requirements.txt -t ./build

aws cloudformation package --template-file template.yaml --output-template-file template-out.yaml --s3-bucket $S3Bucket

aws cloudformation deploy --template-file template-out.yaml --stack-name apigw-resource-policies-demo --capabilities CAPABILITY_IAM

Get API ID after deployment

API_ID=$(aws cloudformation describe-stacks --stack-name apigw-resource-policies-demo --query 'Stacks[0].Outputs[?OutputKey==`AwsApiId`].OutputValue' --output text)

cp policy.json_template policy.json

perl -p -i -e "s/account_idA/$AccountA/g" policy.json
perl -p -i -e "s/account_idB/$AccountB/g" policy.json
perl -p -i -e "s/region/$REGION/g" policy.json
perl -p -i -e "s/api_id/$API_ID/g" policy.json
perl -p -i -e "s/user/$userA/g" policy.json

policy=`cat policy.json`

aws apigateway update-rest-api --rest-api-id $API_ID --patch-operations op=replace,path=/policy,value="$policy"

```





