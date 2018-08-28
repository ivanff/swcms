from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Faq
from .serializers import FaqSerList, FaqSerRetrieve


class FaqListView(ListAPIView):
    queryset = Faq.objects.filter(is_active=True).select_related('subject')
    serializer_class = FaqSerList


class FaqRetrieveView(RetrieveAPIView):
    queryset = Faq.objects.filter(is_active=True).select_related('subject')
    serializer_class = FaqSerRetrieve
