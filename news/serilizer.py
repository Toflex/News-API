from rest_framework import serializers
from .models import News
import math


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        exclude = ['deleted', 'dead', 'kids', 'time', 'score']


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title','text','url','type','by')

    def create(self):
        data = self.data
    
        item = News()
        item.text = data['text']
        item.title = data['title']
        item.by = data['by']
        item.type = data['type']
        item.url = data['url']
        item.APICreated = True
        item.save()


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('title','text','url','type','by')


    def update(self, instance, validated_data):
        data = validated_data
    
        instance.text = data['text']
        instance.title = data['title']
        instance.by = data['by']
        instance.type = data['type']
        instance.url = data['url']
        instance.save()

