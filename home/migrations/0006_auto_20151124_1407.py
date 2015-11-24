# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import home.models
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0004_set_unique_on_path_and_site'),
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('home', '0005_auto_20151122_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testpost',
            name='image',
        ),
        migrations.RemoveField(
            model_name='testpost',
            name='page_ptr',
        ),
        migrations.AddField(
            model_name='postpage',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='postpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), (b'attribution', wagtail.wagtailcore.blocks.CharBlock(required=False, null=False, blank=True))])), ('related', home.models.RelatedPostBlock()), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full')), ('citation', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=256, required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(null=False, blank=True)), (b'date', wagtail.wagtailcore.blocks.CharBlock(help_text='Enter as string', null=False, blank=True)), (b'href', wagtail.wagtailcore.blocks.URLBlock(null=False, blank=True)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(required=False))])), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media'))]),
        ),
        migrations.DeleteModel(
            name='TestPost',
        ),
    ]
