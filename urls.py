from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cad.views',
    url(r'^services/foncier$', 'carto', name='cad_carto'),
    url(r'^layers/cad/prc$', 'prc_layer', name='cad_prc_layer')
)
