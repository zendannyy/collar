# Generated by Django 3.2.5 on 2021-08-25 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='isWorker',
            field=models.BooleanField(default='false', null=True),
        ),
    ]