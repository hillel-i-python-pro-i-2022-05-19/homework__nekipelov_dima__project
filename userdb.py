import sqlite3


class UserDB:
    def __init__(self, file_db: str):
        self.connection = sqlite3.connect(file_db)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_name: str) -> bool:
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_name` = ?", (user_name,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_name: str) -> int:
        """Get user_id from database by user_name"""
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_name` = ?", (user_name,))
        return result.fetchone()[0]

    def add_user(self, user_name: str) -> None:
        """Add new user to database"""
        self.cursor.execute("INSERT INTO `users` (`user_name`) VALUES (?)", (user_name,))
        return self.connection.commit()

    def add_record(self, user_name: str, operation: str, value: int) -> None:
        """Add new spend/earn record to database"""
        self.cursor.execute("INSERT INTO `rec` (`user_id`, `operation`, `value`) VALUES (?, ?, ?)", (self.get_user_id(user_name), operation == "+", value))
        return self.connection.commit()

    def get_records(self, user_name: str, within="all") -> list:
        """Get spend/earn record from database"""

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
