from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.contrib.auth.decorators import user_passes_test
from models import VgOwners
from geoshortcuts.geojson import render_to_geojson
from django.http import HttpResponse
from django.contrib.gis.geos import Polygon
import ast
from django.views.decorators.gzip import gzip_page


def carto(request):
    return render_to_response(
        'cad/map.html', context_instance=RequestContext(request))


# @todo Test this
#@user_passes_test(lambda u: u.has_perm('staff'))
@gzip_page
def ownership(request):

    # Get the current user form the request
    # @todo Move this filter to model
    qs = VgOwners.objects.filter(activated=True)
    bbox = ast.literal_eval(
        '(%s)' % (request.GET.get('bbox', '-160, -89, 160, 89')))
    polygon = Polygon.from_bbox(bbox)
    polygon.set_srid(4326)
    polygon.transform(900913)
    json = render_to_geojson(
        qs,
        projection=4326,
        properties=[('name', 'name'), ('theme', 'theme')],
        #extent=polygon
    )

    return HttpResponse(json, content_type=u'application/json')
