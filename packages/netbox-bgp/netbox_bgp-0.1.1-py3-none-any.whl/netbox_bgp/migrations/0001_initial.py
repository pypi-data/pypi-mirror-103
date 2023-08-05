# Generated by Django 3.1.3 on 2021-02-09 10:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('extras', '0053_rename_webhook_obj_type'),
        ('ipam', '0043_add_tenancy_to_aggregates'),
        ('tenancy', '0011_standardize_name_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4294967294)])),
                ('status', models.CharField(default='active', max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('value', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('\\d+:\\d+')])),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.role')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='community_related', to='dcim.site')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tenancy.tenant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ASNGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dcim.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ASN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4294967294)])),
                ('status', models.CharField(default='active', max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='netbox_bgp.asngroup')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipam.role')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='asn_related', to='dcim.site')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tenancy.tenant')),
            ],
            options={
                'verbose_name_plural': 'ASNs',
            },
        ),
    ]
