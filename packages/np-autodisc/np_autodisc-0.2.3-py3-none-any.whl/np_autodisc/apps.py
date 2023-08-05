# apps.py

from django.apps import AppConfig

class NPAutoDiscoveryConfig(AppConfig):
    name = 'np_autodisc'
    verbose_name = 'Auto Discovery'
    # netbox_min_version = ''
    # netbox_max_version = ''
    required_configuration_settings = []
    default_configuration_settings = {}
#   nav_links = [
#       {
#           'primary': {
#               'name': 'Discovery Requests',
#               'view': 'discoveryrequest_list',
#               'permission': 'view_discoveryrequest'
#           },
#           'add': {
#               'view': 'discoveryrequest_add',
#               'permission': 'add_discoveryrequest'
#           },
#       }
#   ]
