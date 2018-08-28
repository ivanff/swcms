import os

from django.conf import settings
from django.views import static
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import TemplateView


class SandboxIndexView(TemplateView):
    def get_template_names(self):
        return 'sandbox/index.html'

    def get_filename(self, name):
        if name.endswith('.html'):
            return os.path.splitext(name)[0]
        return name

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        path = os.path.join(settings.BASE_DIR, 'templates', 'sandbox', self.kwargs.get('file_path', ''))

        files = filter(lambda name: os.path.isfile(os.path.join(path, name)) and name != 'index.html', os.listdir(path))
        dirs = filter(lambda name: os.path.isdir(os.path.join(path, name)), os.listdir(path))

        kwargs['files'] = list(map(lambda name: {
            'file_name': name,
            'name': os.path.splitext(name)[0],
            'url': os.path.join(self.kwargs.get('file_path', ''), self.get_filename(name))}, files))

        kwargs['dirs'] = list(map(lambda name: {
            'dir_name': name,
            'name': os.path.splitext(name)[0],
            'url': os.path.join(self.kwargs.get('file_path', ''), os.path.splitext(name)[0])}, dirs))

        order = self.request.GET.get('order', '-changed')
        if order in ['name', '-name']:
            kwargs['files'] = sorted(kwargs['files'], key=lambda i: i['name'], reverse=order[0] == '-')

        if order in ['created', '-created']:
            kwargs['files'] = sorted(kwargs['files'], key=lambda i: os.path.getmtime(os.path.join(path, i['file_name'])), reverse=order[0] == '-')

        if order in ['changed', '-changed']:
            kwargs['files'] = sorted(kwargs['files'], key=lambda i: os.path.getctime(os.path.join(path, i['file_name'])), reverse=order[0] == '-')

        kwargs['order'] = order
        kwargs['sub_dir'] = self.kwargs.get('file_path', '')
        return kwargs


class SandboxView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'templates', 'sandbox')
        file_path = os.path.join(path, self.kwargs['file_path'])
        if os.path.isdir(file_path):
            return SandboxIndexView.as_view()(request, *args, **kwargs)

        if os.path.isfile(file_path):
            return static.serve(request, self.kwargs['file_path'], document_root=path)

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return 'sandbox/%(file_path)s.html' % self.kwargs

    def get(self, request, *args, **kwargs):
        if self.kwargs['file_path'] == 'index':
            return HttpResponseRedirect(reverse('sandbox:sandbox'))
        return super().get(request, *args, **kwargs)