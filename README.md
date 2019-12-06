# snapshotalyzer-3000
Demo project to manage AWS EC2 instance snapshots

## About

This project is demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuration

shotty uses the Configuration file created by the AWS cli. e.g.

'aws configure --profile shotty'

##Running

'pipenv run python shotty/shotty.py <command> <--project=PROJECT>'

*command* is list, stop, or Start
*project" is optional
