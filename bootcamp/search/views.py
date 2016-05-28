from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from bootcamp.feeds.models import Feed
from bootcamp.articles.models import Article
from bootcamp.questions.models import Question
from django.contrib.auth.decorators import login_required


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

        except Exception, e:
            search_type = 'feed'

        count = {}
        results = {}
        results['feed'] = Feed.objects.filter(post__icontains=querystring,
                                              parent=None)
        results['articles'] = Article.objects.filter(
            Q(title__icontains=querystring) | Q(content__icontains=querystring)
            )
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
