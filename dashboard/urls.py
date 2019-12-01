from django.urls import path
from .views import autocomplete, news_view, SearchView

urlpatterns = [
    path('search/autocomplete/', autocomplete),
    path('news/view/<int:news_id>', news_view, name='news-view'),
    path('search/', SearchView(), name='haystack_search')
]