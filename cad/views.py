from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from models import VgOwners
from geoshortcuts.geojson import render_to_geojson
from django.http import HttpResponse


def carto(request):
    return render_to_response(
        'cad/map.html', context_instance=RequestContext(request))


@user_passes_test(lambda u: u.has_perm('staff'))
def ownership(request):
    qs = VgOwners.objects.filter(activated=True)
    json = render_to_geojson(
        qs,
        projection=4326,
        properties=[
            ('name', 'name'), ('theme', 'theme'), ('activated', 'activated')]
    )

    return HttpResponse(json, content_type=u'application/json')
