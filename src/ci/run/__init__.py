import click
from ci.run.jenkinsfile import jenkins


@click.group("run")
def group():
    pass


group.add_command(jenkins)
