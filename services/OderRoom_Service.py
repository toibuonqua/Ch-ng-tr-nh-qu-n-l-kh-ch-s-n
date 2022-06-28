from services.Sql_Service import Sqlservice
from prettytable import PrettyTable
from error.errors import errorsys


class OderRoomService(Sqlservice):
    def __init__(self):
        super().__init__()
        self.table = "order_rooms"
        self.primary_key = "id"

    def menu_order_room(self, info_acc, dict_room, id_cus):
        print("Thông tin đặt phòng".center(40, "="))
        print(f"ID nhân viên đặt: {info_acc.id}")
        print(f"Tên nhân viên đặt: {info_acc.name}")
        print(f"Đặt phòng: {dict_room.get('name_room')}")
        print(f"CCCD khách đặt: {id_cus}")
        total_time_hour = int(input("Thuê theo giờ: "))
        total_time_day = int(input("Thuê theo ngày: "))
        if total_time_day != 0:
            price = total_time_day * dict_room.get("price_day")
        elif total_time_hour != 0:
            price = total_time_hour * dict_room.get("price_hour")
        print(f"Tổng thanh toán: {price} VND")
        self.add({
            "id_account": info_acc.id,
            "id_room": dict_room.get("name_room"),
            "id_customer": id_cus,
            "total_time_hour": total_time_hour,
            "total_time_day": total_time_day,
            "price": price,
            "od_status": "check in"
        })
        self.update_checkin_checkout(self.get_max_id(), total_time_hour, total_time_day)
        return price

    def update_checkin_checkout(self, id_oder, hour, day):
        sql = f"update {self.table} set check_in = current_timestamp() where {self.primary_key} = %s"
        self.cursor.execute(sql, (id_oder,))
        self.connect.commit()
        sql_hour = f"update {self.table} set check_out = adddate(check_in, interval %s hour) where {self.primary_key} = %s"
        sql_day = f"update {self.table} set check_out = adddate(check_in, interval %s day) where {self.primary_key} = %s"
        if hour != 0:
            self.cursor.execute(sql_hour, (hour, id_oder))
            self.connect.commit()
        if day != 0:
            self.cursor.execute(sql_day, (day, id_oder))
            self.connect.commit()

    def show_order(self):
        print("Phòng đang sử dụng".center(40, "#"))
        sql = f"select id_account, id_room, id_customer, check_in, check_out, price, od_status from {self.table} where od_status = 'check in'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        my_table = PrettyTable(list(result[0].keys()))
        for x in result:
            my_table.add_row(list(x.values()))
        print(my_table)

    def ktra_check_out(self, id_cccd, name_room):
        sql = f"select * from {self.table} where id_room = %s and id_customer = %s and od_status = 'check in'"
        self.cursor.execute(sql, (name_room, id_cccd))
        result = self.cursor.fetchone()
        try:
            return result
        except Exception:
            return None

    def check_out_order(self):
        print("Trả phòng".center(40, "="))
        self.show_order()
        id_cccd = input("Nhập CCCD khách hàng: ")
        name_room = input("Nhập phòng: ")
        result = self.ktra_check_out(id_cccd, name_room)
        if result is None:
            errorsys.order_invalid()
            return self.display_check_out()
        else:
            sql = f"update {self.table} set od_status = 'check out' where {self.primary_key} = %s"
            self.cursor.execute(sql, (result.get("id"),))
            self.connect.commit()
            print("Check out thành công".center(40, "~"))
            return name_room

    def display_check_out(self):
        print("Khách hàng trả phòng".center(40, "="))
        print("1. Kiểm tra phòng đang sử dụng")
        print("2. Khách check out")
        print("3. Trở về menu")
        nhap = input("Mời bạn nhập: ")
        if nhap == "1":
            self.show_order()
            press = input("nhập phím bất kì để về menu...")
            return self.display_check_out()
        elif nhap == "2":
            return self.check_out_order()
        elif nhap == "3":
            return "back menu"
        else:
            return "logout"
