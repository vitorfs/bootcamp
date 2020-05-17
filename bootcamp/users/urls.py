from django.conf.urls import url
from allauth.account.views import PasswordChangeView

from . import views

app_name = "users"
urlpatterns = [
    url(regex=r"^$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    url(
        regex=r"^~password/$",
        view=PasswordChangeView.as_view(),
        name="account_change_password",
    ),
    url(r"^picture/$", views.picture, name="picture"),
    url(r"^upload_picture/$", views.upload_picture, name="upload_picture"),
    url(
        r"^save_uploaded_picture/$",
        views.save_uploaded_picture,
        name="save_uploaded_picture",
    ),
    url(
        regex=r"^(?P<username>[\w.@+-]+)/$",
        view=views.UserDetailView.as_view(),
        name="detail",
    ),
]
