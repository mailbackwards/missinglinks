from .models import HomePage, PostPage, ExtraTag
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.syndication.views import Feed
import mimetypes

### POSTS ###

class PostListView(ListView):
    model = PostPage
    queryset = PostPage.objects.live().order_by('-first_published_at')
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        kwargs = super(PostListView, self).get_context_data(**kwargs)
        kwargs['featured_posts'] = PostPage.objects.filter(featured=True)
        return kwargs

class PostListTileView(PostListView):
    template_name = 'home/home_page.html'
    paginate_by = 8

class PostListFeedView(PostListView):
    template_name = 'home/home_page_list.html'
    paginate_by = 12


### TEMPLATES ###

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        kwargs = super(AboutView, self).get_context_data(**kwargs)
        kwargs['about_page'] = HomePage.objects.first()
        kwargs['featured_posts'] = PostPage.objects.filter(featured=True)
        return kwargs

class LinkView(TemplateView):
    template_name = 'home/links.html'

    def get_context_data(self, **kwargs):
        kwargs = super(LinkView, self).get_context_data(**kwargs)
        kwargs['featured_posts'] = PostPage.objects.filter(featured=True)
        return kwargs


### TAGS ###

class TagListView(ListView):
    model = ExtraTag
    context_object_name = 'tag_list'
    template_name = 'home/tag_list.html'
    paginate_by = 4
    ordering = '-post_page_tags__content_object__first_published_at'

    def get_context_data(self, **kwargs):
        kwargs = super(TagListView, self).get_context_data(**kwargs)
        kwargs['featured_tags'] = self.model._default_manager.filter(featured=True)
        return kwargs

    def get_queryset(self):
        return self.model._default_manager.prefetch_posts().order_by_post_count()

class TagDetailView(DetailView):
    model = ExtraTag
    template_name = 'home/tag.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        kwargs = super(TagDetailView, self).get_context_data(**kwargs)
        kwargs['featured_tags'] = self.model._default_manager.filter(featured=True)
        return kwargs


### FEEDS ###

class MainFeed(Feed):
    title = 'The Missing Links feed'
    link = '/feed/'
    description = 'Posts on The Missing Links project (themissinglinks.co)'

    author_name = 'Liam Andrew'
    author_email = 'liam.p.andrew@gmail.com'
    author_link = 'http://www.themissinglinks.co'
    feed_copyright = 'Copyright (c) 2016, Liam Andrew'
    item_author_name = 'Liam Andrew'
    item_author_email = 'liam.p.andrew@gmail.com'
    item_author_link = 'http://www.themissinglinks.co'
    item_copyright = 'Copyright (c) 2016, Liam Andrew'

    categories = ('media', 'publishing', 'technology', 'news', 'archives',
                  'hyperlinks')

    def items(self):
        return PostPage.objects.order_by('-first_published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.url

    def item_description(self, item):
        return item.body

    def item_enclosure_url(self, item):
        url = item.lead_art.file.url
        if url.startswith('//'):
            url = 'https:' + url
        return url

    def item_enclosure_length(self, item):
        return item.lead_art.get_file_size()

    def item_enclosure_mime_type(self, item):
        filename = item.lead_art.filename
        return mimetypes.guess_type(filename)[0]

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.latest_revision_created_at

    def item_categories(self, item):
        return item.tags.values_list('name', flat=True)
