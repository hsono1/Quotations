from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.content),
    url(r'^login$', views.login),
    url(r'^remove$', views.remove),
    url(r'^logout$', views.logout),
    url(r'^addQuote$', views.addQuote),
    url(r'^users/(?P<id>\d+)$', views.userQuotes),
    url(r'^favorite$', views.userFavorite),
    url(r'^removeFav$', views.remove),

]