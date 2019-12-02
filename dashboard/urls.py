from django.urls import path
from .views import autocomplete, news_view, SearchView, suggestion_for_ajax

urlpatterns = [
    path('search/autocomplete/', autocomplete),
    path('news/view/<int:news_id>', news_view, name='news-view'),
    path('search/', SearchView(), name='haystack_search'),
    path('search/ajax', suggestion_for_ajax, name='search_ajax')
]