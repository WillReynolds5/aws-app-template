# Meeca Backend - AWS SAM Project

This README provides quick instructions for setting up and running the Meeca backend using AWS SAM and local DynamoDB.

## Setup

1. Install required tools and dependencies in virtual env:

   ```
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a Docker network:

   ```
   docker network create sam-local
   ```

3. Start local DynamoDB:

   ```
   docker run -p 8000:8000 --network sam-local --name dynamodb-local amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb
   ```

4. Initialize local DynamoDB table:

   ```
   python init_db.py
   ```

## Development

Build the SAM application:

```
sam build --use-container
```

Run the API locally: (port 3001 as FE is on 3000 and db is on 8000)

```
sam local start-api --debug --port 3001 --docker-network sam-local
```

Use this single command for rapid dev

```
sam build --use-container && sam local start-api --port 3001 --docker-network sam-local --debug --warm-containers eager
```

OR

having trouble connecting the db to workbench?
shut down and restart

```
docker run -p 8000:8000 --network sam-local --name dynamodb-local amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb
```

## Deployment

### Staging Deployment

To deploy the staging environment:

sam build -t template_staging.yaml --use-container
sam deploy -t template_staging.yaml

add klayers with this link: https://github.com/keithrozario/Klayers/tree/master/deployments/python3.9

##

##

##

##

##

##

##

##

##

##

## Template Notes... could be useful

## Deploy the sample application

5. Set up DynamoDB Admin (optional):

   a. Install DynamoDB Admin globally:

   ```
   npm install -g dynamodb-admin
   ```

   b. Run DynamoDB Admin:

   ```
   AWS_REGION=us-west-1 AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local DYNAMO_ENDPOINT=http://localhost:8000 dynamodb-admin
   ```

   This will start the DynamoDB Admin interface, which you can access through your web browser for easier management and visualization of your local DynamoDB data.

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

- SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- [Python 3 installed](https://www.python.org/downloads/)
- Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

- **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
- **AWS Region**: The AWS region you want to deploy your app to.
- **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
- **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
backend$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
backend$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
backend$ sam local start-api
backend$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
Events:
  HelloWorld:
    Type: Api
    Properties:
      Path: /hello
      Method: get
```

## Add a resource to your application

The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
backend$ sam logs -n HelloWorldFunction --stack-name "backend" --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
backend$ pip install -r tests/requirements.txt --user
# unit test
backend$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
backend$ AWS_SAM_STACK_NAME="meeca-backend" python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "meeca-backend"
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
