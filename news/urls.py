from .views import JobListView, StoryListView, PollsListView, SearchListView, detail_page
from django.urls import path


urlpatterns = [
    path('', StoryListView.as_view(), name="stories"),
    path('<int:pk>', detail_page, name="detail"),
    path('comment/<int:pk>', detail_page, name="comment"),
    path('jobs', JobListView.as_view(), name="jobs"),
    path('polls', PollsListView.as_view(), name="polls"),
    path('search', SearchListView.as_view(), name="search"),
]
