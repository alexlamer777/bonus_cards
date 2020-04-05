import logging

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cards.views import CRUDCard, GenerateCard, SearchCard, ActivatedCard

logger = logging.getLogger('api')
urlpatterns = [

    # CARD
    url(r'^card/$', CRUDCard.as_view()),
    url(r'^card/generate/$', csrf_exempt(GenerateCard.as_view())),
    url(r'^card/search/$', csrf_exempt(SearchCard.as_view())),
    url(r'^card/activated/$', csrf_exempt(ActivatedCard.as_view())),

]
