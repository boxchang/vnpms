# # 滾序號
# def get_series_number(sqlite_db, function, key):
#     obj = Series.objects.filter(function=function, key=key)
#     if obj:
#         _series = obj[0].series + 1
#         obj.update(series=_series)
#     else:
#         _series = 1
#         Series.objects.create(function=function, key=key, series=1)
#     return _series


# 滾序號
def get_series_number(sqlite_db, function, key):
    sql = """select * from production_series where function='{function}' and key='{key}'"""\
        .format(function=function, key=key)
    results = sqlite_db.select_sql_dict(sql)

    if len(results) > 0:
        _series = results[0]['series'] + 1
        sql = """update production_series set series={series} where function='{function}' and key='{key}'"""\
            .format(function=function, key=key, series=_series)
        sqlite_db.execute_sql(sql)
    else:
        _series = 1
        sql = """insert into production_series(function,key,series) values('{function}','{key}',1)"""\
            .format(function=function, key=key)
        sqlite_db.execute_sql(sql)
    return _series
