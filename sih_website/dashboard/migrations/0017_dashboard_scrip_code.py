# Generated by Django 2.2.2 on 2020-08-03 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_delete_company_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='scrip_code',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
