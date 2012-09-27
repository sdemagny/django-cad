from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from models import CadPrc
from geoshortcuts.geojson import render_to_geojson
from django.http import HttpResponse


def carto(request):
    return render_to_response('services/cad_service_map.leaflet.html', context_instance=RequestContext(request))


@user_passes_test(lambda u: u.has_perm('staff'))
def prc_layer(request):
    qs = CadPrc.objects.all()

    json = render_to_geojson(qs, projection=4326, properties=['num_plan'])
    return HttpResponse(json, mimetype=u'application/json')
