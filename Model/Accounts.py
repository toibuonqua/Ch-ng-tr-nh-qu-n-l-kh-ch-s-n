from helpers.hashhelpers import md5_hash


class Accounts:
    def __init__(self, data):
        self.id = data.get("id")
        self.username = data.get("username")
        self.password = data.get("password")
        self.name = data.get("name")
        self.address = data.get("address")
        self.dob = data.get("dob")
        self.role = data.get("role")
        
    def get_role(self):
        if self.role == 1:
            return "Admin"
        return "Staff"

    def show_info(self):
        print("Information account".center(40, "="))
        print("Username: " + self.username)
        print("Name: " + self.name)
        print("Address: " + self.address)
        print("Date of birth: " + self.dob)
        print("Role: " + self.get_role())
        print("".center(40, "+"))
        print("1. Đổi mật khẩu")
        print("2. Trở về menu")
        nhap = input("mời bạn nhập: ")
        if nhap == "1":
            return self.change_password()
        elif nhap == "2":
            return "back menu"
        else:
            return "choice invalid"

    def change_password(self):
        print("Đổi mật khẩu".center(40, "="))
        time = 3
        while time > 0:
            input_old_pass = input("Nhập mật khẩu cũ: ")
            while md5_hash(input_old_pass) == self.password:
                input_new_pass = input("Nhập mật khẩu mới: ")
                input_new_pass1 = input("Nhập lại mật khẩu mới: ")
                time1 = 0
                while input_new_pass1 != input_new_pass:
                    print("Nhập lại mật khẩu không hợp lệ".center(40, "="))
                    input_new_pass1 = input("Nhập lại mật khẩu mới: ")
                    time1 += 1
                    if time1 == 3:
                        return "input too much"
                print("Đổi mật khẩu thành công".center(40, "*"))
                return input_new_pass1
            else:
                time = time - 1
                print("="*40)
                print("Mật khẩu cũ không hợp lệ")
                print("="*40)
        return "input too much"
