from django.conf.urls import url

from bootcamp.articles.views import (
    ArticlesListView,
    ArticlesByTagListView,
    DraftsListView,
    CreateArticleView,
    EditArticleView,
    DetailArticleView,
)

app_name = "articles"
urlpatterns = [
    url(r"^$", ArticlesListView.as_view(), name="list"),
    url(r"^tag/(?P<slug>[-\w]+)/$", ArticlesByTagListView.as_view(), name="by_tag_list"),
    url(r"^write-new-article/$", CreateArticleView.as_view(), name="write_new"),
    url(r"^drafts/$", DraftsListView.as_view(), name="drafts"),
    url(r"^edit/(?P<pk>\d+)/$", EditArticleView.as_view(), name="edit_article"),
    url(r"^(?P<slug>[-\w]+)/$", DetailArticleView.as_view(), name="article"),
]
