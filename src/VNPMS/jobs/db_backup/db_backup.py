#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import os
import datetime
now = datetime.datetime.now()
file_name = datetime.datetime.strftime(now,'%Y%m%d %H%M%S')
delete_keyword = datetime.datetime.strftime((now - datetime.timedelta(days=7)), '%Y%m%d')
src = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'db.sqlite3')

dst_path = 'D:\\Noah_db_backup\\'
dst = dst_path + file_name + ".sqlite3"

for dirpath, dirName, filenames in os.walk(dst_path):
    for file in filenames:
        if delete_keyword in file:
            print(file)
            os.remove(dst_path+file)

result = os.path.isfile(src)
if result:
    shutil.copyfile(src, dst)

