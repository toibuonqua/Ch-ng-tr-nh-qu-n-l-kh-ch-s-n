from services.OderRoom_Service import OderRoomService
from services.Account_Service import AccountService
from services.Customer_Service import CustomerService
from services.Room_Service import RoomService
from error.errors import errorsys


class main:

    def __init__(self):
        self.account = AccountService()
        self.order_room = OderRoomService()
        self.customer = CustomerService()
        self.room = RoomService()

    def login(self):
        print("Login".center(40, "="))
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        check_role = self.account.check_login(username, password)
        if check_role == 1:
            self.menu_manager()
        elif check_role == 2:
            self.menu_employee()
        else:
            errorsys.login_error()

    def menu_manager(self):
        list_menu = {
            1: "Quản lý tài khoản cá nhân",
            2: "Quản lý tài khoản hệ thống",
            3: "Quản lý phòng",
            4: "Quản lý thông tin khách hàng",
            5: "Đặt phòng",
            6: "Trả phòng",
            7: "Thống kê khách hàng",
            8: "Đăng xuất"
        }
        print(f"Chào {self.account.account1.name}, chúc bạn 1 ngày làm việc hiệu quả".center(40, "="))
        option = self.show_menu(list_menu)
        if option == 1:
            out = self.account.show_info_acc()
            if out == "back menu":
                pass
            elif out == "choice invalid":
                pass
            elif out == "input too much":
                errorsys.input_error()
            else:
                self.account.update_password(out)
                return self.login()
            return self.menu_manager()
        elif option == 2:
            out = self.account.manager_acc()
            if out == "back menu":
                return self.menu_manager()
            elif out == "logout":
                return self.logout()
        elif option == 3:
            out = self.room.manager_room()
            if out == "back menu":
                return self.menu_manager()
            elif out == "logout":
                return self.logout()
        elif option == 4:
            out = self.customer.manager_customer()
            if out == "back menu":
                return self.menu_manager()
        elif option == 5:
            print("Đặt phòng".center(40, "="))
            id_customer = int(input("Nhập cccd khách hàng: "))
            check_cccd = self.customer.check_customer(id_customer)
            info_acc = self.account.account1
            select_room = self.room.select_room()
            if select_room == "back menu":
                return self.menu_manager()
            price = self.order_room.menu_order_room(info_acc, select_room, check_cccd)
            self.customer.plus_price(price, id_customer)
            self.room.change_status_used(select_room.get("name_room"))
            return self.menu_manager()
        elif option == 6:
            out = self.order_room.display_check_out()
            if out == "back menu":
                return self.menu_manager()
            elif out == "out system":
                return self.logout()
            else:
                self.room.change_status_avai(out)
                return self.menu_manager()
        elif option == 7:
            pass
        elif option == 8:
            return self.logout()
        else:
            return self.menu_manager()

    def menu_employee(self):
        list_menu = {
            1: "Quản lý tài khoản cá nhân",
            2: "Đặt phòng",
            3: "Trả phòng",
            4: "Đăng xuất"
        }
        print(f"Chào {self.account.account1.name}, chúc bạn 1 ngày làm việc hiệu quả".center(40, "="))
        option = self.show_menu(list_menu)
        if option == 1:
            out = self.account.show_info_acc()
            if out == "back menu":
                pass
            elif out == "choice invalid":
                pass
            elif out == "input too much":
                errorsys.input_error()
            else:
                self.account.update_password(out)
                return self.login()
            return self.menu_manager()
        elif option == 2:
            print("Đặt phòng".center(40, "="))
            id_customer = int(input("Nhập cccd khách hàng: "))
            check_cccd = self.customer.check_customer(id_customer)
            info_acc = self.account.account1
            select_room = self.room.select_room()
            if select_room == "back menu":
                return self.menu_employee()
            price = self.order_room.menu_order_room(info_acc, select_room, check_cccd)
            self.customer.plus_price(price, id_customer)
            self.room.change_status_used(select_room.get("name_room"))
            return self.menu_employee()
        elif option == 3:
            out = self.order_room.display_check_out()
            if out == "back menu":
                return self.menu_manager()
            elif out == "out system":
                return self.logout()
            else:
                self.room.change_status_avai(out)
                return self.menu_employee()
        elif option == 4:
            return self.logout()
        else:
            return self.menu_manager()

    def show_menu(self, list_menu):
        print("Chose your option".center(40, "="))
        for key, val in list_menu.items():
            print(str(key) + ". " + val)
        nhap = int(input("Mời bạn nhập: "))
        if nhap in list_menu.keys():
            return nhap
        else:
            errorsys.choice_invalid()

    def logout(self):
        print("-" * 40)
        print("CẢM ƠN VÀ HẸN GẶP LẠI")
        print("-" * 40)


if __name__ == '__main__':
    run = main()
    run.login()

# order_room = OderRoomService()
# order_room.sayhello()
# acc = AccountService()
# room = RoomService()
# username = input('enter username: ')
# password = input('enter password: ')
# name = input('enter name: ')
# address = input('enter address: ')
# dob = input('enter dob: ')
# role = input('role: ')
# acc.add(data={
#     "username": username,
#     "password": md5_hash(password),
#     "name": name,
#     "address": address,
#     "dob": dob,
#     "role": role
# })
# name_room = input('enter name room: ')
# type_room = input('enter type of room: ')
# price_hour = input('enter price per hour: ')
# price_day = input('enter price per day: ')
# room_status = input('enter status of room: ')
# room.add(data={
#     "name_room": name_room,
#     "type_room": type_room,
#     "price_hour": price_hour,
#     "price_day": price_day,
#     "room_status": room_status
# })
# acc.showtable()
