# Generated by Django 2.2.7 on 2020-03-11 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200311_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='token',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]