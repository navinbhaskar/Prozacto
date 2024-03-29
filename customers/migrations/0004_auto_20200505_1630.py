# Generated by Django 2.2.12 on 2020-05-05 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='assistant',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.Clinic'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.Clinic'),
        ),
    ]
