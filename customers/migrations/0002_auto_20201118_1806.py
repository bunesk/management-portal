# Generated by Django 3.1.2 on 2020-11-18 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAdviser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email_address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='company',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='active',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone_number',
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email_address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('house_number', models.CharField(max_length=8)),
                ('postcode', models.CharField(max_length=16)),
                ('city', models.CharField(max_length=64)),
                ('adviser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='advisers', related_query_name='adviser', to='customers.customeradviser')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email_address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=64)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_persons', related_query_name='contact_person', to='customers.location')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]