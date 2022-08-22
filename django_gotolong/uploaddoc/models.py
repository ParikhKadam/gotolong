from __future__ import unicode_literals

from django.db import models

from datetime import date


class UploadDocModel(models.Model):

    def file_rename(instance, filename):
        ext = filename.split('.')[-1]
        return 'documents/{}/{}-data/{}/{}.{}'.format(instance.uploaddoc_scope, instance.uploaddoc_type,
                                                      instance.uploaddoc_year, instance.uploaddoc_type, ext)

    DOC_SCOPES = [
        ('input-global-data', "---GLOBAL---"),
        ('input-user-data', "---USER---"),
    ]

    DOC_TYPES = [
        ('global', "---GLOBAL---"),
        ('amfi', "AMFI"),
        ('bhav', "BHAV"),
        ('ftwhl', "FTWHL"),
        ('isin', "ISIN"),
        ('nach', "NACH"),
        ('screener', "SCREENER"),
        ('trendlyne', "TRNDLYNE"),
        ('gcweight', "WEIGHT"),
        ('user', "---USER---"),
        ('dematsum', "DEMATSUM"),
        ('dematxn', "DEMATTXN"),
        ('dividend', "DIVIDEND"),
    ]

    current_date = date.today()
    current_year = current_date.year

    DOC_YEARS = [
        ('all', "ALL"),
        ('latest', "LATEST"),
    ]

    for year_idx in range(current_year - 10, current_year + 1):
        next_year = year_idx + 1
        year_key = "FY " + str(year_idx) + "-" + str(next_year)
        DOC_YEARS.append((year_key, year_key))

    uploaddoc_id = models.AutoField(primary_key=True)
    uploaddoc_scope = models.CharField(max_length=255, choices=DOC_SCOPES)
    uploaddoc_type = models.CharField(max_length=255, choices=DOC_TYPES)
    uploaddoc_year = models.CharField(max_length=255, choices=DOC_YEARS, blank=True)
    uploaddoc_fpath = models.FileField(upload_to=file_rename)

    class Meta:
        db_table = 'user_doc'
