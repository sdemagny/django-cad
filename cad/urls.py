from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cad.views',
    url(r'^services/cad$', 'carto', name='cad_carto'),
    url(r'^services/data/cad/articles.json$', 'parcels'),
    url(r'^layers/cad/parcels$', 'parcels', name='cad_parcels'),
    url(r'^services/partials/cad.list.html', 'ng_list')
)
