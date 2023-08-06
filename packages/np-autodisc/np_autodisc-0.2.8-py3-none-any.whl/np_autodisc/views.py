# views.py

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

# from extras.views import ObjectDeleteView, ObjectEditView, ObjectListView
from netbox.views import generic

from np_autodisc import filters, forms, tables
from np_autodisc.models import DiscoveryRequest


#
# DiscoveryRequests
#

class DiscoveryRequestListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = 'np_autodisc.view_discoveryrequest'
    queryset = DiscoveryRequest.objects.all()
    filter = filters.DiscoveryRequestFilter
    filter_form = forms.DiscoveryRequestFilterForm
    table = tables.DiscoveryRequestTable
    template_name = 'np_autodisc/discoveryrequest_list.html'

class DiscoveryRequestView(PermissionRequiredMixin, View):
    permission_required = 'np_autodisc.view_discoveryrequest'

    def get(setlf, request, pk):
        discoveryrequest = get_object_or_404(DiscoveryRequest, pk = pk)
        return render(request, 'np_autodisc/discoveryrequest.html', {
            'discoveryrequest': discoveryrequest,
        })

class DiscoveryRequestCreateView(PermissionRequiredMixin, generic.ObjectEditView):
    permission_required = 'np_autodisc.add_discoveryrequest'
    model = DiscoveryRequest
    queryset = DiscoveryRequest.objects.all()
    model_form = forms.DiscoveryRequestForm
    template_name = 'np_autodisc/discoveryrequest_edit.html'
    default_return_url = 'np_autodisc:discoveryrequest_list'

class DiscoveryRequestDeleteView(PermissionRequiredMixin, generic.ObjectDeleteView):
    permission_required = 'np_autodisc.delete_discoveryrequest'
    model = DiscoveryRequest
    default_return_url = 'np_autodisc:discoveryrequest_list'
