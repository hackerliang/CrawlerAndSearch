import time
import json
import requests
from django.shortcuts import render, get_object_or_404
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
import simplejson as json
from django.conf import settings
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from haystack.query import EmptySearchQuerySet
from .forms import FacetedSearchForm, ModelSearchForm
from .models import News


# def autocomplete(request):
#     sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
#     suggestions = [result.title for result in sqs]
#     # Make sure you return a JSON object, not a bare list.
#     # Otherwise, you could be vulnerable to an XSS attack.
#     the_data = json.dumps({
#         'results': suggestions
#     })
#     print(the_data)
#     return HttpResponse(the_data, content_type='application/json')

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))
    suggestions = [result.suggestions for result in sqs]
    print(sqs.spelling_suggestion('UI'))

    # for i in sqs:
    #     print(i.suggestions)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    # print(suggestions)
    return HttpResponse(the_data, content_type='application/json')


def spelling(q):
    r = requests.get(url="http://hadoopmaster:8983/solr/project/select?q=text%3A{}&wt=json&indent=true".format(q))
    # data = r.json()['spellcheck']
    spell_corr = list()
    data = None
    try:
        # visitt
        data = r.json()['spellcheck']['collations']
        spell_count = 1
        for i in data:
            if spell_count % 2 == 0:
                # Do it
                # print(i)
                i = json.loads(str(i).replace("'", '"'))['misspellingsAndCorrections'][1]
                spell_corr.append(i)
            else:
                pass
            spell_count += 1
        # data = data[1]
        # data = str(data)
        # data = data.replace("'", '"')
        # data = json.loads(data)
        # data = data['misspellingsAndCorrections']
    except:
        # print("NN")
        pass
    # print(data)
    try:
        if spell_corr:
            pass
        else:
            spell_corr = None
    except:
        pass
    return spell_corr


def suggestion_for_query(q):
    r = requests.get(url="http://hadoopmaster:8983/solr/project/select?q=text%3A{}&wt=json&indent=true".format(q))
    # data = r.json()['spellcheck']
    spell_corr = list()
    data = None
    try:
        # visitt
        data = r.json()['spellcheck']['suggestions'][1]
        data = json.loads(str(data).replace("'", '"'))

        # print(data['suggestion'])
        for i in data['suggestion']:
            spell_corr.append(i['word'])
        print(spell_corr)
        # spell_count = 1
        # for i in data:
        #     if spell_count % 2 == 0:
        #         # Do it
        #         # print(i)
        #         i = json.loads(str(i).replace("'", '"'))['misspellingsAndCorrections'][1]
        #         spell_corr.append(i)
        #     else:
        #         pass
        #     spell_count += 1
        # data = data[1]
        # data = str(data)
        # data = data.replace("'", '"')
        # data = json.loads(data)
        # data = data['misspellingsAndCorrections']
    except:
        # print("NN")
        pass
    # print(data)
    try:
        if spell_corr:
            pass
        else:
            spell_corr = None
    except:
        pass
    return spell_corr

def suggestion_for_ajax(request):
    q = request.GET.get("q")
    # print(request.GET)
    # print(q)
    r = requests.get(url="http://hadoopmaster:8983/solr/project/select?q=text%3A{}&wt=json&indent=true".format(q))
    # data = r.json()['spellcheck']
    spell_corr = list()
    data = None
    try:
        # visitt
        data = r.json()['spellcheck']['suggestions'][1]
        data = json.loads(str(data).replace("'", '"'))

        # print(data['suggestion'])
        for i in data['suggestion']:
            spell_corr.append(i['word'])
        print(spell_corr)
        # spell_count = 1
        # for i in data:
        #     if spell_count % 2 == 0:
        #         # Do it
        #         # print(i)
        #         i = json.loads(str(i).replace("'", '"'))['misspellingsAndCorrections'][1]
        #         spell_corr.append(i)
        #     else:
        #         pass
        #     spell_count += 1
        # data = data[1]
        # data = str(data)
        # data = data.replace("'", '"')
        # data = json.loads(data)
        # data = data['misspellingsAndCorrections']
    except:
        # print("NN")
        pass
    # print(data)
    try:
        if spell_corr:
            pass
        else:
            spell_corr = None
    except:
        pass
    return HttpResponse(json.dumps({
        'result': spell_corr
    }))


def news_view(request,news_id):
    news = get_object_or_404(News, pk=news_id)
    context = dict()
    context['news'] = news
    context['referer'] = request.META.get('HTTP_REFERER', "/")
    return render(request, 'news-view.html', context)


class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.searchqueryset = searchqueryset
        self.startTime = time.time()
        self.endTime = time.time()
        self.page_range = None

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request
        self.startTime = time.time()
        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.get_page(page_no)
            current_page_num = page.number
            page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                         list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
            if page_range[0] - 1 >= 2:
                page_range.insert(0, '...')
            if paginator.num_pages - page_range[-1] >= 2:
                page_range.append('...')
            if page_range[0] != 1:
                page_range.insert(0, 1)
            if page_range[-1] != paginator.num_pages:
                page_range.append(paginator.num_pages)
            self.page_range = page_range
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def get_context(self):
        (paginator, page) = self.build_page()
        self.endTime = time.time()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
            'time': (self.endTime - self.startTime),
            'page_range': self.page_range
        }

        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            # context['suggestion'] = self.form.get_suggestion()
            context['suggestion'] = spelling(self.get_query())

        context.update(self.extra_context())

        # suggestion_for_query(self.get_query())

        return context

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """

        context = self.get_context()


        return render(self.request, self.template, context)