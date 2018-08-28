from django.urls import path
from .js_api_views import FaqListView, FaqRetrieveView

urlpatterns = [
    path('list', FaqListView.as_view()),
    path('<int:pk>', FaqRetrieveView.as_view(), name='detail'),
]

