dockyard
========

Dockyard is web UI for docker

Follow us on [![alt text][1.2]][1]

Setup Development Environment
=============================

```
$ virtualenv dockyard
$ cd dockyard
$ source bin/activate
$ pip install -r requirements.txt
```

Install dockyard-mysql
```
$ docker pull mysql
$ docker run --name dockyard-mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=d0cky4rd mysql
```

Install dockyard-web
```
$ docker pull datt/datt-archlinux
$ docker run --name dockyard-web -a stdin -a stdout -a stderr -i -t -p 2222:22 -p 80:80 --expose 22 --expose 80 datt/datt-archlinux /bin/bash
```

Once you are inside container
```
$ pacman -Syyuu --ignore filesystem
```

```
$ sudo python -B dockyard.py -b 0.0.0.0:80
```

[1.2]: http://i.imgur.com/wWzX9uB.png (getdockyard)
[1]: http://www.twitter.com/getdockyard
