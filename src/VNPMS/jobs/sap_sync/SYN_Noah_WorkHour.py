import csv

import xlwt
from jobs.sap_sync.encode import get_series_number
from jobs.sap_sync.utils import get_ip, get_batch_no, get_date_str
import datetime

class SYN_Noah_WorkHour(object):
    create_by = ""
    save_path = ""
    ip = ""
    dc_db = None
    sqlite_db = None

    # 建構子，初始化
    def __init__(self, sqlite_db, dc_db, create_by, save_path):
        self.sqlite_db = sqlite_db
        self.dc_db = dc_db
        self.create_by = create_by
        self.ip = get_ip()
        self.save_path = save_path

    # 取得報工資料
    def export_records(self, plant):
        sql = """select * from production_record where plant='{plant}' and sap_flag={sap_flag}""".format(plant=plant, sap_flag=0)
        records = self.sqlite_db.select_sql_dict(sql)
        return records

    # 更新報工資料
    def update_records(self, plant):
        sql = """update production_record set sap_flag=1 where plant='{plant}' and sap_flag=0""".format(
            plant=plant)
        self.sqlite_db.execute_sql(sql)

    # 報工資料轉入中介
    def create_dc_workhour_data(self, records, batch_no):
        amount = 0
        for record in records:
            tmp_record_dt = record['record_dt'].split('-')
            tmp_record_dt = tmp_record_dt[2] + tmp_record_dt[1] + tmp_record_dt[0]
            tmp_status = 'X' if record['status'] != None else ''

            sql = """insert into SYN_Noah_WorkHour(wo_no, cfm_code, item_no, record_id,
                             setting_time, mach_time, labor_time, emp_no, record_dt, good_qty, ng_qty, comment,
                             status, batch_no, create_by, create_at)
                             values('{wo_no}', '{cfm_code}', '{item_no}', '{record_id}', {setting_time},
                             {mach_time}, {labor_time}, '{emp_no}', '{record_dt}', {good_qty}, {ng_qty},
                             '{comment}', '{status}', '{batch_no}', '{create_by}', GETDATE())""" \
                .format(wo_no=record['wo_no'], cfm_code=record['cfm_code'], item_no=record['item_no'],
                        record_id=record['id'], setting_time=0, mach_time=record['mach_time'],
                        labor_time=record['labor_time'],
                        emp_no=record['sap_emp_no'], record_dt=tmp_record_dt, good_qty=record['good_qty'],
                        ng_qty=record['ng_qty'], comment=record['comment'], status=tmp_status,
                        batch_no=batch_no, create_by=self.ip)
            try:
                self.dc_db.execute_sql(sql)

                # 成功塞到中介就將Flag改成True
                sql = """update production_record set sap_flag=1 where wo_no='{wo_no}' and cfm_code='{cfm_code}'"""\
                    .format(wo_no=record['wo_no'], cfm_code=record['cfm_code'])
                self.sqlite_db.execute_sql(sql)

                amount += 1
            except Exception as e:
                print(e)
                print(sql)
        return amount

    # 取得中介要轉出資料
    def get_dc_workhour_data(self, batch_no):
        sql = "select * from SYN_Noah_WorkHour where batch_no='{batch_no}'".format(batch_no=batch_no)
        records = self.dc_db.select_sql_dict(sql)
        return records

    # 匯出CSV
    def prod_sap_workhour_csv(self, records, file_path):
        amount = 0
        fieldnames = ['PersonalNumber', 'Posting Date (DDMMYYYY)', 'WorkCenter', 'Production Order', 'Confirmation',
                   'Material', 'SetupTime', 'Machine Time', 'Labour Time', 'Yield to Confirm', 'Scrap to Confirm',
                   'ConfText', 'Partial/Final', 'SysX ID']

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                tmp_record_dt = record['record_dt'].split('-')
                tmp_record_dt = tmp_record_dt[2] + tmp_record_dt[1] + tmp_record_dt[0]
                tmp_status = 'X' if record['status'] != None else ''

                writer.writerow({'PersonalNumber': record['sap_emp_no'],
                                 'Posting Date (DDMMYYYY)': tmp_record_dt,
                                 'WorkCenter': "",
                                 'Production Order': record['wo_no'],
                                 'Confirmation': record['cfm_code'],
                                 'Material': record['item_no'],
                                 'SetupTime': "0",
                                 'Machine Time': record['mach_time'],
                                 'Labour Time': record['labor_time'],
                                 'Yield to Confirm': record['good_qty'],
                                 'Scrap to Confirm': record['ng_qty'],
                                 'ConfText': record['comment'],
                                 'Partial/Final': tmp_status,
                                 'SysX ID': record['id']})
                amount += 1
        return amount


    # 匯出Excel，Excel的欄位格式及內容調整
    def prod_sap_workhour_excel(self, batch_no):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Confirmation')
        ws.col(0).width = 256 * 20
        ws.col(1).width = 256 * 20
        ws.col(2).width = 256 * 20
        ws.col(3).width = 256 * 20
        ws.col(4).width = 256 * 20
        ws.col(5).width = 256 * 20
        ws.col(6).width = 256 * 20
        ws.col(7).width = 256 * 20
        ws.col(8).width = 256 * 20
        ws.col(9).width = 256 * 20
        ws.col(10).width = 256 * 20

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['PersonalNumber', 'Posting Date (DDMMYYYY)', 'WorkCenter', 'Production Order', 'Confirmation',
                   'Material', 'SetupTime', 'Machine Time', 'Labour Time', 'Yield to Confirm', 'Scrap to Confirm',
                   'ConfText', 'Partial/Final', 'SysX ID']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        records = self.get_dc_workhour_data(batch_no)

        for record in records:
            row_num += 1
            ws.write(row_num, 0, record['sap_emp_no'], font_style)  # SAP員編
            ws.write(row_num, 1, record['record_dt'], font_style)  # 工作執行日
            ws.write(row_num, 2, "", font_style)  # Work Center
            ws.write(row_num, 3, record['wo_no'], font_style)  # 生產工單
            ws.write(row_num, 4, record['cfm_code'], font_style)  # 確認單
            ws.write(row_num, 5, record['item_no'], font_style)  # 料號
            ws.write(row_num, 6, "0", font_style)  # setting time
            ws.write(row_num, 7, record['mach_time'], font_style)  # machine time
            ws.write(row_num, 8, record['labor_time'], font_style)  # labor time
            ws.write(row_num, 9, record['good_qty'], font_style)  # Yield to Confirm
            ws.write(row_num, 10, record['ng_qty'], font_style)  # Scrap to Confirm
            ws.write(row_num, 11, record['comment'], font_style)  # ConfText
            ws.write(row_num, 12, record['status'], font_style)  # Partial/Final
            ws.write(row_num, 13, record['record_id'], font_style)  # SysX ID
        return wb

    # 紀錄Log
    def save_log(self, func, batch_no, amount, create_by, file_name):
        create_at = datetime.datetime.now()
        sql = """insert into production_sync_sap_log(function,batch_no,create_by,amount,file_name,create_at)
                 Values('{function}','{batch_no}','{create_by}',{amount},'{file_name}','{create_at}')"""\
            .format(function=func, batch_no=batch_no, amount=amount, create_by=create_by, file_name=file_name, create_at=create_at)
        self.sqlite_db.execute_sql(sql)

    # 產生Excel檔案流程(已無使用)
    # def generate_excel(self, plant, file_name):
    #     records = self.export_records(plant)  # 取得本次處理資料
    #     batch_no = get_batch_no()  # 取號
    #     amount = self.create_dc_workhour_data(records, batch_no)  # Insert中介資料
    #     if amount > 0:
    #         self.save_log("workhour", batch_no, amount, self.create_by, file_name)  # 紀錄Log
    #         wb = self.prod_sap_workhour_csv(batch_no)
    #         wb.save(self.save_path + file_name)  # 儲存一份在主機上
    #         return wb

    # 產生CSV檔案流程
    def generate_csv(self, plant, file_path, file_name):
        amount = 0
        records = self.export_records(plant)  # 取得本次處理資料
        batch_no = get_batch_no()  # 取號

        if len(records) > 0:
            amount = self.prod_sap_workhour_csv(records, file_path)
            self.save_log("workhour", batch_no, amount, self.create_by, file_name)  # 紀錄Log
            self.update_records(plant)  # 更新Flag
        return amount

    # 取得檔案名稱
    def get_file_name(self, plant):
        key = plant + get_date_str()
        series = get_series_number(self.sqlite_db, "sap_workhour_excel", key)
        file_name = "TimeConf_{plant}_{key}V{series}.csv".format(plant=plant, key=key, series=series)
        return file_name
