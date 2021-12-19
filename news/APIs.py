from rest_framework import filters
from rest_framework import serializers
from rest_framework.response import Response
from news.models import News
from news.serilizer import CreateSerializer, NewsSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView


class StoryList(ListAPIView):
    queryset = News.object.get_stories()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'title']


class PollList(ListAPIView):
    queryset = News.object.get_polls()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'title']


class JobsList(ListAPIView):
    queryset = News.object.get_jobs()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'title']


class CreateItem(CreateAPIView):
    serializer_class = CreateSerializer
    queryset = News.object.all()

    def perform_create(self, serializer):
        if serializer.data['type'] == 'comment':
            raise serializers.ValidationError({"message": "failed", 'error': "Type 'comment' is not allowed, your options are 'poll', 'story' and 'job'"})
        try:
            serializer.create()
            return Response({"message": "Item was added successfully"})
        except Exception as ex:
            return Response({"message": "failed", "error": ex})
    

class DeleteItem(DestroyAPIView):
    queryset = News.object.all()
    serializer_class = NewsSerializer


class UpdateItem(UpdateAPIView):
    serializer_class = CreateSerializer
    queryset = News.object.all()
    lookup_field = 'pk'


    def update(self, request, *args, **kwargs):
        """
            Update news object by item id
        """
        instance = self.get_object()
        if instance.APICreated == False:
            raise serializers.ValidationError({"message": "failed", 'error': "This item cannot be updated"})
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, data=request.data)
            return Response({"message": "Update was done successfully"})
        else:
            return Response({"message": "failed", "error": serializer.errors})