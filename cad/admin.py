from django.contrib.gis import admin

from .models import *

admin.site.register(Insee, admin.ModelAdmin)


class CadEvalCultAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('insee', 'gr_ss_gr', 'classe', 'nat_cult')
    raw_id_fields = ('insee',)


class CadSectionAdmin(admin.ModelAdmin):
    raw_id_fields = ('insee',)


class CadExonerationAdmin(admin.ModelAdmin):
    list_display = ('fiscalite', 'nat_exo', 'until_year', 'pourcent_exo')


class CadSubfiscAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('prc', 'suf', 'area')


class ParcelOwnerInline(admin.TabularInline):
    model = ParcelOwner
    extra = 1
    exclude = ('created_at', 'updated_at')


class CadPrjUserInline(admin.TabularInline):
    model = CadPrjUser
    extra = 1


class ProspectiveAdmin(admin.ModelAdmin):
    pass


class ProspectiveTranslationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'id')

from ios.admin import IOSGeoAdmin

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

csrf_protect_m = method_decorator(csrf_protect)


class ParcelAdmin(IOSGeoAdmin):
    list_select_related = True
    list_display = ('lieudit', 'num_plan', 'code_edigeo', 'edigeo_area')
    inlines = (ParcelOwnerInline, )


class OwnerAdmin(admin.ModelAdmin):
    inlines = (ParcelOwnerInline, )
    list_display = ('name', 'address', 'phone', 'theme', 'edigeo_area')
    inlines = (CadPrjUserInline, )


class CadLieuditAdmin(admin.ModelAdmin):
    list_select_related = True


admin.site.register(CadEvalCult, CadEvalCultAdmin)
admin.site.register(CadSection, CadSectionAdmin)
admin.site.register(CadExoneration, CadExonerationAdmin)
admin.site.register(CadSubfisc, CadSubfiscAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(CadLieudit, CadLieuditAdmin)
admin.site.register(Prospective, ProspectiveAdmin)
admin.site.register(ProspectiveTranslation, ProspectiveTranslationAdmin)
