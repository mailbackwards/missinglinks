from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HomePage(Page):
    body = RichTextField(null=False, default='')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full')
    ]

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
