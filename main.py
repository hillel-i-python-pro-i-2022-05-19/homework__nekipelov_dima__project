import sqlite3


class UserDB:
    def __init__(self, file_db):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()

    # def user_exists(self, user_name):
    #     result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_name` = ?", (user_name,))
    #     return bool(len(result.fetchall()))

    def get_user_id(self, user_name):
        """Достаем user_id из базы по его user_name"""
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_name` = ?", (user_name,))
        return result.fetchone()[0]

    def add_user(self, user_name):
        """Добавляем пользователя"""
        self.cursor.execute("INSERT INTO `users` (`user_name`) VALUES (?)", (user_name,))
        return self.connection.commit()

    def add_record(self, user_name, operation, value):
        """Добавляем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO `rec` (`user_id`, `operation`, `value`) VALUES (?, ?, ?)", (self.get_user_id(user_name), operation == "+", value))
        return self.connection.commit()

    def get_records(self, user_name, within="all"):
        """Получаем записи о доходах/расходах"""

        if within == "day":
            result = self.cursor.execute(
                "SELECT * FROM `rec` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_name),))
        elif within == "week":
            result = self.cursor.execute(
                "SELECT * FROM `rec` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_name),))
        elif within == "month":
            result = self.cursor.execute(
                "SELECT * FROM `rec` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_name),))
        else:
            result = self.cursor.execute("SELECT * FROM `rec` WHERE `user_id` = ? ORDER BY `date`", (self.get_user_id(user_name),))
        return result.fetchall()


user_1 = UserDB('acc.db')
# user_1.add_user("kuku")
# print(user_1.user_exists("kuku"))
# user_1.add_record('kuku', '+', 12)
# user_1.add_record('kuku', '-', 4)
print(user_1.get_user_id("kuku"))
print(user_1.get_records('kuku', 'day'))
