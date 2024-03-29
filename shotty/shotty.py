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
def cli():
    """shotty manages snapshots"""

@cli.group('volumes')
def volumes():
    """commands for volumes"""

@volumes.Commands('snapshot',
    help = "Create snapshots of all volumes")
@click.option('--project', default = None,
    help = "Only instances for project (tag project:<name>)")
def create_snapshots(project):
    "Create Snapshot for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print("Create Snapshot {0}".format(v.id))
            v.create_snapshots(Description = "Create by SnapshotAlyzer 30000")

    return



@volumes.command('list')
@click.option('--project',default=None,
    help="Only volumes for project (tag project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
            print (", ".join((
            s.id,
            v.id,
            i.id,
            s.state,
            s.progress,
            s.start_time.st
            s.start_time.strftime("%C")
            )))
    return

@cli.group('instance')
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
    cli()
