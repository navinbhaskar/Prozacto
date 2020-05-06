# Generated by Django 2.2.12 on 2020-05-05 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_medical_records'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medical_records',
            name='url',
        ),
        migrations.AddField(
            model_name='medical_records',
            name='document',
            field=models.FileField(blank=True, default='document.zip', null=True, upload_to=''),
        ),
    ]
