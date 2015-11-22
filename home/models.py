from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

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
from wagtail.wagtailadmin.taggable import TagSearchable

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class CitationBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=256)
    author = blocks.CharBlock(null=False, blank=True)
    date = blocks.CharBlock(null=False, blank=True, help_text='Enter as string')
    href = blocks.URLBlock(null=False, blank=True)
    image = ImageChooserBlock(required=False)
    document = DocumentChooserBlock(required=False)

    class Meta:
        icon = 'snippet'
        template = 'blocks/_citation.html'

class PullquoteBlock(blocks.StructBlock):
    content = blocks.RichTextBlock(required=True)
    attribution = blocks.CharBlock(required=False, null=False, blank=True)

    class Meta:
        icon = 'openquote'
        template = 'blocks/_pullquote.html'


class HomePage(Page):
    body = RichTextField(null=False, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]

    search_fields = Page.search_fields + (
        index.SearchField('body', partial_match=True, boost=1),
    )

class PostPageTag(TaggedItemBase):
    content_object = ParentalKey('home.PostPage', related_name='tagged_items')

class PostPage(Page, TagSearchable):
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
        ('pullquote', PullquoteBlock()),
        ('page', blocks.PageChooserBlock(icon='doc-empty')),
        ('document', DocumentChooserBlock(icon='doc-full')),
        ('citation', CitationBlock()),
        ('embed', EmbedBlock(icon='media')),
    ])

    tags = ClusterTaggableManager(through=PostPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        ImageChooserPanel('lead_art'),
        StreamFieldPanel('body'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    search_fields = Page.search_fields + TagSearchable.search_fields + (
        index.SearchField('body'),
    )

    @property
    def date(self):
        return self.first_published_at.date()
