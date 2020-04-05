# coding=utf-8

from django.contrib import admin

from cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'card_number', 'card_series', 'card_issue_datetime',
        'card_activity_end_datetime', 'card_status', 'status')


admin.site.register(Card, CardAdmin)
