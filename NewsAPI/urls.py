from django.contrib import admin
from django.urls import path, include
from news.APIs import CreateItem, JobsList, PollList, StoryList, DeleteItem, UpdateItem
from rest_framework_swagger.views import get_swagger_view



schema_view = get_swagger_view(title='News API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),

    path('api/stories/', StoryList.as_view(), name='api-stories'),
    path('api/jobs/', PollList.as_view(), name='api-jobs'),
    path('api/polls/', JobsList.as_view(), name='api-poll'),
    path('api/create/', CreateItem.as_view(), name='create'),
    path('api/update/<int:pk>', UpdateItem.as_view(), name='update'),
    path('api/delete/<int:pk>', DeleteItem.as_view(), name='delete'),
    path('docs/', schema_view)
]