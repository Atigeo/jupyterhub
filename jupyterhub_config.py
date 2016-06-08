c.JupyterHub.spawner_class = 'dockerspawner.dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'jupyter/singleuser'
c.DockerSpawner.hub_ip_connect = '10.3.22.99'
c.JupyterHub.hub_ip = '10.3.22.99'
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.authenticator_class = 'jupyterhub.jwtauth.JWTHeaderAuthenticator'
c.JWTHeaderAuthenticator.token_service_url = 'http://10.3.22.99:16350/token'
c.DockerSpawner.volumes = {'/notebooks/{username}': '/notebooks'}
