from django.db import models

# Create your models here.
class file_download(models.Model):
    company_name = models.CharField(max_length=500)
    parent_link = models.CharField(max_length=500)
    url_of_file = models.CharField(max_length=500)

    class meta:
        db_table = "file_download"