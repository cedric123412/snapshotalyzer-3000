import boto3
import click


session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instance():
    """Commands for insances"""


@instance.command('list')
@click.option('--project',default=None,
    help="Only instances for project (tag project:<name>)")
def list_instance(project):
    "List EC2 instance"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print( ', '.join((i.id,
                          i.instance_type,
                          i.placement['AvailabilityZone'],
                          i.state['Name'],
                          i.public_dns_name,
                          tags.get('Project','<no project>'))))

    return

@instance.command('stop')
@click.option('--project',default=None,help="only instance for project")
def stop_instance(project):

    "Stop EC2 instance"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instance.command('start')
@click.option('--project',default=None,help="only instance for project")
def stop_instance(project):

    "Start EC2 instance"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    instance()
