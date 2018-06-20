# monitor-deploy

use fabric3 deploy monitor

## depended

> `pip3`, `Fabric3`

### ops

> ubuntu

```bash
sudo apt-get install python3-pip

#upgrade
sudo pip3 install --upgrade pip

# uninstall
sudo apt-get remove python3-pip
```

> CentOS

```bash
# add epel source
yum install epel-release

# install python3.4
yum install python34

yum install python34-setuptools
easy_install-3.4 pip
```

> Install Fabric3

```bash
sudo pip install Fabric3
#sudo pip3 install Fabric3
```

## go-seele deploy

```text
┌── monitor-deploy
│   └── conf
│       ├── seele
│           └── nodes-seele
│       └── ...
│   └── script
│       ├── seele
│           ├── bin
│           └── build
│   └── sources
│       ├── go-seele-source
│            └──config
│  
```