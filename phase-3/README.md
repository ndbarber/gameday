OK, this place is really starting to get to me. I was sick for a few days because the chowder went sour. I am done with that and I'm never working at a place that offers all you can eat chowder. We have boarded up the door to the ball pit. The masseuse stopped coming on Wednesdays.  

I've realized that if we only process HTTP messages we will be missing out on a lot of points. We should try to get more points by responding to messages from other transports. I've written up some ansible code to create an S3 bucket, SQS queue, and a Kinesis stream for the other messages. I know we'll need a policy on our queue and bucket to allow another AWS account to send messages there. I wrote some policies, but I don't know if they work or not. The other account is 336189371117, but the easiest thing to do would be to open the queue and bucket to the world. What's the worst that could happen?

I also think it's time we look into a "serverless" architecture. I'm including a draft of how we can use ansible to create a Lambda function. It should be straight forward to translate the code we have into a Lambda function and then there will be no EC2 instances to manage!

### Files:

- tasks/
	s3.yml: creates an S3 bucket, based on your team name, and places the appropriate bucket policy
	sqs.yml: creates an SQS queue, based on your team name, and places the appropriate queue policy
	kinesis.yml: creates a kinesis stream, based on your team name
	lambda_something.yml: I think this should create a lambda function? For something? 


- templates/
	bucket_policy.json: creates the bucket policy for the S3 bucket
	queue_policy.json: creates the sqs queue policy


### How to use

- add the new tasks to the site.yml file

- run the site.yml playbook to create the new endpoints
