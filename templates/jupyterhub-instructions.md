# Prerequisites

$ uname -a
Linux CharlesH-HP8300-Ubuntu1604 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux

$ python3 --version
Python 3.5.2
# This must be 3.3 or above

## Install docker
$ sudo apt-get install docker.io

$ docker ps
If this gives a permission error, then do the following.
$ sudo gpasswd -a ${USER} docker
$ sudo service docker restart
$ newgrp docker

Test by
$ docker ps

## Install virtualenv
$ sudo apt-get install virtualenv

## Install npm
$ sudo apt-get install npm nodejs-legacy
$ sudo npm install -g configurable-http-proxy


# Install jupyterhub

## Create virtual environment for jupyterhub
$ cd $HOME
$ mkdir workspaces
$ cd workspaces
$ virtualenv -p python3 venv-jh
$ source venv-jh/bin/activate
After this you see a (venv-jh) prompt.

## Create jupyterhub and its dependencies

$ git clone https://github.com/Atigeo/jupyterhub.git
$ cd jupyterhub
$ $ pip3 install -r requirements.txt -e .

## Create notebooks area
$ cd /
$ sudo mkdir notebooks
$ sudo chmod 777 notebooks/


## Configure jupyterhub
$ cd ~/workspaces/jupyterhub
$ mv jupyterhub_config.py jupyterhub_config.py.old
$ cp templates/jupyterhub_config.py.template1 jupyterhub_config.py

Review the settings, using the IP address of your own workstation in place of '192.168.12.109'.

## Install chrome extensions to send Authentication header
google "chrome modheader"
click first link
click "add to chrome"

in the same way, install editthiscookie

To the right of the address bar, there are two new icons.

## Install jupyter/singleuser
$ docker pull jupyter/singleuser

## Run jupyterhub
$ ~/workspaces/jupyterhub/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl

## Get a valid token
Go to jwt.io
Paste in the following payload:
{
  "sub": "xsuser",
  "iv-user": "xsuser",
  "iv-groups": "\"admin\",\"healthcare\"",
  "iss": "xPatterns",
  "admin": true
}
Enter "my secret" in the secret.
Copy the token.

Go to the browser and invoke modheader.
Enter name as Authorization and value as Bearer <token>

Then browse to http://localhost:8000/

Should see green button "Start Server".
Press it and you should see a jupyter notebook.  The address bar should be something like:
http://localhost:8000/jupyter/user/xsuser/tree

## Troubleshooting

In /notebooks there should be a directory xsuser owned by the user that ran jupyterhub.

Do docker ps.
There should be a docker with the name jupyter-xsuser.
There should be a node process running:
  /usr/local/bin/configurable-http-proxy.
There should be a python3 process running:
  /usr/local/bin/jupyterhub-singleuser

To clean up the environment, make sure to kill the node process and to *stop and rm* the docker.
Just stopping is not recommended.  Incomplete cleanup can result in the user's notebook directory having the
wrong owner settings.
This can result in being unable to create notebooks in jupyter.


# Set up kerberos and protected notebooks

To proceed we need access to some of the xpatterns services, such as configuration service,
as well as spark and hdfs.
We will use the aws-secure cluster.

Connect to the AWS vpn now.
Test that you can connect to the configuration service by browsing to:
  http://10.0.2.228:7070/configuration/v1
You should see a page of json (a list of dictionaries)

## Install kerberos
$ sudo apt-get install krb5-user

## Install a keytab
$ cd ~/workspaces/jupyterhub
$ mkdir etc
$ cp templates/jupyterhub.keytab etc/


## Get kerberos key
$ cd ~/workspaces/jupyterhub
$ sudo cp templates/krb5.conf /etc
$ kinit -kt etc/jupyterhub.keytab jupyterhub




## Create refresh-keytab
$ mkdir bin
$ cd bin
$ cp templates/refresh-keytab .
$ chmod +x refresh-keytab

Test by running ./refresh-keytab.
You should see "refreshed keytabs!"

Then in jupyterhub_config.py, put in the path to this file in REFRESH_KEYTABS_PATH as follows:
REFRESH_KEYTABS_PATH='/home/charlesh/workspaces/jupyterhub/bin/refresh-keytab'

# Alter the config file

Edit jupyterhub_config.py
Change  c.DockerSpawner.container_image.
Uncomment the entry as follows.

c.DockerSpawner.container_image = 'docker.staging.xpatterns.com/xpatterns-analytics:89'

Test by running klist.
You should see a single key.


## Create config.properties
$ cd ~/workspaces/jupyterhub/bin
$ cp templates/config_properties .

## Create publish_configs.py
(still in bin)
$ cp templates/publish_configs.py .
$ chmod +x publish_configs.py

Test by running:
python2 publish_configs.py

# If jupyterhub is still running in a window, kill it with ^C.
Then run it again.
$ ~/workspaces/jupyterhub/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl


## Add a cookie
Browse to localhost:8000
You should see an error message.

Using EditThisCookie (installed above) add a cookie
click on the cookie icon in the add-in area
click on + button
Put name field as Authorization
Put anything in Value field
Check Host-only and session
Hit green checkmark

Browse to localhost:8000 and you should see julyter page on the files selection.

Select or open a notebook

!klist
You should see a single kerberos token.

Run this:

from xpatterns.analytics.dal import DAL, HDFSSecureOperations
d = DAL()
d.get_databases()

hdfs = HDFSSecureOperations()
hdfs.check_path('/')



# DevOps setup instructions
https://confluence.life.atigeo.com:8443/display/DEV/Setup+xPatterns+JupyterHub



# Set up token service
$ cd ~/workspaces
$ git clone git@git.life.atigeo.com:cristians/xpatterns-analytics-token-service.git

To build the docker, go to the top level in the project and run
$ python setup.py bdist_wheel
This builds the wheel, which you can install with pip install.
You need to do this inside a 2.7 virtual environment with setuptools at least.

You can install directoy, and you can build a docker file for installing on a production cluster.

## Build the docker
First copy the wheel.
$ cp dist/xpatterns_analytics_token_service-1.0-py2-none-any.whl docker/
$ cd docker
$ docker build -t xpatterns-token-service .
$ check by running "docker images"

This builds a local docker.  Jenkins builds the docker that you are going to deploy, and
it assigns a build number and puts it in the docker repo.

We can run the service using docker/docker_run_script.sh

Check that it is running with docker ps.
Test it by calling ping:
$ curl localhost:16350/ping
Should get pong.

To build with jenkins, use
http://jenkins.life.atigeo.com/job/xpatterns-token-service-docker/
This does not trigger on checkin.

## Configure jupyterhub to use the token service
Go to julyterhub and add
c.JupyterHub.hub_ip = '192.168.0.220'


----------
troubleshooting
Proxy appears to be running at http://*:8000/, but I can't access it (HTTP 403: Forbidden)
    Did CONFIGPROXY_AUTH_TOKEN change?
cchayden@cchayden-XPS-8900:~/workspaces$ ps aux | grep configurable-http
cchayden  2877  0.0  0.0  21292  1088 pts/24   S+   22:58   0:00 grep --color=auto configurable-http
cchayden 25664  0.0  0.1 979528 33948 pts/23   Sl+  Aug05   0:02 node /usr/local/bin/configurable-http-proxy --ip  --port 8000 --api-ip 127.0.0.1 --api-port 8001 --default-target http://192.168.0.220:8081
cchayden@cchayden-XPS-8900:~/workspaces$ kill 25664
----------
troubleshooting
!pwd in a notebook will give the notebook root
It should not be /notebooks, that is something on the outside.
It shold be /home/jovyan/work.
----------

## ​Configure notebooks directory.
In jupyterhub_config.py, add the following:
c.Spawner.notebook_dir = '/home/jovyan/work'


-----------
troubleshooting
If there are permissions problems running the DAL test in the notebook, make sure the kerberos token is valid.
Run refresh-keytab.
In the notebook, run "!klist"
Look for a token.  If none, run kinit.
Check that it is not expired.  If it is expired, make sure refresh-keytab is configured with the right pathname in jupyterhub_config.py

# Rebuild xpatterns analytics docker to add another package.

$ git clone git@git.life.atigeo.com:mpa/xpatterns-analytics.git
$ switch to branch xpatterns6.0
 add new package in setup.py
$ cd analytics_framework
Make sure you are in 2.7 virtual environment. (source venv/bin/activate)
$ python setup.py bdist_wheel

If this fails, you might need to add to the virtual env.
$ sudo apt-get install libcurl4-openssl-dev
$ sudo apt-get install libsasl2-dev
$ sudo apt-get install libfreetype6-dev
$ sudo apt-get install python-dev
$ sudo apt-get install ssh-krb5
$ sudo apt-get install libkrb5-dev

$ cd dist
$ pip install xpatterns_analytics-1.1-py2-none-any.whl
 
## Build the docker
First copy the wheel.
$ cp dist/xpatterns_analytics-1.1-py2-none-any.whl ../docker
$ cd ../docker
$ docker build -t xpatterns-analytics .
$ check by running "docker images"
You should see xpatterns-analytics.

<unclear> Jenkins does not build this docker and place it in the repo.
Need to do this by hand.  (Don't know how.)

Activate the venv-jh
$ jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl
Edit jupyterhub_config.py to use the local xpatterns-analytics docker.
c.DockerSpawner.container_image = 'xpatterns-analytics'

Make sure the token server is running.

Make sure there is no left over jupyterhub.
$ docker ps -a
Look for a process */xpatterns-analytics:*
If there is one, kill it with docker rm <container id>

Then run jupyterhub:
~/workspaces/venv-jh/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl

Check by running a notebook and importing the new package.



​