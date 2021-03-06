Preliminaries
=============

Jupyterhub is a python3 project, and has a matching virtual environment.
Token server and xpatterns-analytics are python 2.7 projects, and have their own virtual environments.
These instructions assume a pristene developer machine.

Find out what machine I am on
-----------------------------
    $ uname -a
    Linux CharlesH-HP8300-Ubuntu1604 4.4.0-31-generic #50-Ubuntu SMP Wed Jul 13 00:07:12 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux

    $ python3 --version
    Python 3.5.2
This must be 3.3 or above

Install docker
--------------
    $ sudo apt-get install docker.io
    $ docker ps

If this gives a permission error, then do the following.

    $ sudo gpasswd -a ${USER} docker
    $ sudo service docker restart
    $ newgrp docker

Test by

    $ docker ps

Install virtualenv
------------------
    $ sudo apt-get install virtualenv

Install npm
-----------
    $ sudo apt-get install npm nodejs-legacy
    $ sudo npm install -g configurable-http-proxy


Install jupyterhub
==================

We are going to install everything into $HOME/workspaces.

Create virtual environment for jupyterhub
-----------------------------------------
    $ cd $HOME
    $ mkdir workspaces
    $ cd workspaces
    $ virtualenv -p python3 venv-jh
    $ source venv-jh/bin/activate
After this you see a (venv-jh) prompt.

Create jupyterhub and its dependencies
--------------------------------------
    $ git clone https://github.com/Atigeo/jupyterhub.git
    $ cd jupyterhub
    $ pip3 install -r requirements.txt -e .

Create notebooks area
---------------------
    $ cd /
    $ sudo mkdir notebooks
    $ sudo chmod 766 notebooks/


Configure jupyterhub
--------------------
    $ cd ~/workspaces/jupyterhub
    $ mv jupyterhub_config.py jupyterhub_config.py.old
    $ cp templates/jupyterhub_config.py.template jupyterhub_config.py


Review the settings, using the IP address of your own workstation in place of '192.168.12.109'.

At this stage, configure the singleuser docker by enabling the commented-out configuration:

    c.DockerSpawner.container_image = 'jupyter/singleuser'

and comment out the other one.

Install chrome extensions to send Authentication header
-------------------------------------------------------
* Google "chrome modheader".
* Click first link
* Click "add to chrome"

In the same way, install ```editthiscookie```.

To the right of the address bar, there are two new icons.

Install jupyter/singleuser
--------------------------
    $ docker pull jupyter/singleuser

## Run jupyterhub
    $ ~/workspaces/jupyterhub/bin/jupyterhub -f jupyterhub_config.py --no-ssl

Run jupyterhub
--------------
    $ ~/workspaces/venv-jh/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl


Create a valid token
--------------------
Go to jwt.io

Paste in the following payload:
```
{
  "sub": "xsuser",
  "iv-user": "xsuser",
  "iv-groups": "\"admin\",\"healthcare\"",
  "iss": "xPatterns",
  "admin": true
}
```

Enter "my secret" in the secret.

You can put in a different user, as long as you put it in both places.

Copy the token.

Go to the browser and invoke modheader (one of the extensions you installed).
Enter name as "Authorization" and value as "Bearer <token>"

Then browse to http://localhost:8000/

You should see green button "Start Server".
Press it and you should see a jupyter notebook.  The address bar should be something like:

    http://localhost:8000/jupyter/user/xsuser/tree

Troubleshooting
---------------

In /notebooks there should now be a directory xsuser owned by the user that ran jupyterhub.

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

Set up kerberos and protected notebooks
---------------------------------------

To proceed we need access to some of the xpatterns services, such as configuration service, as well as spark and hdfs.
We will use the aws-secure cluster.

Connect to the AWS vpn now.

Test that you can connect to the configuration service by browsing to:

    http://10.0.2.228:7070/configuration/v1

You should see a page of json (a list of dictionaries)

Install kerberos
----------------
    $ sudo apt-get install krb5-user


Install a keytab
----------------
    $ cd ~/workspaces/jupyterhub
    $ mkdir etc
    $ cp templates/jupyterhub.keytab etc/


Get kerberos key
----------------

    $ cd ~/workspaces/jupyterhub
    $ sudo cp templates/krb5.conf etc/
    $ KRB5_CONFIG=etc/krb5.conf kinit -kt etc/jupyterhub.keytab jupyterhub



Create refresh-keytab
---------------------

    $ cd ~/workspaces/jupyterhub
    $ cp templates/refresh-keytab bin/
    $ chmod +x bin/refresh-keytab

Test by running bin/refresh-keytab.
You should see ```refreshed keytabs!```

Test by running klist.

You should see a single key.


Then in ```jupyterhub_config.py```, put in the path to this file in REFRESH_KEYTABS_PATH as follows:

    REFRESH_KEYTABS_PATH='/home/<your login>/workspaces/jupyterhub/bin/refresh-keytab'

Be sure to change the path as approppriate.

Alter the config file
---------------------
Pull the xpatterns-analytics docker.  Use the latest tag number.

    $ docker pull docker.staging.xpatterns.com/xpatterns-analytics:91

Edit ```jupyterhub_config.py```

Change  ```c.DockerSpawner.container_image.```

Comment out the existing entry, and uncomment the entry as follows:

    c.DockerSpawner.container_image = 'docker.staging.xpatterns.com/xpatterns-analytics:91'

The version number (91) is normally the latest one in Jenkins.

Publish Configuration
=====================
This pushes configuration values up to the configuration service.
The values come from config.properties.  Make sure these are the
properties you want.  There are many server names and IP addresses
in this file.

Create config.properties
------------------------
    $ cd ~/workspaces/jupyterhub
    $ cp templates/config.properties bin/

Create publish_configs.py
-------------------------
    $ cp templates/publish_configs.py bin/
    $ chmod +x bin/publish_configs.py

Edit publish_configs.py to put in the IP address of the connect box.
If you are setting this up on a local dev box, it is easiest to point to
a connect box on an existing cluster.  Be sure to connect to the appropriate
VPN if you do this.

Change CONNECT_BOX_IP as follows:

    CONNECT_BOX_IP = '10.0.2.228'


Test by running:

    $ cd bin
    $ python publish_configs.py

The result shoould show a status code of 200.


If jupyterhub is still running in a window, kill it with ^C.

Then run it again.

    $ ~/workspaces/jupyterhub/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl


Add a cookie
------------
Browse to localhost:8000

You should see an error message.

Using EditThisCookie (installed above) add the cookie "Authorization" with any value inside it (make it a
session cookie so it doesn't go away). Otherwise, some javascript is
going to notice that you're not having an active webseal cookie and will
redirect you to the logout_path in the jupyterhub_config (which is usually
/pkmslogout).

## Troubleshooting
If the server gets an exception trying to index a string with the index 'username'
that can mean that the authenticator class is incorrect.  This can happen when
the config file does not load correctly.  Check the pathname in the -f argument of jupyterhub.

## What is this ??

    name: jupyter-hub-token-datas1
    value: 2|1:0|10:1470319260|24:jupyter-hub-token-datas1|44:ZTI0YmVhN2E4YjNhNDc2YWEyMmU2ZGViMmUxN2JkZDY=|1b9ea97df512a3ace6e21b2446340d380ae85b8fb9ea91e39fc36bf27b14c924
    Check Host Only
    Click on the check.

## Change the token
Do something to change the token.

Hit green checkmark.

Browse to localhost:8000 and you should see jupyter page on the files screen.

Select to open a notebook or create a new one.

Enter into a notebook cell and execute:

    !klist

You should see a single kerberos token.

Run these smoke tests.  Run each of these in a cell.

## Analytics Library
    # DAL smoke test
    d = DAL()
    print d.get_databases()
    d.close_connection()
    
Expected output:
```
['atigeo', 'audit', 'dataa1chestie', 'default', 'delta', 'demo', 'dictionaries', 'qa_db', 'rbi', 'sample_hive', 'test', 'test_hue_deployment', 'testcosmin', 'testcosmin2', 'testcristis', 'tpcds_bin_partitioned_orc_10', 'tpcds_text_10', 'uci', 'usecasedb']
```

## HDFS
    # HDFS smoke test
    hdfs = HDFSSecureOperations()
    hdfs.check_path('/')
    
Expected output:
```
True
```

## Livy
    # Livy smoke test
    lv = LivyOperations()
    print lv.execute_statement('print "hello"')
    print lv.execute_statement(
    """
        import random
        NUM_SAMPLES = 100000
        def sample(p):
          x, y = random.random(), random.random()
          return 1 if x*x + y*y < 1 else 0

        count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
        print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)
    """)
    lv.close()

Expected output:
```
{u'status': u'ok', u'execution_count': 1, u'data': {u'text/plain': u'hello'}}
{u'status': u'ok', u'execution_count': 2, u'data': {u'text/plain': u'Pi is roughly 3.156640'}}
In [4]:

```

Troubleshooting
---------------

### Server State Dead
If you get an error creating ```LivyOperations``` and you see a message
indicating that the server state is "dead" then you need to investigate
the xpatterns-livy service.

Log in to the connect server and get the logs:

    $ docker logs xpatterns-livy
    
You might see an error backtrace in the logs.

If you see a permittions message about accessing '/user' then this
is talking about a permissions problem in hdfs.  If, for instance, you are
logged in to the xpatterns console as xiengineer, then the error message
would refer to permissions for user 'xiengineer'.  

Check the hadoop permissions:

    $ hadoop fs -ls /user
    
If you do not see a directory for 'xiengineer', then you need to make one.

    $ hadoop fs -mkdir /user/xiengineer
    $ hadoop fs -chown xiengineer /user/xiengineer
    
Also check that the permissions for the new directory is 750.


### Connection Error
If you get an error creating LivyOperations with a ConnectionError for
trying to rech port 8998, this means that the livy server is not running.

If the docker is stopped (if you see it with ```docker ps -a`) then you can simply
start if (```docker start xpatterns-livy```).

If not, you can restart using the normal start mechanism.

    $ cd /opt/atigeo/xpatterns-docker-compose
    $ sudo ./xpatterns.sh init



Set up token service
====================
The token service is a freestanding service running on the connect machine.
Jupyterhub posts valid tokens to it, and apps can get these tokens if they
present a valid (but possibly expired) token from the same user.

    $ cd ~/workspaces
    $ virtualenv venv

Make sure you have the (venv) prompt.

    $ git clone git@git.life.atigeo.com:cristians/xpatterns-analytics-token-service.git

Enter the project:

    $ cd xpatterns-analytics
    $ source setup

Build the docker:

    $ bin/build-docker

This builds the wheel, which you can install with pip install.


You can install directly, and you can build a docker file for installing on a production cluster.

Let's build and install the docker.

Build the docker
----------------
This builds a local docker.

    $ cd ~/workspaces/xpatterns-analytics-token-service
    $ bin/build-docker

Test by running

    $ docker images

You should see xpatterns-analytics-token-service docker.

Later on, we will have Jenkins build the docker that you are going to
deploy, and it assigns a build number and puts it in the docker repo.

We can run the service locally using:

    $ build/run-docker

Test by running

    $ docker ps

This should show a running xpatterns-token-service.

Test it by calling ping:

    $ curl localhost:16350/ping

Should get pong.

To build with jenkins, go to

    http://jenkins.life.atigeo.com/job/xpatterns-token-service-docker/

This does not trigger on checkin.
Click on "Build With Parameters" to build it.

Configure jupyterhub to use the token service
---------------------------------------------
Go to jupyterhub_config.py and add

    c.JupyterHub.hub_ip = <your IP address>

This should the IP of the machine you are running on.




Troubleshooting
---------------
### If you get a message like this:
    Proxy appears to be running at http://*:8000/, but I can't access it (HTTP 403: Forbidden)
        Did CONFIGPROXY_AUTH_TOKEN change?

Do this:

    $ ps aux | grep configurable-http
```
cchayden  2877  0.0  0.0  21292  1088 pts/24   S+   22:58   0:00 grep --color=auto configurable-http
cchayden 25664  0.0  0.1 979528 33948 pts/23   Sl+  Aug05   0:02 node /usr/local/bin/configurable-http-proxy --ip  --port 8000 --api-ip 127.0.0.1 --api-port 8001 --default-target http://192.168.0.220:8081
```
    $ kill 25664



### If notebooks are not persistent

Find the notebook root:

    !pwd


It should *not* be ```/notebooks```, that is something on the outside.

It should be ```/home/jovyan/work```.

Make sure you configure the notebooks directory:

In ```jupyterhub_config.py```, add the following:

    c.Spawner.notebook_dir = '/home/jovyan/work'


### Permissions problems using DAL from the notebook

If there are permissions problems running the DAL test in the notebook, make sure the kerberos token is valid.
Run ```refresh-keytab```.

In the notebook, run

    !klist

Look for a token.  If none, run ```kinit``` (as shown above).
Check that the token is not expired.
If it is expired, make sure ```refresh-keytab``` is configured with the 
right pathname in ```jupyterhub_config.py``` and that it is running.

Rebuild xpatterns-analytics docker to add another package
=========================================================

Notebook users can only import packages that you have configured into it.
The project xpatterns-analytics creates a library that gets incorporated into it.
You may need to do this stuff before you build jupyterhub.


    $ git clone git@git.life.atigeo.com:mpa/xpatterns-analytics.git
    $ git checkout xpatterns6.0
    $ cd xpatterns-analytics
    $ source setup

Add the new package in into setup.py.
Open ```analytics_framework/setup.py``` and add the package name
to the list ```install_requires```.

Make sure you are in 2.7 virtual environment. (prompt: (venv)).
Then build the wheel.

    $ bin/build-wheel


If this fails, you might need to add to the virtual environment venv.

    $ sudo apt-get install libcurl4-openssl-dev
    $ sudo apt-get install libsasl2-dev
    $ sudo apt-get install libfreetype6-dev
    $ sudo apt-get install python-dev
    $ sudo apt-get install ssh-krb5
    $ sudo apt-get install libkrb5-dev

    $ cd dist
    $ pip install xpatterns_analytics-1.1-py2-none-any.whl

Build the docker
----------------
    $ bin/build-docker

Check by running

    $ docker images

You should see xpatterns-analytics.

Jenkins builds the docker when you push to git.

Make sure you are in venv.

If necessary, create a window and do:

    $ cd ~workspaces/xpatterns-analytics
    $ source setup


Edit ```jupyterhub_config.py``` to use the local xpatterns-analytics docker.

    c.DockerSpawner.container_image = 'xpatterns-analytics'

Make sure the token server is running.

Make sure there is no leftover jupyterhub process.

    $ docker ps -a

Look for a process ```*/xpatterns-analytics:*```
If there is one, kill it with ```docker rm <container id>```.

Then run jupyterhub:

    ~/workspaces/venv-jh/bin/jupyterhub -f ~/workspaces/jupyterhub/jupyterhub_config.py --no-ssl


Check by running a notebook and importing the new package.



​# DevOps setup instructions"

https://confluence.life.atigeo.com:8443/display/DEV/Setup+xPatterns+JupyterHub
