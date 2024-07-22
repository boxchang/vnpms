import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(os.path.split(curPath)[0])[0]
sys.path.append(rootPath)

from jobs.sap_sync.database import dc_database, sqlite_database
from jobs.sap_sync.utils import get_ip
from jobs.sap_sync.SYN_Noah_Consumption import SYN_Noah_Consumption
from jobs.sap_sync.SYN_Noah_WorkHour import SYN_Noah_WorkHour

plants = ['302A', '302B']
save_path = "C:\\temp\\python\\"

create_by = get_ip()  # 執行位置
dc_db = dc_database()  # 中介資料庫
sqlite_db = sqlite_database()  # Noah資料庫


def prepare_test_data():
    # 報工測試資料重置
    sql = "update production_record set sap_flag=0 where update_at like '2024-04-02%'"
    sqlite_db.execute_sql(sql)

    # 物料耗用資料重置
    sql = "update production_consumption set sap_flag=0 where create_at like '2024-04-02%'"
    sqlite_db.execute_sql(sql)

    # 清空中介報工資料表
    sql = "delete from SYN_Noah_WorkHour"
    dc_db.execute_sql(sql)

    # 清空中介耗用資料表
    sql = "delete from SYN_Noah_Consumption"
    dc_db.execute_sql(sql)



# 測試時使用，上線要拿掉
prepare_test_data()

workhour = SYN_Noah_WorkHour(sqlite_db, dc_db, create_by, save_path)
for plant in plants:
    file_name = workhour.get_file_name(plant)
    workhour.generate_excel(plant, file_name)

material = SYN_Noah_Consumption(sqlite_db, dc_db, create_by, save_path)
for plant in plants:
    file_name = material.get_file_name(plant)
    material.generate_excel(plant, file_name)
