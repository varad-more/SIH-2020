from django.db import models

# Create your models here.
class file_download(models.Model):
    company_name = models.CharField(max_length=500)
    parent_link = models.CharField(max_length=500)
    url_of_file = models.CharField(max_length=500)
    sha_file = models.CharField(max_length=200,default=None)
    ca_checked = models.BooleanField(default=None)
    ca_type = models.CharField(max_length=100,default=None)

    class meta:
        db_table = "file_download"


class corp_action_data (models.Model):
    company_name = models.CharField(max_length=255)
    ca_type = models.CharField(max_length=255)
    data = models.CharField(max_length=5000)

    class meta:
        db_table = "corp_action_data"

    
