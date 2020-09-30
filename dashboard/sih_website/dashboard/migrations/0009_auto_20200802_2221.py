# Generated by Django 2.2.2 on 2020-08-02 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200802_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='ca_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ca_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='ISIN',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='industry',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='instrument',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='security_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='security_group',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='security_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='status',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='securities_master',
            name='trading_symbol',
            field=models.CharField(max_length=100),
        ),
    ]
