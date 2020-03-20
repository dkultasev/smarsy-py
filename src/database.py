def db_connect():
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = ""
    )