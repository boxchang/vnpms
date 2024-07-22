from bases.utils import get_date_str
from production.models import Series


# 滾序號
def get_series_number(function, key):
    obj = Series.objects.filter(function=function, key=key)
    if obj:
        _series = obj[0].series + 1
        obj.update(series=_series)
    else:
        _series = 1
        Series.objects.create(function=function, key=key, series=1)
    return _series