from services.Sql_Service import Sqlservice
from error.errors import errorsys
import matplotlib.pyplot as plt


class CustomerService(Sqlservice):
    def __init__(self):
        super().__init__()
        self.table = "customers"
        self.primary_key = "id_cccd"

    def manager_customer(self):
        print("Quản lý khách hàng".center(40, "="))
        print("1. Thêm mới khách hàng")
        print("2. Cập nhật khách hàng")
        print("3. Xóa khách hàng")
        print("4. hiển thị danh sách khách hàng")
        print("5. Trở về menu")
        nhap = input("Mời bạn nhập: ")
        if nhap == "1":
            self.add_new_customer()
            return self.manager_customer()
        elif nhap == "2":
            return self.update_info_customer()
        elif nhap == "3":
            return self.delete_customer()
        elif nhap == "4":
            print("Danh sách khách hàng".center(40, "="))
            self.showtable()
            return self.manager_customer()
        elif nhap == "5":
            return "back menu"
        else:
            return "back menu"

    def update_info_customer(self):
        print("Cập nhập thông tin khách hàng".center(40, "="))
        self.showtable()
        id_cccd = input("Nhập CCCD khách hàng (Tối đa 12 số): ")
        check_id = self.check_id(id_cccd)
        if check_id is None:
            errorsys.customer_invalid()
            return self.manager_customer()
        else:
            name = input("Tên khách hàng: ")
            phone_number = input("số điện thoại: ")
            address = input("Địa chỉ: ")
            self.update(id_cccd, {
                "name": name,
                "phone_number": phone_number,
                "address": address
            })
            return self.manager_customer()

    def delete_customer(self):
        print("Xóa thông tin khách hàng".center(40, "="))
        self.showtable()
        id_cccd = input("Nhập CCCD khách hàng (Tối đa 12 số): ")
        check_id = self.check_id(id_cccd)
        if check_id is None:
            errorsys.customer_invalid()
            return self.manager_customer()
        else:
            self.delete(id_cccd)
            return self.manager_customer()

    def check_customer(self, cccd_cus):
        print("Kiểm tra thông tin khách hàng".center(40, "="))
        check_cus = self.check_id(cccd_cus)
        if check_cus != cccd_cus:
            print("Khách hàng chưa là thành viên".center(40, "*"))
            return self.add_new_customer()
        elif check_cus == cccd_cus:
            print("Khách hàng đã là thành viên".center(40, "*"))
            return cccd_cus

    def add_new_customer(self):
        print("Thêm mới khách hàng".center(40, "="))
        id_cccd = input("Nhập CCCD khách hàng (Tối đa 12 số): ")
        check_cccd = self.check_id(id_cccd)
        if check_cccd is not None:
            return self.add_new_customer()
        else:
            name = input("Họ và tên khách hàng: ")
            phone_number = input("Số điện thoại: ")
            address = input("Địa chỉ: ")
            total_price = 0
            self.add({
                "id_cccd": id_cccd,
                "name": name,
                "phone_number": phone_number,
                "address": address,
                "total_price": total_price
            })
            return id_cccd

    def get_current_total_price(self, cccd):
        sql = f"select total_price from {self.table} where {self.primary_key} = %s"
        self.cursor.execute(sql, (cccd,))
        result = self.cursor.fetchone()
        return result.get("total_price")

    def plus_price(self, price, cccd):
        total_price = int(price) + int(self.get_current_total_price(cccd))
        sql = f"update {self.table} set total_price = %s where {self.primary_key} = %s"
        self.cursor.execute(sql, (total_price, cccd))
        self.connect.commit()

    def thong_ke_total_price_of_customer(self):
        list_handle = self.take_column_in_sql(["id_cccd", "name", "total_price"])
        x_row = []
        y_row = []
        for tp in list_handle:
            x_row.append(f"{tp['name']} CCCD:{tp['id_cccd']}")
            y_row.append(int(tp['total_price']))
        y_row = list(map(int, y_row))
        for i, v in zip(x_row, y_row):
            plt.text(i, v, str(v), color='black', fontweight='bold')
        plt.bar(x_row, y_row, color="blue", width=0.3)
        plt.xlabel("Khách hàng")
        plt.ylabel("Tổng chi tiêu (triệu đồng)")
        plt.title("Thống kê tổng chi tiêu của tất cả các khách hàng")
        plt.show()
