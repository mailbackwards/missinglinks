# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailadmin.taggable
import wagtail.wagtaildocs.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks
import modelcluster.fields
import wagtail.wagtailimages.blocks
import django.db.models.deletion
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('home', '0004_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('summary', models.TextField(blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('pullquote', wagtail.wagtailcore.blocks.RichTextBlock(icon='openquote')), ('page', wagtail.wagtailcore.blocks.PageChooserBlock(icon='doc-empty')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full')), ('citation', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=256, required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(null=False, blank=True)), (b'href', wagtail.wagtailcore.blocks.URLBlock(null=False, blank=True)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock())])), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media'))])),
                ('lead_art', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='PostPageTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='tagged_items', to='home.PostPage')),
                ('tag', models.ForeignKey(related_name='home_postpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='postpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='home.PostPageTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
