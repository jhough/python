
# Deploy API Gateway and Lambda using AWS Chalice (within AWS Cloud9 environment)

Chalice provides:
* A command line tool for creating, deploying, and managing your app
* A familiar and easy to use API for declaring views in python code (similar to Python Flask)
* Automatic IAM policy generation

https://chalice.readthedocs.io/en/latest/index.html

Prerequisite: You will need an IAM user in the AWS account you're using.



## Cloud9 Environment (IDE)

Follow these instructions to create a Cloud9 environment (IDE):
https://docs.aws.amazon.com/cloud9/latest/user-guide/tutorial.html
Step 1: Create an Environment

Then from the Cloud9 command line:

```
$ sudo yum -y update

$ sudo yum -y install python36
```


## Install AWS Chalice

From the Cloud9 command line:

```
$ sudo pip install chalice

$ chalice new-project helloworld
$ cd helloworld

$ cat app.py

from chalice import Chalice

app = Chalice(app_name="helloworld")

@app.route("/")
def index():
    return {"hello": "world"}

$ chalice deploy
```

This will cause this error:

"An error occurred (InvalidClientTokenId) when calling the CreateRole operation: The security token included in the request is invalid"

*InvalidClientTokenId Cause:*

Cloud9 is generating (and regenerating) a set of temporary credentials every five minutes for the ec2-user in ~/.aws/credentials. This prevents the EC2 instance from inheriting permissions from an IAM role assigned to the instance itself.

*InvalidClientTokenId Resolution:*

Step 1: Turn off the managed temporary credentials.
Within Cloud9 Settings (accessed via the gear icon on upper right), under AWS Settings section, turn off the AWS Managed Temporary Credentials.

Step 2: Install AWS access key.
You must make use an IAM user and create a static AWS access key.
Go to the AWS web console and select IAM service. Go to your IAM user. Select the Security credentials tab. Create an access key. Save the Access key ID and Secret access key.

From the command line:

```
$ aws configure
```
... enter the access key, secret access key, region=us-east-1, format=json

Then try again:
```
$ chalice deploy
```
...
Rest API URL: https://endpoint/api

```
$ curl https://endpoint/api
{"hello": "world"}
```


## A little more educational Chalice app

Using the Cloud9 navigation on the left side, find and open the app.py file

Edit the app.py file. Enter this code:

https://github.com/jhough/python/blob/master/SimpleChalice/app.py

Save the file. Then run this command:

```
$ chalice deploy
```

Get the endpoint and use in these commands:

```
$ curl --include --request GET --header "User: Jim" --header "Content-Type: application/json" https://APIIDGOESHERE.execute-api.us-east-1.amazonaws.com/api/time

$ curl --include --request GET --header "User: Jim" --header "Content-Type: application/json" https://APIIDGOESHERE.execute-api.us-east-1.amazonaws.com/api/game/1
```
(You will get ResourceNotFoundException until you create the DynamoDB table. You can do this manually via the web console.)



## For more on Chalice:

https://chalice.readthedocs.io/en/latest/index.html

