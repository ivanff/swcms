from django.views.generic import ListView, DetailView
from .models import Posts, Tags


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    queryset = Posts.objects.active().prefetch_related('tags')
    current_tags = None

    def dispatch(self, request, *args, **kwargs):
        self.current_tags = Tags.objects.filter(id__in=self.request.GET.getlist('tag', []))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.current_tags:
            qs = qs.filter(tags__in=self.current_tags).distinct()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['current_tags'] = self.current_tags
        kwargs['tags'] = Tags.objects.filter(posts__isnull=False).distinct()
        return super().get_context_data(object_list=object_list, **kwargs)


class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    queryset = Posts.objects.active().prefetch_related('tags')


