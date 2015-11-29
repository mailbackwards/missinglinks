# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20151124_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('featured', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AlterField(
            model_name='postpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='home.ExtraTag', through='home.PostPageTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='postpagetag',
            name='tag',
            field=models.ForeignKey(related_name='post_page_tags', to='home.ExtraTag'),
        ),
    ]
