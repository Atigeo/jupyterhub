# The connect server is used in several places.
# It is the server that is running jupyterhub
#connect_server = '192.168.0.220' 
connect_server = '192.168.12.109'

c.JupyterHub.spawner_class = 'dockerspawner.dockerspawner.DockerSpawner'
# generic singleuser docker
# to specify a tag, append it after colon
#c.DockerSpawner.container_image = 'jupyter/singleuser'   

# the xpatterns-analytcs version from the docker repo
c.DockerSpawner.container_image = 'docker.staging.xpatterns.com/xpatterns-analytics:91'
# local build of xpatterns-analytics
#c.DockerSpawner.container_image = 'xpatterns-analytics'

# the next two are normally the same
# it is the IP of the machine where jupyterjub is installed
c.DockerSpawner.hub_ip_connect = connect_server
c.JupyterHub.hub_ip = connect_server

# leave this True
c.JupyterHub.cleanup_proxy = True
# leave this -- it is the authenticator class that gets the JWT token from the header
c.JupyterHub.authenticator_class = 'jupyterhub.jwtauth.JWTHeaderAuthenticator'

# Comment this out when running in development
# Include it when actually running the token service.
c.JWTHeaderAuthenticator.token_service_url = 'http://{}:16350/token'.format(connect_server)

# This is an outside : inside pair used for notebook storage
# username is populated from the JWT token
# /notebooks needs to be 755 
c.Spawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.volumes = {'/notebooks/{username}': c.Spawner.notebook_dir}

# don't know what this is for
#c.DockerSpawner.keytab_path = '/usr/local/keytabs'

# this is executed inside the container at creation or start
c.DockerSpawner.extra_start_command = '/bin/bash /usr/local/init_container.sh'

# this is executed inside the container at creation or start
REFRESH_KEYTABS_PATH='/home/charlesh/workspaces/jupyterhub/bin/refresh-keytab'
c.DockerSpawner.extra_system_start_command = '/bin/bash ' + REFRESH_KEYTABS_PATH

# These settings define how the application interacts with kerberos.
# They are normally pointed to an actual cluster, even when running locally in development mode.
# The ones here point to AWS secure cluster.
# Make sure you are running a VPN that allows access to these IP addresses.

# KRB_SERVER is kerberos server
# TOKEN_URL is URL of a service that refreshes the JWT tokens
# This server is at http://git.life.atigeo.com/cristians/xpatterns-analytics-token-service
# It must be running on the connect server
# CONFIG_UTL is the xpatterns foundation configuration service
c.Spawner.environment = {
                         'KRB_REALM':  'STAGING.XPATTERNS.COM',
                         'KRB_SERVER': '10.0.2.122',
                         'TOKEN_URL': 'http://10.0.2.228:16350',
                         'CONFIG_URL': 'http://10.0.2.228:7070/configuration/v1'}


# comment out when doing development locally -- they will log you out otherwise
# Restore when running i production

#c.JWTHeaderAuthenticator.extra_logout_location = '/pkmslogout'
#c.JWTHeaderAuthenticator.xpatterns_cookie_name = 'xpatternsLink'

# These hosts are added to /etc/hosts inside the docker when it is started
# Configure as appropriate to the cluster were this is deployed.

# Here are a few examples for different clusters.
# The last one f these will be used.
c.DockerSpawner.extra_hosts = {
    '10.0.2.197': 'xpatterns-admin	xpatterns-foundation xpatterns-workflow xpatterns-rabbitmq connect.staging.xpatterns.com xpatterns-ingestion',
    '54.201.104.32': 'docker.staging.xpatterns.com',
    '10.0.2.196': 'xpatterns-cassandra',
    '10.0.2.70': 'scdh56-master.staging.xpatterns.com scdh56-master',
    '10.0.2.71': 'scdh56-slave1.staging.xpatterns.com scdh56-slave1',
    '10.0.2.72': 'scdh56-slave2.staging.xpatterns.com scdh56-slave2',
    '10.0.2.73': 'scdh56-slave3.staging.xpatterns.com scdh56-slave3'
}

c.DockerSpawner.extra_hosts = {
    '10.91.154.8': 'connect1.dev.ydcloud.net  connect1 xpatterns-workflow xpatterns-ingestion xpatterns-publish',
    '10.91.154.9': 'spark-master.dev.ydcloud.net  spark-master',
    '10.91.154.10': 'spark-slave1.dev.ydcloud.net  spark-slave1 xpatterns-cassandra',
    '10.91.154.11': 'spark-slave2.dev.ydcloud.net  spark-slave2',
    '10.91.154.12': 'spark-slave3.dev.ydcloud.net  spark-slave3'}

# This is the last one, that is actually used.
c.DockerSpawner.extra_hosts = {
    '10.0.2.228': 'xpatterns-admin xpatterns-foundation xpatterns-workflow xpatterns-rabbitmq xpatterns-sjr secluster-connect secluster-connect.xpatterns.com connect.staging.xpatterns.com xpatterns-publish xpatterns-ingestion',
    '10.0.2.122': 'secluster-master.staging.xpatterns.com secluster-master',
    '10.0.2.45': 'xpatterns-cassandra secluster-node1.staging.xpatterns.com secluster-node1',
    '10.0.2.46': 'secluster-node2.staging.xpatterns.com secluster-node2',
    '10.0.2.47': 'secluster-node3.staging.xpatterns.com secluster-node3'}

# this is the service root -- do not change
c.JupyterHub.base_url = '/jupyter'

# Set the log level by value or name.
#c.JupyterHub.log_level = 'DEBUG'

# Enable debug-logging of the single-user server
c.Spawner.debug = True

# This is used to decode the JWT token in the token service.
c.JWTHeaderAuthenticator.secret_key = 'my secret'
