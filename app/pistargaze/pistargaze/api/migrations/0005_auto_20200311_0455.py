# Generated by Django 2.2.7 on 2020-03-11 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200311_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.TextField(),
        ),
    ]
