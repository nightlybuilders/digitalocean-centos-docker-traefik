import os

from fabric import task


HERE = os.path.dirname(os.path.abspath(__file__))


@task
def setup(c):
    c.run('mkdir -p docker/infra')
    """Upload the docker-compose.yml"""
    c.put(f'{HERE}/docker-compose.yml',
          remote='docker/infra/docker-compose.yml')
    c.put(f'{HERE}/traefik.toml',
          remote='docker/infra/traefik.toml')
    c.put(f'{HERE}/dot.env',
          remote='docker/infra/.env')
    
    result = c.run('docker network ls | grep proxy', warn=True)
    if result.failed:
        c.run('docker network create proxy')

    c.run('test -f docker/infra/acme.json || touch docker/infra/acme.json && chmod 600 docker/infra/acme.json')


@task
def up(c):
    """docker-compose up -d"""
    with c.cd('~/docker/infra'):
      c.run('docker-compose config')
      c.run('docker-compose up -d')


@task
def down(c):
    """docker-compose down"""
    with c.cd('~/docker/infra'):
      c.run('docker-compose down')


@task
def ps(c):
    """docker-compose ps"""
    with c.cd('~/docker/infra'):
      c.run('docker-compose ps')


@task
def config(c):
    """docker-compose config"""
    with c.cd('~/docker/infra'):
      c.run('docker-compose config')


@task
def restart(c, container=''):
    """docker-compose restart <container>"""
    with c.cd('~/docker/infra'):
      c.run(f'docker-compose restart {container}')