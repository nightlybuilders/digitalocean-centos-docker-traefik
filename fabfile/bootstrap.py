from fabric import task


@task
def bootstrap_centos(context, timezone='UTC'):
    """
    Bootstrap the CentOS machine.

    - Add an 'admin' user. The admin user will have no password. One can only
      access the machine with SSH!
    - Copy 'authorized_keys' from root-user to the new 'admin' user
    - Disable SSH login for 'root'
    - Setup a firewall
        - Only SSH, HTTP, HTTPS and 8080/tcp are open
    - Set default time zone
    - Install and synchronize with NTP
    - Setup a 'swapfile' with 4GB
    - Configure 'swappiness'
    - Configure 'vfs_cache_pressure'

    NOTE:
      After running 'bootstrap_centos', 'ssh root@<ip>' does not work
      anymore! Use 'ssh admin@<ip>'.
      If you want to log in to root-user, use the 'admin' user first to
      connect, then change to the root-user:
        ```
        $ ssh admin@<ip>
        $ sudo -i
        # whoami
        ```
    """
    # ---------------------
    # setup an 'admin' user
    # ---------------------
    context.run('adduser admin')
    # remove the password
    context.run('passwd -d admin')
    # grant root privileges
    context.run('gpasswd -a admin wheel')
    # copy the SSH authorized_keys from 'root' to 'admin'
    context.run('mkdir -p /home/admin/.ssh')
    context.run('cp ~/.ssh/authorized_keys /home/admin/.ssh/')
    context.run('chown -R admin:admin /home/admin/.ssh')
    context.run('chmod 700 /home/admin/.ssh')
    context.run('chmod 600 /home/admin/.ssh/authorized_keys')
    # disable root-login
    context.run("sed -i -e 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config")
    context.run('systemctl reload sshd')
    # NOTE:
    #  From now on, 'ssh root@<ip>' does not work anymore! If you want to do so,
    #  use the 'admin' user first to connect, then change to the root-user:
    #   ```
    #   $ ssh admin@<ip>
    #   $ sudo -i
    #   # whoami
    #   ```
    # for now, we continue as root-user

    # update all dependencies
    context.run('yum check-update || yum -y update')

    # --------------
    # firewall setup
    # --------------
    context.run('yum -y install firewalld')
    context.run('systemctl start firewalld')
    context.run('firewall-cmd --permanent --add-service=ssh')
    context.run('firewall-cmd --permanent --add-service=http')
    context.run('firewall-cmd --permanent --add-service=https')
    context.run('firewall-cmd --permanent --add-port=8080/tcp')
    context.run('firewall-cmd --reload')
    context.run('systemctl enable firewalld')  # autostart

    # ------------------------
    # time & timezone settings
    # ------------------------
    # Set timezone
    context.run('timedatectl set-timezone '.format(timezone))
    # NTP Synchronization
    context.run('yum -y install ntp')  # keep time up2date
    context.run('systemctl start ntpd')
    context.run('systemctl enable ntpd')  # autostart

    # ---------
    # Swap File
    # ---------
    context.run('fallocate -l 4G /swapfile')
    context.run('dd if=/dev/zero of=/swapfile count=4096 bs=1MiB')
    context.run('chmod 600 /swapfile')
    context.run('mkswap /swapfile')
    context.run('swapon /swapfile')
    context.run("""
        sh -c 'echo "/swapfile none swap sw 0 0" >> /etc/fstab'
    """)
    # Lower Swapiness & Cache Pressure
    context.run('sysctl vm.swappiness=10')
    context.run("""
        sh -c 'echo "vm.swappiness = 10" >> /etc/sysctl.conf'
    """)
    context.run('sysctl vm.vfs_cache_pressure=50')
    context.run("""
        sh -c 'echo "vm.vfs_cache_pressure = 50" >> /etc/sysctl.conf'
    """)


@task
def install_docker(context):
    # ------------
    # Docker setup
    # ------------
    # install docker
    context.run('curl -fsSL https://get.docker.com/ | sh')
    context.run('sudo usermod -aG docker $(whoami)')
    context.run('id $(whoami)')
    context.run('sudo systemctl enable docker.service')
    context.run('sudo systemctl start docker.service')

    # Docker compose is written in Python. Keep Python up2date
    context.run('sudo yum -y update python*')

    # install docker-compose
    context.run('sudo yum install -y epel-release')
    context.run('sudo yum install -y python-pip')
    context.run('sudo pip install --upgrade pip')
    # Currently, there is an issue when trying to install docker-compose on
    # CentOS 7 with the latest pip version (pip >= 10.0)
    # Workaround with adding '--ignore-installed'
    # https://github.com/blockstack/blockstack-core/issues/504
    context.run('sudo pip install docker-compose --ignore-installed')