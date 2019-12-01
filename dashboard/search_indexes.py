import datetime
from haystack import indexes
from .models import News


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    suggestions = indexes.FacetCharField()
    title = indexes.CharField(model_attr='title', boost=1)
    # author = indexes.CharField(model_attr='author')
    # content = indexes.CharField(model_attr='content')
    content_auto = indexes.EdgeNgramField(model_attr='content')

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self, obj):
        prepared_data = super(NewsIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
