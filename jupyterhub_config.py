c.JupyterHub.spawner_class = 'dockerspawner.dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/singleuser'
c.DockerSpawner.hub_ip_connect = '10.3.22.99'
c.JupyterHub.hub_ip = '10.3.22.99'
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.authenticator_class = 'jupyterhub.jwtauth.JWTHeaderAuthenticator'
c.JWTHeaderAuthenticator.token_service_url = 'http://10.3.22.99:16350/token'
c.DockerSpawner.volumes = {'/notebooks/{username}': '/home/jovyan/work'}
c.DockerSpawner.extra_start_command = '/bin/bash /keytabs/refresh_keytab.sh'
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

c.Spawner.environment = {'XPATTERNS_TEST_VAR': 'CRISTOS'}

c.JupyterHub.base_url = '/jupyter'
# c.DockerSpawner.copy_host_file = True
# c.DockerSpawner.extra_host_config = {'network_mode': 'host'}
# c.DockerSpawner.network_name = 'host'
# Set the log level by value or name.
c.JupyterHub.log_level = 'DEBUG'

# Enable debug-logging of the single-user server
c.Spawner.debug = True
# c.DockerSpawner.use_internal_ip = True
