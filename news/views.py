from django.http.response import HttpResponse
import sys
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import News
from news.hackerAPI import startScheduler


if 'runserver' in sys.argv:
    startScheduler()


class StoryListView(ListView):
    template_name = 'news/list_items.html'
    context_object_name = 'items'
    Model = News
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(StoryListView, self).get_context_data(**kwargs)
        context["title"] = "News"
        return context

    def get_queryset(self):
        """Return all news of type story."""
        return News.object.get_stories()


# class DetailView(DetailView):
#     queryset = News.object.get_item_by_pk()
#     template_name = 'news/detail.html'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['book_list'] = '' #Book.objects.all()
#         return context

#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return {} #Question.objects.filter(pub_date__lte=timezone.now())


def detail_page(request, pk:int) -> HttpResponse:
    
    news = get_object_or_404(News, pk=pk)
    kids = News.object.get_comments(news.kids)
    context = {"news": news, "kids": kids}
    return render(request, 'news/detail.html', context)


# def comments(request, pk:int) -> HttpResponse:
    
#     news = get_object_or_404(News, pk=pk)
#     kids = News.object.get_comments(news.kids)
#     context = {"news": news, "kids": kids}
#     return render(request, 'news/detail.html', context)


class JobListView(ListView):
    template_name = 'news/list_items.html'
    context_object_name = 'items'
    Model = News
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context["title"] = "Jobs"
        return context

    def get_queryset(self):
        """Return all news of type job."""
        return News.object.get_jobs()


class PollsListView(ListView):
    template_name = 'news/list_items.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)
        context["title"] = "Polls"
        return context

    def get_queryset(self):
        """Return all news of type poll."""
        return News.object.get_polls()

        
class SearchListView(ListView):
    template_name = 'news/list_items.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context.update({
           'title': "Search Results: '{}'".format(self.request.GET.get('query'))
        })
        return context


    def get_queryset(self):
        """Return all news that matches filter params."""
        query = self.request.GET.get('query') or ''
        type = self.request.GET.get('type')
        print("Query text:", query)
        print("Type:",type)
        return News.object.get_search(query=query, type=type)
