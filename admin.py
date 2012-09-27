from django.conf.urls import patterns, url, include
from django.contrib.gis import admin

from models import *

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

class CadPrjPrcInline(admin.TabularInline):
    model = CadPrjPrc
    extra = 1
    exclude = ('created_at', 'updated_at')

class CadPrjUserInline(admin.TabularInline):
    model = CadPrjUser
    extra = 1

class CadProspectiveTranslationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'id')

class CadPrcAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('lieudit', 'num_plan', 'code_edigeo', 'edigeo_area')
    inlines = (CadPrjPrcInline, )

class CadPrjAdmin(admin.ModelAdmin):
    inlines = (CadPrjPrcInline, )
    list_display = ('name', 'address', 'phone', 'theme', 'edigeo_area')
    inlines = (CadPrjUserInline, )

class CadLieuditAdmin(admin.ModelAdmin):
    list_select_related = True

admin.site.register(CadEvalCult, CadEvalCultAdmin)
admin.site.register(CadSection, CadSectionAdmin)
admin.site.register(CadExoneration, CadExonerationAdmin)
admin.site.register(CadSubfisc, CadSubfiscAdmin)
admin.site.register(CadPrc, CadPrcAdmin)
admin.site.register(CadPrj, CadPrjAdmin)
admin.site.register(CadProspectiveTranslation, CadProspectiveTranslationAdmin)
admin.site.register(CadLieudit, CadLieuditAdmin)
