from .models import HomePage, PostPage, ExtraTag
from django.views.generic import ListView, TemplateView, DetailView

### POSTS ###

class PostListView(ListView):
    model = PostPage
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
