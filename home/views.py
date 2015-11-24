from .models import HomePage, PostPage
from django.views.generic import ListView, TemplateView, DetailView

class PostListView(ListView):
    model = PostPage
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        kwargs = super(PostListView, self).get_context_data(**kwargs)
        kwargs['related_posts'] = PostPage.objects.filter(featured=True)
        return kwargs

class PostListTileView(PostListView):
    template_name = 'home/home_page.html'
    paginate_by = 8

class PostListFeedView(PostListView):
    template_name = 'home/home_page_list.html'
    paginate_by = 12

class PostDetailView(DetailView):
    model = PostPage
    template_name = 'home/post_page.html'
    context_object_name = 'post'

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        kwargs = super(TemplateView, self).get_context_data(**kwargs)
        kwargs['about_page'] = HomePage.objects.first()
        kwargs['related_posts'] = PostPage.objects.filter(featured=True)
        return kwargs
