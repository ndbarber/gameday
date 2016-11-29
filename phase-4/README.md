This will be my last entry in the worklog. This place is a disaster. You will all be fired in a few minutes anyways. If for some reason you still care about winning, you could just configure and run these Ansible playbooks to stand up all the infrastructure. I'm going to leave the unicorn business. I think my days of renting mythical animals are over. 

### Files

- site.yml: has all the includes needed to build the entire stack and all endpoints 

- vars.yml: all variables that are needed to create all endpoints

- tasks/ : all the playbooks needed to create each individual part/service
	- server.yml
	- dynamodb.yml
	- s3.yml
	- sqs.yml
	- kinesis.yml
	- lambda_s3.yml
	- lambda_sqs.yml
	- lambda_kinesis.yml
	- networks.yml

- templates/ : additional assets needed
	- userdata.txt.j2: userdata to use in the EC2 launch configuration
	- bucket_policy.json: S3 bucket policy to allow The Game to send unicorn parts
	- queue_policy.json: SQS queue policy to allow The Game to send unicorn parts

- files/ : the python code for each lambda function
	- lambda_kinesis.py
	- lambda_s3.py
	- lambda_sqs.py

### How to use

- Pip install ansible (should be v2.2) and boto3 ```pip install ansible boto3```

- fill out all the variables needed in the vars.yml file

- copy the credentials from the dashboard for the account you're using

- run ```ansible-playbook site.yml```
