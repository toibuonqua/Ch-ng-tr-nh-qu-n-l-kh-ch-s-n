from connectDB.connection import Connect
from prettytable import PrettyTable


class Sqlservice:
    def __init__(self):
        self.connect = Connect().getconnect()
        self.cursor = self.connect.cursor(buffered=True, dictionary=True)
        self.table = None
        self.primary_key = None

    def add(self, data):
        values = list()
        header = ", ".join(list(data.keys()))
        for i in range(len(list(data.values()))):
            values.append("%s")
        values = ", ".join(values)
        sql = f"insert into {self.table}({header}) values({values})"
        self.cursor.execute(sql, tuple(data.values()))
        self.connect.commit()
        print("Thêm thành công".center(40, "+"))

    def update(self, id, data):
        list_set = []
        list_values = list(data.values())
        list_values.append(id)
        for x in data:
            list_set.append(f"{x} = %s")
        str_set = ", ".join(list_set)
        sql = f"update {self.table} set {str_set} where {self.primary_key} = %s"
        self.cursor.execute(sql, tuple(list_values))
        self.connect.commit()
        print("Cập nhật thành công".center(40, "+"))

    def delete(self, id):
        sql = f"delete from {self.table} where {self.primary_key} = %s"
        self.cursor.execute(sql, (id,))
        self.connect.commit()
        print("Xóa thành công".center(40, "+"))

    def showtable(self):
        sql = f"select * from {self.table}"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        my_table = PrettyTable(list(result[0].keys()))
        for x in result:
            my_table.add_row(list(x.values()))
        print(my_table)
        
    def find_by_info(self, header, value):
        sql = f"select * from {self.table} where {header} = %s"
        self.cursor.execute(sql, (value,))
        result = self.cursor.fetchone()
        try:
            return result
        except Exception:
            return None

    def take_column_in_sql(self, list_col):
        str_col = ", ".join(list_col)
        sql = f"select {str_col} from {self.table}"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def check_id(self, id):
        sql = f"select * from {self.table} where {self.primary_key} = %s"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        try:
            return result.get(self.primary_key)
        except Exception:
            return None

    def get_max_id(self):
        sql = f'select max({self.primary_key}) as current_id from {self.table}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result.get("current_id")

    def sayhello(self):
        print("hello")

    def datediff(self, id):
        pass
