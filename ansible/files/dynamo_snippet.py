# DYNAMODB = boto3.resource('dynamodb')
# STATE_TABLE = DYNAMODB.Table('XXXXXX') # The Dynamodb table name needed here

def store_message(input_id, part_num, data):
    """
    stores the message locally on a file on disk for persistence
    """
    try:
        STATE_TABLE.update_item(
            Key={
                'Id': input_id
            },
            UpdateExpression="set #key=:val",
            ExpressionAttributeValues={
                ":val":data
            },
            ExpressionAttributeNames={
                "#key":str(part_num),
                "#p":"processed"
            },
            ConditionExpression="attribute_not_exists(#p)"
        )
    except Exception:
        # conditional update failed since we have already processed this message
        # at this point we can bail since we don't want to process again
        # and lose cash moneys
        return False


# here is an activation code: dvorakrulez

def check_messages(input_id):
    """
    checking to see in dynamo if we have the part already
    """
    # do a get item from dynamo to see if item exists
    response = STATE_TABLE.get_item(
        Key={
            'Id': input_id
        },
        ConsistentRead=True
    )
    item = response['Item']
    # check if both parts exist
    if "0" in item and "1" in item:
        print("we have both!")
        # we have all the parts
        build_final(item, input_id)
        # now we need to update dynamo saying we processed this message
	# TODO: implement this. 
    else:
        # we have some parts but not all
        return
