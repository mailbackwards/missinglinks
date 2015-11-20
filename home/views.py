from .models import TestPost
from django.views.generic import ListView

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
