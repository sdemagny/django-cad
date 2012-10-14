from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from models import Parcel
from geoshortcuts.geojson import render_to_geojson
from django.http import HttpResponse


def carto(request):
    return render_to_response('cad_map.html', context_instance=RequestContext(request))


@user_passes_test(lambda u: u.has_perm('staff'))
def parcels(request):
    qs = Parcel.objects.select_related().all()
    json = render_to_geojson(qs, projection=4326, properties=['num_plan', 'code_edigeo', 'lieudit'])

    return HttpResponse(json, mimetype=u'application/json')


from django.core.servers.basehttp import FileWrapper
import os


def ng_list(request):
    filename = os.path.abspath(os.path.dirname(__file__) + '/static/js/ng/partials/cad.list.html')
    wrapper = FileWrapper(file(filename))

    return HttpResponse(wrapper)
