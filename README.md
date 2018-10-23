# Digital Ocean CentOS Setup with Docker and Traefik

This projects helps manage a CentOS instance on [DigitalOcean](https://www.digitalocean.com/).
After the setup, the CentOS will have:

- Installed and running [Docker](https://www.docker.com/) including ``docker-compose``
- Installed and running Traefik

## Requirements

We assume that a Droplet with CentOS 7.5+ is already running. We further
assume, the CentOS machine can already be accessed with SSH as 'root': 

 - ``ssh root@<ip>`` should work, otherwise we cannot perform the setup
  successfully!

Make sure to have [Python 3.6.3](https://www.python.org/) (or higher)
installed before running ``./bootstrap.sh``.

Run ``./bootstrap.sh`` on your local machine to install all dependencies
locally. Managing the CentOS setup is done by
[Fabric](http://www.fabfile.org). All local dependencies are installed via
[Pipenv](https://pipenv.readthedocs.io) so your system's Python will not be
touched.

## How to Use

### Get a list of available tasks

```
pipenv run fab -l
```

### Bootstrap a CentOS machine without Docker

Prepare the machine initially. NOTE: Please run the command with ``--help``
before actually executing it. This is a one time command and running it
multiple times may produce unexpected results!

```
pipenv run fab -H root@<ip> bootstrap.centos --help
```

### Install Docker & Docker Compose

```
pipenv run fab -H <ip> bootstrap.docker --help
```


## Traefik

### Setup

Upload the ``docker-compose.yml`` with the basic setup of Traefik

```
pipenv run fab -H <ip> infra.setup --help
```

### Manage

Use one of the following commands to manage the docker compose stack

```
pipenv run fab -H <ip> infra.up --help
pipenv run fab -H <ip> infra.down --help
pipenv run fab -H <ip> infra.ps --help
```


## Not yet on Digital Ocean?

If you are not yet using [DigitalOcean](https://m.do.co/c/6c3524a1f261), get
a jump start by using our [referral link](https://m.do.co/c/6c3524a1f261).
Setting up your own account using our [referral
link](https://m.do.co/c/6c3524a1f261) will give you [$100](https://m.do.co/c/6c3524a1f261) to use over the next 60 days. Pretty cool of them, isn't it?