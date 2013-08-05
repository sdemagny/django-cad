from django.conf.urls import patterns, url, include
from tastypie.api import Api
from cad.api import ParcelResource, LieuditResource,\
    InseeResource, SectionResource

a = Api(api_name='a')
a.register(InseeResource())
a.register(SectionResource())
a.register(LieuditResource())
a.register(ParcelResource())

urlpatterns = patterns(
    'cad.views',
    url(r'^services/cad$', 'carto', name='cad_carto'),
    url(r'^services/cad/api/', include(a.urls)),
    url(r'^layers/cad/ownership$', 'ownership', name='cad_ownership'),
)
