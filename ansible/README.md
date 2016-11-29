# Worklog

What a wild few weeks it has been. A bunch of absurdly dressed teenagers rollerbladed in here and caused a bunch of trouble. "The Plague" no longer works here. He wasn't fired and didn't quit, but sort of dissappeared. Rumor has it that he was arrested on an airplane by the secret service, but who knows. I've been putting in a lot of hours. I hope someone is feeding my cats.

I found the network problems. One of the subnets in the VPC didn't have routes to the internet. There was also an ACL that prevented me from SSHing into the instance. Not that it would matter, "The Plague" had the SSH key and wouldn't share it with anyone. I need to get the application to be highly available by running it on at least 2 instances, but I realized that the Python code is storing the messages in memory. If I use two instances, parts of the same message could go to two different instances. If this happens, the server will never have both parts and we'll miss out on points. We are also in trouble if the server crashes or is shut down-- we'll lose all the messages. An external database seems like the right idea. I think I could use DynamoDB, Elasticache, or RDS. I need to look into this, but in the meantime an Autoscaling group with a minimum and maximum of 1 instance will be OK.

Here are the Ansible playbooks I have been working on. Hopefully these will be useful to set up instance and networks.


- vars.yml: use this to fill out the variables you will use in the Ansible playbooks

- site.yml: run the ansible-playbook script against this playbook. It identifies which 'tasks' you want to run

- tasks/
	server.yml: actions within your AWS account including creates EC2 launch configuration, autoscaling group, elastic load balancer, and security groups
	networks.yml: creates a new VPC in 2 availability zones

### How to use


- Pip install [Ansible](http://docs.ansible.com/ansible/intro_installation.html) either on an EC2 instance or locally ```pip install ansible```

- Fill in the correct values for the variables in the vars.yml file

- Grab the credentials from the GameDay [dashboard](https://dashboard.cash4code.net/?tid=<YOUR_TEAMS_API_TOKEN)

- Run the command to create the EC2 assets ``` ansible-playbook site.yml```

- I think the other thing - the networks.yml - it probably should be in the sites.yml somewhere as well. And then you probably have to change something in the server.yml to refer to the name of the new VPC you're creating.

For more information, visit the [Ansible documentation](http://docs.ansible.com/ansible/index.html) page

