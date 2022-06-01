from userdb import UserDB


def main(db_name, user_name):
    """Just to check if it works"""
    user = UserDB(db_name)
    print(user.user_exists(user_name))


if __name__ == "__main__":
    main("acc.db", "kuku")
