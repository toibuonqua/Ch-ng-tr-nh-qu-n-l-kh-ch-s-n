from services.Sql_Service import Sqlservice
from error.errors import errorsys
from prettytable import PrettyTable


class RoomService(Sqlservice):
    def __init__(self):
        super().__init__()
        self.table = "rooms"
        self.primary_key = "name_room"

    def manager_room(self):
        print("Quản lý phòng khách sạn".center(40, "="))
        print("1. Thêm phòng")
        print("2. Cập nhập phòng")
        print("3. Xóa phòng")
        print("4. Trở về menu")
        print("5. Đăng xuất")
        press = input("Mời bạn nhập: ")
        if press == "1":
            print("Thêm phòng mới".center(40, "="))
            name_room = input("Nhập tên phòng: ")
            name_room_check = self.check_id(name_room)
            while name_room == name_room_check:
                print("Room name did exist".center(40, "#"))
                name_room = input("Nhập tên phòng: ")
                name_room_check = self.check_id(name_room)
            type_room = input("Nhập kiểu phòng: ")
            price_hour = int(input("Nhập giá phòng/ giờ: "))
            price_day = int(input("Nhập giá phòng/ ngày: "))
            room_status = input("Nhập trạng thái phòng: ")
            self.add({
                "name_room": name_room,
                "type_room": type_room,
                "price_hour": price_hour,
                "price_day": price_day,
                "room_status": room_status
            })
            return self.manager_room()
        elif press == "2":
            print("Cập nhật phòng".center(40, "="))
            self.showtable()
            id_room = input("Nhập tên phòng: ")
            check_id = self.check_id(id_room)
            if check_id is None:
                errorsys.phong_invalid()
                return self.manager_room()
            else:
                print("Cập nhập thông tin".center(40, "="))
                type_room = input("Nhập kiểu phòng: ")
                price_hour = int(input("Nhập giá phòng/giờ: "))
                price_day = int(input("Nhập giá phòng/ngày: "))
                self.update(id_room, {
                    "type_room": type_room,
                    "price_hour": price_hour,
                    "price_day": price_day
                })
                return self.manager_room()
        elif press == "3":
            print("Xóa phòng".center(40, "="))
            self.showtable()
            id_room = input("Nhập tên phòng: ")
            check_id = self.check_id(id_room)
            if check_id is None:
                errorsys.phong_invalid()
                return self.manager_room()
            else:
                self.delete(id_room)
                return self.manager_room()
        elif press == "4":
            return "back menu"
        elif press == "5":
            return "logout"
        else:
            return "back menu"

    def select_room(self):
        print("Phòng đang sẵn dùng".center(40, "="))
        sql = f"select * from {self.table} where room_status = 'avai'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        try:
            my_table = PrettyTable(list(result[0].keys()))
            for x in result:
                my_table.add_row(list(x.values()))
            print(my_table)
        except Exception:
            print("#" * 40)
            print("Hiện đang không có phòng nào sẵn dùng")
            print("#" * 40)
            input("Ấn để tiếp tục...")
            return "back menu"
        select_room = input("Phòng muốn đặt: ")
        check_room = self.check_id(select_room)
        if check_room == select_room:
            return self.find_by_info(header="name_room", value=select_room)
        else:
            print("Phòng không tồn tại hoặc không khả dụng".center(40, "#"))
            return self.choice()

    def choice(self):
        print("1. Tiếp tục đặt phòng")
        print("2. Trở về menu")
        nhap = input("Mời bạn nhập: ")
        if nhap == "1":
            return self.select_room()
        elif nhap == "2":
            return "back menu"

    def change_status_used(self, name_room):
        sql = f"update {self.table} set room_status = 'used' where {self.primary_key} = %s"
        self.cursor.execute(sql, (name_room,))
        self.connect.commit()

    def change_status_avai(self, name_room):
        sql = f"update {self.table} set room_status = 'avai' where {self.primary_key} = %s"
        self.cursor.execute(sql, (name_room,))
        self.connect.commit()