dockyard
========

__Dockyard__ delivers a __massively scalable cloud computing__ platform based
on [Docker](https://docker.io). It comes with complete web interface
for both administrating and regularly using platform. It supports
multiple hosts and cross-datacenter management.

Setup Development Environment _[in progress]_
=============================================

## Controller Node _ctrl0_

Install dockyard-mysql
```
$ docker pull mysql
$ docker run --name dockyard-mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=d0cky4rd mysql
$ mysql -u root -h 127.0.0.1 -p
mysql> CREATE DATABASE dockyard;
mysql> GRANT ALL PRIVILEGES ON dockyard.* TO 'dockyard'@'localhost' IDENTIFIED BY 'd0cky4rd';
mysql> GRANT ALL PRIVILEGES ON dockyard.* TO 'dockyard'@'172.17.42.1' IDENTIFIED BY 'd0cky4rd';
```

Install dockyard-web
```
$ docker pull base/archlinux
$ docker run --name dockyard-web -a stdin -a stdout -a stderr -i -t \
    -p 80:80 --expose 80 base/archlinux /bin/bash
```

Once you are inside container
```
$ pacman -Syyuu base-devel screen git pypy mysql vim --ignore filesystem --noconfirm
$ curl -O http://python-distribute.org/distribute_setup.py
$ curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
$ pypy distribute_setup.py
$ pypy get-pip.py
$ ln -s /opt/pypy/bin/pip /usr/local/bin/pip-pypy
$ pip-pypy install virtualenv
$ ln -s /opt/pypy/bin/virtualenv /usr/local/bin/virtualenv-pypy
$ git clone https://github.com/mtasic85/dockyard.git
$ virtualenv-pypy dockyard
$ cd dockyard
$ source bin/activate
$ pip install -r requirements.txt
$ python -B dockyard.py -b 0.0.0.0:80
```

## Network Node: _net0_

## Compute Nodes: _compX_

Compute nodes store volumes locally, so docker container and volume are always on
same machine.
For storing volumes, dockyard uses mounted btrfs filesystem(s), and creates
subvolumes.
You can pass any number of mount points to dockyard-slave container.
It really depends on host system.
Lets assume that each compute node has follwoing devcies mounted:
```
/dev/sdb1 -> /mnt/sdb1
/dev/sdc1 -> /mnt/sdc1
/dev/sdd1 -> /mnt/sdd1
/dev/sde1 -> /mnt/sde1
```

Disable auto-start of docker containers when host reboots.
```
sudo sh -c "echo 'DOCKER_OPTS=\"-r=false\"' > /etc/default/docker"
```

Install dockyard-web
```
$ docker pull base/archlinux
$ docker run --name dockyard-slave --privileged=true \
    -v /var/run/docker.sock:/docker.sock \
    -v /mnt/sdb1:/mnt/sdb1 \
    -v /mnt/sdc1:/mnt/sdc1 \
    -v /mnt/sdd1:/mnt/sdd1 \
    -v /mnt/sde1:/mnt/sde1 \
    -p 4000:4000 --expose 4000 \
    -a stdin -a stdout -a stderr -i -t base/archlinux /bin/bash
```

Once you are inside container
```
$ pacman -Syyuu base-devel btrfs-progs screen git pypy mysql vim --ignore filesystem --noconfirm
$ curl -O http://python-distribute.org/distribute_setup.py
$ curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
$ pypy distribute_setup.py
$ pypy get-pip.py
$ ln -s /opt/pypy/bin/pip /usr/local/bin/pip-pypy
$ pip-pypy install virtualenv
$ ln -s /opt/pypy/bin/virtualenv /usr/local/bin/virtualenv-pypy
$ git clone https://github.com/mtasic85/dockyard.git
$ virtualenv-pypy dockyard
$ cd dockyard
$ source bin/activate
$ cd slave
$ pip install -r requirements.txt
$ python -B slave.py
```

To exit from dockyard-web container without stopping it, press CTRL+P CTRL+Q.

Social Media
============

Follow us on [![alt text][1.2]][1]

[1.2]: http://i.imgur.com/wWzX9uB.png (getdockyard)
[1]: http://www.twitter.com/getdockyard
