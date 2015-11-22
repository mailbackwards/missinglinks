# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('home', '0004_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('summary', models.TextField(blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('pullquote', wagtail.wagtailcore.blocks.RichTextBlock()), ('other_page', wagtail.wagtailcore.blocks.PageChooserBlock()), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('citation', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=256, required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(null=False, blank=True)), (b'href', wagtail.wagtailcore.blocks.URLBlock(null=False, blank=True)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock())])), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock())])),
                ('lead_art', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
