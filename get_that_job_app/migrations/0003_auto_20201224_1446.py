# Generated by Django 2.2.4 on 2020-12-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_that_job_app', '0002_auto_20201224_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='education',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='field_of_experience',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
