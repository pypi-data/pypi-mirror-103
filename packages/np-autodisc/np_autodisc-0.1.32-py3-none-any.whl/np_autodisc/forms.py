# forms.py

from django import forms

from dcim.models import DeviceRole, Platform, Site
from utilities.forms import (
    add_blank_choice, APISelect, APISelectMultiple, BootstrapMixin, StaticSelect2
)

from np_autodisc.np_transitions.forms import FilterChoiceField

from np_autodisc.constants import REQUEST_NAPALM_DRIVER_CHOICES, REQUEST_STATUS_CHOICES
from np_autodisc.models import DiscoveryRequest


#
# DiscoveryRequest
#

class DiscoveryRequestFilterForm(BootstrapMixin, forms.Form):
#    def __init__(self, *args, **kwargs):
#        return super().__init__(*args, **kwargs)

    model = DiscoveryRequest
    field_order = ['q', 'status', 'prefix', 'update_existing', 'platform', 'site']
    q = forms.CharField(
        required = False,
        label = 'Search'
    )
    status = forms.ChoiceField(
        choices = add_blank_choice(REQUEST_STATUS_CHOICES),
        required = False,
        widget = StaticSelect2()
    )
    platform = FilterChoiceField(
        queryset = Platform.objects.all(),
        to_field_name = 'slug',
        widget = APISelectMultiple(
            api_url = '/api/dcim/platforms/',
#            value_field = 'slug',
        )
    )
    site = FilterChoiceField(
        queryset = Site.objects.all(),
        to_field_name = 'slug',
        widget = APISelectMultiple(
            api_url = '/api/dcim/sites/',
#            value_field = 'slug'
        )
    )
    device_role = FilterChoiceField(
        queryset = DeviceRole.objects.all(),
        to_field_name = 'slug',
        widget = APISelectMultiple(
            api_url = '/api/dcim/device-roles/',
#            value_field = 'slug'
        )
    )


class DiscoveryRequestForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = DiscoveryRequest
        fields = [
            'prefix', 'update_existing', 'platform', 'site', 'device_role'
        ]
        widgets = {
            'platform': APISelect(
                api_url = '/api/dcim/platforms'
            ),
            'site': APISelect(
                api_url = '/api/dcim/sites/'
            ),
            'device_role': APISelect(
                api_url = '/api/dcim/device-roles/'
            ),
        }
        help_texts = {
            'prefix': 'CIDR prefix to scan for discovery',
            'site': 'Site in which to look for and create new devices',
            'update_existing': 'Update existing devices if they already exist in NetBox',
            'device_role': 'Device role to use for new and updated devices',
            'platform': 'Device platform which contains the applicable NAPALM driver',
        }
