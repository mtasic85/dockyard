dockyard
========

Dockyard is web UI for docker

Follow us on [![alt text][1.2]][1]

Setup Development Environment
=============================

Install dockyard-mysql
```
$ docker pull mysql
$ docker run --name dockyard-mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=d0cky4rd mysql
$ mysql -u root -h 127.0.0.1 -p
mysql> create database dockyard;
mysql> GRANT ALL PRIVILEGES ON dockyard.* To 'dockyard'@'localhost' IDENTIFIED BY 'd0cky4rd';
mysql> GRANT ALL PRIVILEGES ON dockyard.* To 'dockyard'@'172.17.42.1' IDENTIFIED BY 'd0cky4rd';
```

Install dockyard-web
```
$ docker pull base/archlinux
$ docker run --name dockyard-web -a stdin -a stdout -a stderr -i -t -p 80:80 --expose 80 base/archlinux /bin/bash
```

Once you are inside container
```
$ pacman -Syyuu base-devel git pypy mysql --ignore filesystem --noconfirm
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

[1.2]: http://i.imgur.com/wWzX9uB.png (getdockyard)
[1]: http://www.twitter.com/getdockyard
