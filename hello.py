#!/usr/bin/env python3
import os
import boto3
from flask import Flask, render_template

aws_access_key = os.environ.get('ACCESS_KEY_ID')
aws_secret_key = os.environ.get('SECRET_ACCESS_KEY')

app = Flask(__name__, template_folder='html')
aws_session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
)
db_client = aws_session.client('dynamodb')

@app.route('/')
def get_index():
    list_of_users_from_db = db_client.scan(
        TableName='CTF-Table',
        FilterExpression= "#u > :z",
        ExpressionAttributeNames= {"#u":"userid"},
        ExpressionAttributeValues= {":z": {"N":"0"}}
    )['Items']
    parsed_db_results = {}
    for item in list_of_users_from_db:
        username = item['username']['S']
        favorite_artist = item['favorite_artist']['S']
        parsed_db_results[username] = favorite_artist
    return render_template(
        template_name_or_list = "index.html",
        title="WM Security Dashboard",
        list_of_users=parsed_db_results
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
