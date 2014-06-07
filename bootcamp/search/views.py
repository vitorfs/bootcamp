from django.shortcuts import render
from bootcamp.feeds.models import Feed

def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        
        try:
            search_type = request.GET.get('type')
        except Exception, e:
            search_type = 'feed'
        
        #if search_type == 'feed':
        results = Feed.objects.filter(post__icontains=querystring)

        return render(request, 'search/results.html', {'results': results})
    else:
        return render(request, 'search/search.html')