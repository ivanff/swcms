from rest_framework import serializers
from .models import Faq


class FaqSerList(serializers.ModelSerializer):
    subject = serializers.ReadOnlyField(source='subject.h1')

    class Meta:
        model = Faq
        exclude = ('text',)


class FaqSerRetrieve(serializers.ModelSerializer):
    subject = serializers.ReadOnlyField(source='subject.h1')

    class Meta:
        model = Faq
        fields = '__all__'
