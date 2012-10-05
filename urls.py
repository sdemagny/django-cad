from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cad.views',
    url(r'^services/cad$', 'carto', name='cad_carto'),
    url(r'^layers/cad/parcels$', 'parcels', name='cad_parcels')
)
