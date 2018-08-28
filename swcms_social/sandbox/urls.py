from django.urls import path
from .views import *

urlpatterns = [
    path(r'', SandboxIndexView.as_view(), name='sandbox'),
    path(r'<path:file_path>', SandboxView.as_view(), name='sandbox'),
]
