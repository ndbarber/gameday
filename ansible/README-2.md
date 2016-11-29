This company gets crazier and crazier. The chowder taps were out twice last week and while they are telling us that they clean the ball pit nightly, the funky smell says otherwise. Our team has opted to cancel our ball pit standups. In other news, one of the people living in the incubator house accidentally wiped out the entire AWS account. We had to recreate everything. Some of this was automated which made it easier. We really need everything to be automated in case this happens again.

I have made some progress on storing messages in DynamoDB. I built some functions that will store parts of the messages in Dynamo. They just need to be dropped into the code. There's also an Ansible playbook for creating the DynamoDB table. This is pretty important because it will let us recreate all of the infrastructure.

- tasks/
	dynamodb.yml: creates a table called gameday-messages-state

- files/
	dynamo_snippet.py: I started working on this whole "storing in a db table" python thing

### How to use

- copy the dynamodb.yml file to the same directory as the rest of your tasks

- add the dynamodb playbook location to the site.yml file

- run the site.yml playbook ```ansible-playbook site.yml```
