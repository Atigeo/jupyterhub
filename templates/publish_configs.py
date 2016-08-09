
# this updates the xpatterns config service, loading the values in config.properties
#
# change CONNECT_BOX_IP to point to the config service
# If the kerberos secret changes, this will fail.
# Go to jwt.io and make a new token, then paste it here.
# See also the use of the Authorization header to make a request with JWT token.

CONNECT_BOX_IP = '10.91.154.60'
CONFIG_SERVICE_URL = 'http://'+ CONNECT_BOX_IP + ':7070/configuration/v1'
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYXRhczEiLCJpdi11c2VyIjoiZGF0YXMxIiwiaXYtZ3JvdXBzIjoiXCJhZG1pblwiLFwiaGVhbHRoY2FyZVwiIiwiaXNzIjoieFBhdHRlcm5zIiwiYWRtaW4iOnRydWV9.ix_79jYQbWxYgCYLg8H2Ab5GShmpXudD6YOEDG3Z-g0'
import requests
def publish_configs():
    files={'properties':open('config.properties','rb')}
    url = CONFIG_SERVICE_URL + '/appName/profile/?appName=xpatternsAnalytics&profile=default'
    headers = {"Authorization": "Bearer " + token}

    r = requests.post(url=url,files=files, headers=headers)
    print url,'STATUS_CODE: ',r.status_code
publish_configs()
