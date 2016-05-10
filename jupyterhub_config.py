c.JupyterHub.spawner_class= 'dockerspawner.dockerspawner.DockerSpawner'
c.DockerSpawner.container_image = 'radu/xpatterns-jupyter'
c.DockerSpawner.hub_ip_connect = '192.168.13.45'
c.JupyterHub.hub_ip = '192.168.13.45'
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.authenticator_class = 'jupyterhub.jwtauth.JWTHeaderAuthenticator'
