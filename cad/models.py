from django.contrib.gis.db import models
from guard.models import SfGuardUser
from frt.models import FrtSprf


class Insee(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = u'insee'

    def __unicode__(self):
        return self.name


class CadEvalCult(models.Model):
    insee = models.ForeignKey(Insee)
    gr_ss_gr = models.CharField("GR SS GR", max_length=2)
    classe = models.CharField(max_length=2)
    nat_cult = models.CharField(max_length=25)

    class Meta:
        db_table = u'cad_eval_cult'
        verbose_name = "Culture evaluation"

    def __unicode__(self):
        return u'%s %s %s %s' % (
            self.insee, self.gr_ss_gr, self.classe, self.nat_cult)


class Prospective(models.Model):
    theme = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = u'cad_prospective'

    def __unicode__(self):
        return u'%s' % (self.theme)


class ProspectiveTranslation(models.Model):
    id = models.ForeignKey(Prospective, db_column='id', primary_key=True)
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=2)

    class Meta:
        db_table = u'cad_prospective_translation'
        verbose_name = "prospective translation"


class Section(models.Model):
    insee = models.ForeignKey(Insee)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = u'cad_section'
        verbose_name = 'section'

    def __unicode__(self):
        return u'%s %s' % (self.insee, self.name)


class Lieudit(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(max_length=50, blank=True)
    cod_rivoli = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = u'cad_lieudit'
        verbose_name = "lieudit"

    def __unicode__(self):
        return u'%s %s' % (self.section, self.name)


class VgOwners(models.Model):
    """
        ->select(sprintf('gid, id_prj,
             activated, name, theme, updated_by, the_geom,
             (case when updated_by = %s then 1 else 0 end) as priority',
             $userId))
        ->andWhereIn('id_prj', $prjIds)
        ->andWhere('activated = ?', true)
        ->orWhere('updated_by = ?', $userId)
        ->andWhere('activated = ?', true)
        ->orderBy('priority desc');
    """
    gid = models.IntegerField(primary_key=True)
    id_prj = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=True)
    theme = models.CharField(max_length=255, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    activated = models.BooleanField()

    the_geom = models.PolygonField(srid=900913)

    objects = models.GeoManager()

    class Meta:
        db_table = u'vg_owners'


class VgProspective(models.Model):
    """
        ->select(sprintf('gid, id_prj,
             activated, name, theme, updated_by, the_geom,
             (case when updated_by = %s then 1 else 0 end) as priority',
             $userId))
        ->andWhereIn('id_prj', $prjIds)
        ->andWhere('activated = ?', true)
        ->orWhere('updated_by = ?', $userId)
        ->andWhere('activated = ?', true)
        ->orderBy('priority desc');
    """
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    theme = models.CharField(max_length=255, blank=True)
    id_prj = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    activated = models.BooleanField()

    the_geom = models.MultiPolygonField(srid=900913)

    class Meta:
        db_table = u'vg_prospective'


class Parcel(models.Model):
    # @todo See null and blank
    lieudit = models.ForeignKey(Lieudit)

    num_plan = models.IntegerField(null=True, blank=True)
    num_parc_prim = models.IntegerField(null=True, blank=True)
    # character varying in postgresql database
    code_edigeo = models.CharField(max_length=255, blank=True)
    gid = models.IntegerField(null=True, blank=True)
    edigeo_area = models.DecimalField(
        null=True, max_digits=18, decimal_places=4, blank=True)

    the_geom = models.PolygonField(srid=900913)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.code_edigeo

    class Meta:
        db_table = u'cad_prc'


class Owner(models.Model):
    name = models.CharField(max_length=50, blank=True)
    # @todo See max_length in database
    address = models.CharField(max_length=255, blank=True)
    # @todo See max_length in database
    phone = models.CharField(max_length=255, blank=True)
    theme = models.CharField(max_length=255, blank=True)
    edigeo_area = models.DecimalField(
        null=True, max_digits=18, decimal_places=2, blank=True)

    class Meta:
        db_table = u'cad_prj'

    def __unicode__(self):
        return u'%s' % (self.name)


class ParcelOwner(models.Model):
    prc = models.ForeignKey(Parcel)
    prj = models.ForeignKey(Owner)
    year = models.CharField(max_length=4, blank=True)
    activated = models.BooleanField()
    comments = models.CharField(max_length=255, blank=True)
    updated_by = models.ForeignKey(
        SfGuardUser, null=True, db_column='updated_by', blank=True)
    prospective = models.ForeignKey(Prospective, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'cad_prj_prc'


class CadPrjUser(models.Model):
    prj = models.ForeignKey(Owner)
    user = models.ForeignKey(SfGuardUser)
    percentage = models.DecimalField(
        null=True, max_digits=18, decimal_places=2, blank=True)

    class Meta:
        db_table = u'cad_prj_user'


class CadSubfisc(models.Model):
    # @see for notnull and blank status
    prc = models.ForeignKey(Parcel)
    suf = models.CharField(max_length=2, blank=True)
    area = models.DecimalField(
        null=True, max_digits=10, decimal_places=4, blank=True)

    class Meta:
        db_table = u'cad_subfisc'
        verbose_name = "subdivision"

    def __unicode__(self):
        return u'%s %s' % (self.prc, self.suf)


class CadFrt(models.Model):
    id = models.IntegerField(primary_key=True)
    subfisc = models.ForeignKey(CadSubfisc, null=True, blank=True)
    sprf = models.ForeignKey(FrtSprf, null=True, blank=True)
    neo_nat_cu = models.CharField(max_length=25, blank=True)
    neo_gr_ss = models.CharField(max_length=2, blank=True)
    neo_suf = models.CharField(max_length=1, blank=True)
    calculated_area = models.DecimalField(
        null=True, max_digits=10, decimal_places=4, blank=True)

    class Meta:
        db_table = u'cad_frt'


class CadFiscalite(models.Model):
    id = models.IntegerField(primary_key=True)
    eval_cult = models.ForeignKey(CadEvalCult, null=True, blank=True)
    subfisc = models.ForeignKey(CadSubfisc, null=True, blank=True)
    rc = models.DecimalField(
        null=True, max_digits=10, decimal_places=4, blank=True)
    year = models.CharField(max_length=4, blank=True)
    activated = models.BooleanField()

    class Meta:
        db_table = u'cad_fiscalite'

    def __unicode__(self):
        return u'%s %s %s' % (self.rc, self.year, self.activated)


class CadExoneration(models.Model):
    fiscalite = models.ForeignKey(CadFiscalite, null=True, blank=True)
    nat_exo = models.CharField(max_length=50, blank=True)
    until_year = models.CharField(max_length=4, blank=True)
    pourcent_exo = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'cad_exoneration'
        verbose_name = "Exoneration"

    def __unicode__(self):
        return u'%s %s %s' % (self.nat_exo, self.until_year, self.pourcent_exo)
