c.JupyterHub.spawner_class = 'dockerspawner.dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/singleuser'
c.DockerSpawner.hub_ip_connect = '10.3.22.99'
c.JupyterHub.hub_ip = '10.3.22.99'
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.authenticator_class = 'jupyterhub.jwtauth.JWTHeaderAuthenticator'
c.JWTHeaderAuthenticator.token_service_url = 'http://10.3.22.99:16350/token'
c.DockerSpawner.volumes = {'/notebooks/{username}': '/home/jovyan/work'}

c.DockerSpawner.keytab_path = '/usr/local/keytabs'
c.DockerSpawner.extra_start_command = '/bin/bash /usr/local/init_container.sh'

c.Spawner.environment = {'XPATTERNS_KEYTAB_PATH': c.DockerSpawner.keytab_path + '/alinb.keytab',
                         'XPATTERNS_KEYTAB_REFRESH_PATH': c.DockerSpawner.keytab_path + '/refresh_keytab.sh',
                         'XPATTERNS_KEYTAB_USER': 'alinb@STAGING.XPATTERNS.COM',
                         'KRB_REALM':  'STAGING.XPATTERNS.COM',
                         'KRB_SERVER': '10.0.2.181',
                         'TOKEN_URL': 'http://10.0.2.197:16350',
                         'CONFIG_URL': 'http://10.0.2.197:7070/configuration/v1'}

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

c.DockerSpawner.extra_hosts = {
    '10.0.2.228': 'xpatterns-admin xpatterns-foundation xpatterns-workflow xpatterns-rabbitmq xpatterns-sjr secluster-connect secluster-connect.xpatterns.com connect.staging.xpatterns.com xpatterns-publish xpatterns-ingestion',
    '10.0.2.122': 'secluster-master.staging.xpatterns.com secluster-master',
    '10.0.2.45': 'xpatterns-cassandra secluster-node1.staging.xpatterns.com secluster-node1',
    '10.0.2.46': 'secluster-node2.staging.xpatterns.com secluster-node2',
    '10.0.2.47': 'secluster-node3.staging.xpatterns.com secluster-node3'}

c.JupyterHub.base_url = '/jupyter'
# c.DockerSpawner.copy_host_file = True
# c.DockerSpawner.extra_host_config = {'network_mode': 'host'}
# c.DockerSpawner.network_name = 'host'
# Set the log level by value or name.
c.JupyterHub.log_level = 'DEBUG'

# Enable debug-logging of the single-user server
c.Spawner.debug = True
# c.DockerSpawner.use_internal_ip = True
