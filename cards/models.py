from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from cards.settings import CARD_STATUSES, NON_ACTIVATED, DATETIME_FORMAT, SERVICE_TIME, TWELVE_MOUNTS, EXPIRED, \
    ACTIVATED


class Card(models.Model):
    card_series = models.CharField(verbose_name=_("Серия карты"), default="", max_length=50, blank=True, null=True)
    card_number = models.CharField(verbose_name=_("Номер карты"), default="", max_length=50, blank=True, null=True)
    card_issue_datetime = models.DateTimeField(verbose_name=_("Дата выпуска карты"),
                                               default=datetime.now, blank=True, null=True)
    card_activity_end_datetime = models.DateTimeField(verbose_name=_("Дата окончания активности карты"),
                                                      default=datetime.now, blank=True, null=True)
    datetime_of_use = models.SmallIntegerField(verbose_name=_("Срок использования карты"), default=TWELVE_MOUNTS,
                                               choices=SERVICE_TIME)
    sum_on_card = models.IntegerField(verbose_name=_("Сумма на карте"), default=0)
    card_status = models.SmallIntegerField(verbose_name=_("Статус карты"), default=NON_ACTIVATED, choices=CARD_STATUSES)

    def card_issue_datetime_in_format(self):
        return self.card_issue_datetime.strftime(DATETIME_FORMAT)

    def card_activity_end_datetime_in_format(self):
        return self.card_activity_end_datetime.strftime(DATETIME_FORMAT)

    def status(self):
        if self.card_status == ACTIVATED:
            if datetime.now().strftime(DATETIME_FORMAT) > self.card_activity_end_datetime.strftime(DATETIME_FORMAT):
                self.card_status = EXPIRED
                self.save()
        return self.card_status

    # def __init__(self, ):
    #     super().__init__()
    #     if datetime.now > self.card_activity_end_datetime:
    #         self.card_status = EXPIRED
