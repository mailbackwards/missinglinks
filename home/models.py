from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

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
from wagtail.wagtailsearch.backends import get_search_backend
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.taggable import TagSearchable

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TagBase, ItemBase


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

class RelatedPostBlock(blocks.PageChooserBlock):
    @cached_property
    def target_model(self):
        return PostPage

    class Meta:
        icon = 'doc-empty'
        template = 'blocks/_relatedpost.html'


class HomePage(Page):
    body = RichTextField(null=False, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]

class TagQuerySet(models.QuerySet):
    def prefetch_posts(self):
        queryset = PostPageTag.objects.select_related('content_object')
        return self.prefetch_related(models.Prefetch('post_page_tags', queryset=queryset))

    def order_by_post_count(self):
        return self.annotate(post_count=models.Count('post_page_tags')).order_by('-post_count')

class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def prefetch_posts(self):
        return self.get_queryset().prefetch_posts()

    def order_by_post_count(self):
        return self.get_queryset().order_by_post_count()

    def search(self, query):
        return get_search_backend().search(query, self.get_queryset())

class ExtraTag(TagBase, index.Indexed):
    featured = models.BooleanField(default=False)
    objects = TagManager()

    search_fields = [
        index.SearchField('name', partial_match=True)
    ]

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])

class PostPageTag(ItemBase):
    tag = models.ForeignKey(
        ExtraTag, related_name="post_page_tags", on_delete=models.CASCADE)
    content_object = ParentalKey('home.PostPage', related_name='tagged_items')

    class Meta:
        ordering = ['-content_object__first_published_at']

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({
                '%s__content_object' % cls.tag_relname(): instance
            })
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update({
            '%s__content_object__isnull' % cls.tag_relname(): False
        })
        return cls.tag_model().objects.filter(**kwargs).distinct()


class PostPage(Page, TagSearchable):
    summary = models.TextField(null=False, blank=True)
    featured = models.BooleanField(default=False)
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
        ('related', RelatedPostBlock()),
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
        FieldPanel('featured'),
        FieldPanel('tags'),
    ]
    search_fields = Page.search_fields + TagSearchable.search_fields + (
        index.SearchField('body', partial_match=True),
    )

    @property
    def date(self):
        return self.first_published_at.date()

    class Meta:
        ordering = ['-first_published_at']

register_snippet(ExtraTag)
