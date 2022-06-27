from services.Sql_Service import Sqlservice
from helpers.hashhelpers import md5_hash
from Model.Accounts import Accounts
from error.errors import errorsys


class AccountService(Sqlservice):
    def __init__(self):
        super().__init__()
        self.table = "accounts"
        self.account1 = None
        self.primary_key = "id"

    def check_login(self, username, password):
        sql = f"select * from {self.table} where username = %s and password = %s"
        self.cursor.execute(sql, (username, md5_hash(password)))
        result = self.cursor.fetchone()
        if result is None:
            return "LoginFail"
        else:
            self.account1 = Accounts(result)
            return result.get("role")

    def show_info_acc(self):
        return self.account1.show_info()

    def update_password(self, password):
        sql = f"update {self.table} set password = %s where id = {self.account1.id}"
        self.cursor.execute(sql, (md5_hash(password),))
        self.connect.commit()

    def manager_acc(self):
        print("Quản lý tài khoản hệ thống".center(40, "="))
        print("1. Thêm tài khoản")
        print("2. Cập nhập tài khoản")
        print("3. Xóa tài khoản")
        print("4. Trở về menu")
        print("5. Đăng xuất")
        press = input("Mời bạn nhập: ")
        if press == "1":
            print("Thêm tài khoản".center(40, "="))
            user = input("Nhập username: ")
            password = input("Nhập password: ")
            name = input("Nhập họ và tên: ")
            address = input("Nhập địa chỉ: ")
            dob = input("Nhập ngày tháng năm sinh: ")
            role = int(input("Nhập cấp chức vụ: "))
            self.add({
                "username": user,
                "password": md5_hash(password),
                "name": name,
                "address": address,
                "dob": dob,
                "role": role
            })
            return self.manager_acc()
        elif press == "2":
            print("Cập nhật tài khoản".center(40, "="))
            self.showtable()
            id = input("Nhập id tài khoản: ")
            check_id = self.check_id(id)
            if check_id is None:
                errorsys.id_invalid()
                return self.manager_acc()
            else:
                print("Cập nhập thông tin".center(40, "="))
                name = input("Nhập họ và tên: ")
                address = input("Nhập địa chỉ: ")
                dob = input("Nhập ngày tháng năm sinh: ")
                role = int(input("Nhập cấp chức vụ: "))
                self.update(id, {
                    "name": name,
                    "address": address,
                    "dob": dob,
                    "role": role
                })
                return self.manager_acc()
        elif press == "3":
            print("Xóa tài khoản".center(40, "="))
            self.showtable()
            id = input("Nhập id tài khoản: ")
            check_id = self.check_id(id)
            if check_id is None:
                errorsys.id_invalid()
                return self.manager_acc()
            else:
                self.delete(id)
                return self.manager_acc()
        elif press == "4":
            return "back menu"
        elif press == "5":
            return "logout"
        else:
            return "back menu"
