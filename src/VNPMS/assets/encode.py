from assets.models import Series, Location


# 滾序號
def get_series_number(_key, _key_name):
    obj = Series.objects.filter(key=_key)
    if obj:
        _series = obj[0].series + 1
        obj.update(series=_series, desc=_key_name)
    else:
        _series = 1
        Series.objects.create(key=_key, series=1, desc=_key_name)
    return _series


class EncodeInterface:
    def __init__(self, classname=None):
        self.process = classname

    def run(self):
        return self.process.run()


class EncodeIT:
    def __init__(self, asset_category, asset_type):
        self.type_code = asset_type.type_code  # 縮寫
        self.type_name = asset_type.type_name.upper()
        self.type_id = str(asset_type.id)
        self.category_id = str(asset_category.id)
        self.category_name = str(asset_category.category_name)
        self.prefix = asset_type.prefix
        self.series_len = asset_type.series_len

    def run(self):
        if not self.prefix:
            self.prefix = "IT-" + self.type_code + "-"
        _key = self.category_id.zfill(3) + self.type_id.zfill(3)
        _key_name = self.category_name + "_" + self.type_name
        _series = get_series_number(_key, _key_name)
        series_format = str(_series).zfill(self.series_len)
        series_code = self.prefix + series_format
        return series_code


class EncodeOffice:
    def __init__(self, asset_category, asset_type, asset_location):
        self.location_id = str(asset_location.id)
        self.location_name = str(asset_location.location_name)
        self.type_code = asset_type.type_code  # 縮寫
        self.type_name = asset_type.type_name.upper()
        self.category_id = str(asset_category.id)
        self.category_name = str(asset_category.category_name)
        self.series_len = asset_type.series_len

    def run(self):
        loc_obj = Location.objects.filter(id=self.location_id)
        location_code = loc_obj[0].location_code
        series_code = "A-" + location_code + "-" + self.type_code + "-"
        _key = self.category_id.zfill(3) + location_code.zfill(3) + self.type_code.zfill(3)
        _key_name = self.category_name + "_" + self.location_name + "_" + self.type_name
        _series = get_series_number(_key, _key_name)
        series_format = str(_series).zfill(self.series_len)
        series_code = series_code + series_format
        return series_code


class EncodeGeneral:
    def run(self):
        _key = "AMS"
        _key_name = "AMS"
        _series = get_series_number(_key, _key_name)
        series_format = str(_series).zfill(7)
        series_code = _key + series_format
        return series_code
