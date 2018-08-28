from django.views.generic import DetailView

from .models import Pages


class PagesDetailView(DetailView):
    template_name = "text_pages/pages_detail.html"
    queryset = Pages.objects.filter(is_active=True)
    slug_url_kwarg = 'url'
    slug_field = 'url'

    def dispatch(self, request, *args, **kwargs):
        self.kwargs[self.slug_url_kwarg] = '/' + self.kwargs[self.slug_url_kwarg]
        return super().dispatch(request, *args, **kwargs)
