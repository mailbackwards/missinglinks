from .models import TestPost, HomePage, Post
from django.views.generic import ListView, TemplateView, DetailView

class PostListTileView(ListView):
    model = TestPost
    template_name = 'home/home_page.html'
    context_object_name = 'post_list'
    paginate_by = 8

class PostListFeedView(ListView):
    model = TestPost
    template_name = 'home/home_page_list.html'
    context_object_name = 'post_list'
    paginate_by = 12

class PostDetailView(DetailView):
    model = Post
    template_name = 'home/post.html'
    context_object_name = 'post'

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        kwargs['about_page'] = HomePage.objects.first()
        return kwargs
