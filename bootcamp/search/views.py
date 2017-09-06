import json

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from bootcamp.questions.models import Question
from bootcamp.feeds.models import Feed
from bootcamp.decorators import ajax_required
from bootcamp.articles.models import Article


@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['feed', 'articles', 'questions', 'users']:
                search_type = 'feed'

        except Exception:
            search_type = 'feed'

        count = {}
        results = {}
        results['feed'] = Feed.objects.filter(post__icontains=querystring,
                                              parent=None)
        results['articles'] = Article.objects.filter(
            Q(title__icontains=querystring) | Q(
                content__icontains=querystring), status='P')
        results['questions'] = Question.objects.filter(
            Q(title__icontains=querystring) | Q(
                description__icontains=querystring))
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) | Q(
                    last_name__icontains=querystring))
        count['feed'] = results['feed'].count()
        count['articles'] = results['articles'].count()
        count['questions'] = results['questions'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })

    else:
        return render(request, 'search/search.html', {'hide_search': True})


# For autocomplete suggestions
@login_required
@ajax_required
def get_autocomplete_suggestions(request):
    querystring = request.GET.get('term', '')
    # Convert users, articles, questions objects into list to be
    # represented as a single list.
    users = list(User.objects.filter(
        Q(username__icontains=querystring) | Q(
            first_name__icontains=querystring) | Q(
                last_name__icontains=querystring)))
    articles = list(
        Article.objects.filter(Q(title__icontains=querystring) | Q(
            content__icontains=querystring), status='P'))
    questions = list(Question.objects.filter(
        Q(title__icontains=querystring) | Q(
            description__icontains=querystring)))
    # Add all the retrieved users, articles, questions to data_retrieved
    # list.
    data_retrieved = users
    data_retrieved.extend(articles)
    data_retrieved.extend(questions)
    results = []
    for data in data_retrieved:
        data_json = {}

        if isinstance(data, User):
            data_json['id'] = data.id
            data_json['label'] = data.username
            data_json['value'] = data.username

        if isinstance(data, Article):
            data_json['id'] = data.id
            data_json['label'] = data.title
            data_json['value'] = data.title

        if isinstance(data, Question):
            data_json['id'] = data.id
            data_json['label'] = data.title
            data_json['value'] = data.title

        results.append(data_json)

    final_suggestions = json.dumps(results)

    return HttpResponse(final_suggestions, 'application/json')
