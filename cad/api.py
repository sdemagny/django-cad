from tastypie.resources import ModelResource
from tastypie import fields
from cad.models import Parcel, Lieudit, Insee, Section


class InseeResource(ModelResource):
    class Meta:
        queryset = Insee.objects.all()
        resource_name = 'insee'


class SectionResource(ModelResource):
    insee = fields.ForeignKey(InseeResource, 'insee')

    class Meta:
        queryset = Section.objects.all()
        resource_name = 'section'


class LieuditResource(ModelResource):
    section = fields.ForeignKey(SectionResource, 'section')

    class Meta:
        queryset = Lieudit.objects.all()
        resource_name = 'lieudit'


class ParcelResource(ModelResource):
    lieudit = fields.ForeignKey(LieuditResource, 'lieudit')

    class Meta:
        queryset = Parcel.objects.all()
        resource_name = 'parcel'
        excludes = ['the_geom', 'gid']
