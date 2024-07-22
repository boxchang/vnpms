import datetime
import uuid

from stock.models import Item, Bin, StockHistory, Stock, MovementType


def Do_Transaction(request, batch_no, mvt, item_code, bin_code, qty, desc):
    try:
        item = Item.objects.get(item_code=item_code)
        bin = Bin.objects.get(bin_code=bin_code)
        mvt = MovementType.objects.get(mvt_code=mvt)
        if bin and item:
            # 更新庫存資料
            invs = Stock.objects.filter(item=item, bin=bin)
            if invs:
                remain_qty = int(invs.first().qty) + qty
            else:
                remain_qty = qty

            if remain_qty >= 0:
                Stock.objects.update_or_create(item=item, bin=bin,
                                    defaults={'qty': remain_qty, 'update_by': request.user})

                if qty > 0:
                    StockHistory.objects.create(batch_no=batch_no, item=item, bin=bin, mtr_doc='', mvt=mvt, plus_qty=qty,
                                              minus_qty=0, remain_qty=remain_qty, desc=desc, create_by=request.user)
                else:
                    StockHistory.objects.create(batch_no=batch_no, item=item, bin=bin, mtr_doc='', mvt=mvt, plus_qty=0,
                                              minus_qty=-qty, remain_qty=remain_qty, desc=desc, create_by=request.user)
                result = "DONE"
            else:
                msg = '無庫存可以扣帳'
                print(msg)
                raise ValueError(msg)
    except Exception as e:
        print(e)
        result = "ERROR"
    return result