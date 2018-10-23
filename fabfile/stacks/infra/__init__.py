import os

from fabric import task


HERE = os.path.dirname(os.path.abspath(__file__))


@task
def setup(c):
    """Upload the docker-compose.yml"""
    c.put(f'{HERE}/docker-compose.yml',
          remote='docker-compose.yml')


@task
def up(c):
    """docker-compose up -d"""
    c.run('docker-compose -f ~/docker-compose.yml up -d')


@task
def down(c):
    """docker-compose down"""
    c.run('docker-compose -f ~/docker-compose.yml down')


@task
def ps(c):
    """docker-compose ps"""
    c.run('docker-compose -f ~/docker-compose.yml ps')