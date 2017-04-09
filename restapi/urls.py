from rest_framework import renderers
from .views import getScore, buy, sell
from django.conf.urls import url, include



urlpatterns = [
    url(r'^score/(?P<stock>\d+)[/]?$', getScore.as_view(), name='score'),
    url(r'^score[/]?$', getScore.as_view(), name='score'),

    url(r'^buy/(?P<stock>\d+)[/]?$', buy.as_view(), name='buy'),
    url(r'^buy[/]?$', buy.as_view(), name='buy'),

    url(r'^sell/(?P<stock>\d+)[/]?$', sell.as_view(), name='sell'),
    url(r'^sell[/]?$', sell.as_view(), name='sell'),

]