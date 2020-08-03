from django.db import models

# Create your models here.
class file_download(models.Model):
    #crawler_2 table 
    company_name = models.CharField(max_length=500)
    parent_link = models.CharField(max_length=500)
    url_of_file = models.CharField(max_length=500)
    sha_file = models.CharField(max_length=200,default=None)
    ca_checked = models.BooleanField(default=None)
    ca_type = models.CharField(max_length=100,default=None)
    ca_extracted = models.BooleanField(default=None) #aishwarya column 
    exception_ca = models.BooleanField(default=None) #varad ka column for exception  
    class meta:
        db_table = "file_download"


class corp_action_data (models.Model):
    company_name = models.CharField(max_length=255)
    ca_type = models.CharField(max_length=255,null=True)
    div_type = models.CharField(max_length=255,null=True)
    div_percent = models.FloatField(null= True)
    date = models.DateTimeField(null=True)
    bonus_ratio = models.CharField(max_length=255,null=True)
    announcement_date = models.DateTimeField(null=True)
    record_date = models.DateTimeField(null=True)
    ex_date = models.CharField(max_length=255,null=True)
    old_fv = models.IntegerField(null=True)
    new_fv = models.IntegerField(null=True)
    split_date = models.DateTimeField(null=True)
    purpose = models.CharField(max_length=255,null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    agenda = models.CharField(max_length=255,null=True)
    premium = models.IntegerField(null=True)
    right_ratio = models.FloatField(null= True)
    fv = models.IntegerField(null=True)
    # data = models.CharField(max_length=5000)

    class meta:
        db_table = "corp_action_data"



class articles(models.Model):
    url = models.CharField(max_length=1000,default=None)
    company_name = models.CharField(max_length=500,default=None)
    error = models.IntegerField(default=None)
    authors = models.CharField(max_length=1000,default=None)
    publish_date= models.DateTimeField(default=None)
    title = models.CharField(max_length=1000,default=None)
    content = models.CharField(max_length=10000,default=None)
    keywords = models.CharField(max_length=5000,default=None)
    filename = models.CharField(max_length=5000,default=None)
    ranks = models.FloatField(default=None)
    news_checked = models.IntegerField(default=None)
    ca_name = models.CharField(max_length=1000,default=None)


class company(models.Model):
    company_name = models.TextField()
    securities_ex = models.CharField(max_length=10)
    company_web_link = models.CharField(max_length=10)
    op_timeline = models.CharField(max_length=10)
    trading_location = models.CharField(max_length=10)



class dashboard(models.Model):
    date_ca = models.TextField()
    company_name = models.TextField()
    ca_name = models.TextField()
    security_id_type = models.TextField()
    id_value = models.TextField()
    ex_date = models.DateTimeField()
    rec_date = models.DateTimeField()
    pay_date = models.DateTimeField()
    other = models.CharField(max_length=30)
    exception = models.BooleanField()
    remarks = models.CharField(max_length=30)


class errors(models.Model):
    url = models.CharField(max_length=1000)
    exception = models.CharField(max_length=2000)


class historic_data(models.Model):
    security_code  = models.TextField(default=None)
    security_name  = models.TextField(default=None)
    company_name = models.CharField(max_length=255)
    ex_date = models.CharField(max_length=255,null=True)
    ca_type  = models.CharField(max_length=255)
    rec_date = models.CharField(max_length=255,null=True)
    bc_start_date = models.CharField(max_length=255,null=True)
    bc_end_date = models.CharField(max_length=255,null=True)
    nd_start_date = models.CharField(max_length=255,null=True)
    nd_end_date = models.CharField(max_length=255,null=True)
    

class links(models.Model):
    from_id = models.IntegerField()
    to_id = models.IntegerField()


class pages(models.Model):
    url = models.CharField(max_length=1000)
    keywords = models.CharField(max_length=5000)
    website = models.CharField(max_length=5000)
    error = models.IntegerField()
    old_rank = models.FloatField()
    new_rank = models.FloatField()
    moved = models.IntegerField()
    filename = models.CharField(max_length=500)



class securities(models.Model):
    company_name = models.TextField()
    security_type = models.CharField(max_length=100)
    isin = models.CharField(max_length=50)
    trade_volume = models.TextField()
    listed_on_exchange = models.CharField(max_length=20)
    exchange_symbol = models.CharField(max_length=100)



class webs(models.Model): 
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    web_rank = models.FloatField()

class securities_master(models.Model):
    isin =  models.CharField(max_length=100) 
    security_code  = models.CharField(max_length=100)
    trading_symbol = models.CharField(max_length=100)
    security_name  = models.CharField(max_length=100)
    status  = models.CharField(max_length=100)
    security_group  = models.CharField(max_length=100)
    face_value  = models.IntegerField()
    industry   = models.CharField(max_length=100)
    instrument  = models.CharField(max_length=100)
    nse_listed  = models.BooleanField()
    bse_listed  = models.BooleanField()
    trading_location = models.CharField(max_length=6)

class ca_list (models.Model):
    ca_type = models.CharField(max_length=20)
    ca_src = models.CharField(max_length=20,default=None)

