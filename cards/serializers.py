import logging

from rest_framework import serializers

from cards.models import Card

logger = logging.getLogger('api')


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'pk',
            'card_series',
            'card_number',
            # 'card_issue_datetime',
            'card_issue_datetime_in_format',
            # 'card_activity_end_datetime',
            'card_activity_end_datetime_in_format',
            'datetime_of_use',
            'sum_on_card',
            'card_status',
            'status',
        )
