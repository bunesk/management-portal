# Generated by Django 3.1.2 on 2020-12-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('licenses', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactperson',
            name='product',
            field=models.ManyToManyField(related_name='contact_persons', related_query_name='contact_person', to='licenses.SoftwareProduct'),
        ),
    ]