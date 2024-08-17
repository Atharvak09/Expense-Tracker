import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS expense_record (item_name text, item_price float, purchase_date date, category text)"
        )
        self.conn.commit()

    def fetch_records(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert_record(self, item_name, item_price, purchase_date, category):
        self.cur.execute("INSERT INTO expense_record VALUES (?, ?, ?, ?)",
                         (item_name, item_price, purchase_date, category))
        self.conn.commit()

    def remove_record(self, rwid):
        self.cur.execute("DELETE FROM expense_record WHERE rowid=?", (rwid,))
        self.conn.commit()

    def update_record(self, item_name, item_price, purchase_date, category, rid):
        self.cur.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ?, category = ? WHERE rowid = ?",
                         (item_name, item_price, purchase_date, category, rid))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
