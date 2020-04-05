NON_ACTIVATED = 0
ACTIVATED = 1
EXPIRED = 2

CARD_STATUSES = (
    (NON_ACTIVATED, u'Карта не активирована'),
    (ACTIVATED, u'Карта активирована'),
    (EXPIRED, u'Карта просрочена'))

ONE_MOUNTS = 0
SIX_MOUNTS = 1
TWELVE_MOUNTS = 2

SERVICE_TIME = (
    (ONE_MOUNTS, 1),
    (SIX_MOUNTS, 6),
    (TWELVE_MOUNTS, 12))

CARD_EXPIRY_DATE = 10
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
