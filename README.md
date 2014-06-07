dockyard
========

Dockyard is web UI for docker


Setup Development Environment
=============================

```
$ virtualenv dockyard
$ cd dockyard
$ source bin/activate
$ pip install -r requirements.txt
```

```
$ docker pull orchardup/mysql
$ docker run -d -p 3306:3306 -e MYSQL_DATABASE=dockyard -e MYSQL_ROOT_PASSWORD=d0cky4rd -e MYSQL_USER=dockyard -e MYSQL_PASSWORD=d0cky4rd orchardup/mysql
```
