from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailsearch import index


class CitationBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=256)
    author = blocks.CharBlock(null=False, blank=True)
    href = blocks.URLBlock(null=False, blank=True)
    image = ImageChooserBlock()
    document = DocumentChooserBlock()

    class Meta:
        icon = 'snippet'


class HomePage(Page):
    body = RichTextField(null=False, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]

    search_fields = Page.search_fields + (
        index.SearchField('body', partial_match=True, boost=1),
    )

class Post(Page):
    summary = models.TextField(null=False, blank=True)
    lead_art = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('image', ImageChooserBlock(icon='image')),
        ('pullquote', blocks.RichTextBlock(icon='openquote')),
        ('page', blocks.PageChooserBlock(icon='doc-empty')),
        ('document', DocumentChooserBlock(icon='doc-full')),
        ('citation', CitationBlock()),
        ('embed', EmbedBlock(icon='media')),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('headline'),
        FieldPanel('summary'),
        ImageChooserPanel('lead_art'),
        StreamFieldPanel('body'),
    ]

    @property
    def date(self):
        return self.first_published_at.date()


class TestPost(Page):
    body = RichTextField()
    date = models.DateField('Post date')
    headline = models.CharField(max_length=128, null=False, blank=True)
    summary = models.TextField(null=False, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname='full')
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, 'Common page configuration'),
        ImageChooserPanel('image')
    ]
