from __future__ import print_function
import boto3
import json
import datetime

from datetime import datetime

from chalice import Chalice

from chalice import CORSConfig
from chalice import CognitoUserPoolAuthorizer

from chalice import BadRequestError
from chalice import NotFoundError
from chalice import ChaliceViewError


app = Chalice(app_name='mygame_app')
app.debug = True


print('Loading function')


dynamodb_client = boto3.client('dynamodb')


cors_config = CORSConfig(
#    allow_origin='http://localhost:63342',
#    allow_origin='http://mygame.jimhough.com.s3-website-us-east-1.amazonaws.com',
    allow_origin='http://mygame.jimhough.com',
    allow_headers=['Access-Control-Allow-Origin', 'X-Special-Header', 'User'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)


# For Authentication:
# from http://chalice.readthedocs.io/en/latest/api.html#authorization
#authorizer = CognitoUserPoolAuthorizer(
#    'MyPool', header='Authorization',
#    provider_arns=['arn:aws:cognito:...:userpool/name'])

#authorizer = CognitoUserPoolAuthorizer(
#    name='MyPool', 
#    provider_arns=['arn:aws:cognito-idp:us-east-1:1234567890:userpool/us-east-1_SDqT99999'],
#    header='Authorization'
#    )


#@app.route('/user-pools', methods=['GET'], authorizer=authorizer)
#def authenticated():
#    return {"secure": True}


@app.route('/time', methods=['GET'], cors=cors_config)
def get_time():
    
    request = app.current_request
    
    user = request.headers['User']
    
    time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return json.dumps('The time is now ' + time_string + ' UTC.')


@app.route('/game/{game_id}', methods=['GET'], cors=cors_config)
def get_game_state_attrubutes(game_id):
    
    request = app.current_request
    
    user = request.headers['User']

    try:
        response = dynamodb_client.get_item(
            TableName='mygame_games',
            Key={'game_id': {'S': str(game_id)} }
#            ProjectionExpression='GamesStatus, PlayerCount, Players'
        )
#        print(response)
        return response['Item']
    except KeyError:
        raise NotFoundError("Unknown game_id '%s'." % (str(game_id)))
        


@app.route('/game/{game_id}', methods=['DELETE'], cors=cors_config)
def delete_game(game_id):
    
    request = app.current_request
    
    user = request.headers['User']

    try:
        response = dynamodb_client.delete_item(
            TableName='mygame_games',
            Key={'game_id': {'S': str(game_id)}, },
            ReturnValues='ALL_OLD'
        )
#        return response
        return response['Attributes']
    except KeyError:
        raise NotFoundError("Unknown game_id '%s'." % (str(game_id)))
