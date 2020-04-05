from datetime import datetime, timedelta
from random import randint

from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cards.models import Card
from cards.serializers import CardSerializer
from cards.settings import SERVICE_TIME, NON_ACTIVATED, ACTIVATED
from django.db.models import Q


class CRUDCard(APIView):
    context = {}
    status_code = status.HTTP_200_OK

    def dispatch(self, request, *args, **kwargs):
        self.context['data'] = ''
        self.context['detail'] = ''
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        card = Card.objects.all()
        self.context['data'] = CardSerializer(card, many=True).data
        return Response(self.context, status=self.status_code)

    def update_card(self, request, card):
        card_series = self.request.data.get('card_series')
        card_number = self.request.data.get('card_number')
        card_issue_datetime = self.request.data.get('card_issue_datetime')
        card_activity_end_datetime = self.request.data.get('card_activity_end_datetime')
        datetime_of_use = self.request.data.get('datetime_of_use')
        sum_on_card = self.request.data.get('sum_on_card')
        card_status = self.request.data.get('card_status')
        if card_series:
            card.card_series = card_series
        if card_number:
            card.card_number = card_number
        if card_issue_datetime:
            card.card_issue_datetime = card_issue_datetime
        if card_activity_end_datetime:
            card.card_activity_end_datetime = card_activity_end_datetime
        if datetime_of_use:
            card.datetime_of_use = datetime_of_use
        if sum_on_card:
            card.sum_on_card = sum_on_card
        if card_status:
            card.card_status = sum_on_card
        return card

    def post(self, request, **kwargs):

        new_card = Card.objects.create()
        new_card = self.update_card(request, new_card)
        new_card.save()
        self.context['data'] = CardSerializer(new_card).data
        return Response(self.context, self.status_code)

    def put(self, request, **kwargs):

        card = Card.objects.filter(pk=self.request.data.get('pk')).first()
        card = self.update_card(request, card)
        card.save()

        return Response(self.context, self.status_code)

    def delete(self, request, **kwargs):
        print(self.request.POST.get('pk'))
        card = Card.objects.filter(pk=self.request.data.get('pk')).first()
        card.delete()
        return Response(self.context, self.status_code)


class GenerateCard(APIView):
    context = {}
    status_code = status.HTTP_200_OK

    def dispatch(self, request, *args, **kwargs):
        self.context['data'] = ''
        self.context['detail'] = ''
        return super().dispatch(request, *args, **kwargs)

    def random_with_N_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def post(self, request, *args, **kwargs):
        generate_cards_count = self.request.POST.get('generate_cards_count', None)
        generate_series = self.request.POST.get('generate_series', None)
        datetime_of_use = int(self.request.POST.get('generate_datetime_of_use', None))
        for card in range(int(generate_cards_count)):
            card = Card.objects.create()
            if generate_series:
                card.card_series = generate_series
            else:
                card.card_series = self.random_with_N_digits(4)
            card.card_number = self.random_with_N_digits(8)
            card.datetime_of_use = datetime_of_use
            card.card_activity_end_datetime = (datetime.now() + relativedelta(months=+SERVICE_TIME[datetime_of_use][1]))
            card.sum_on_card = self.random_with_N_digits(4)
            card.card_status = 0
            card.save()

        return Response(self.context, status=self.status_code)


class SearchCard(APIView):
    context = {}
    status_code = status.HTTP_200_OK

    def dispatch(self, request, *args, **kwargs):
        self.context['data'] = ''
        self.context['detail'] = ''
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        search_query = self.request.POST.get('search_field', None)
        status_query = self.request.POST.get('search_status_field', None)
        cards_pk = Card.objects.filter(
            Q(card_series__icontains=search_query) | Q(card_number__icontains=search_query) | Q(
                card_issue_datetime__icontains=search_query) | Q(
                card_activity_end_datetime__icontains=search_query))
        if status_query:
            cards_pk = cards_pk.filter(Q(card_status=status_query))
        cards = Card.objects.filter(pk__in=cards_pk.distinct().values_list('pk', flat=True))
        self.context['data'] = CardSerializer(cards, many=True).data
        return Response(self.context, status=self.status_code)


class ActivatedCard(APIView):
    context = {}
    status_code = status.HTTP_200_OK

    def dispatch(self, request, *args, **kwargs):
        self.context['data'] = ''
        self.context['detail'] = ''
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        status_change = int(self.request.POST.get('status_change', None))
        card_pk = self.request.POST.get('pk', None)
        card = Card.objects.filter(pk=card_pk).first()
        print(status_change)
        if status_change:
            card.card_status = NON_ACTIVATED
        else:
            card.card_status = ACTIVATED
        card.save()
        return Response(self.context, status=self.status_code)
