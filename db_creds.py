class db_creds:
    MYSQL_HOST = 0
    MYSQL_USER = 0
    MYSQL_PASSWORD = 0
    MYSQL_DB = 0

    def __init__(self):
        self.MYSQL_HOST = 'mysqldb.cahzfivbuo9y.us-east-2.rds.amazonaws.com'
        self.MYSQL_USER = 'admin'
        self.MYSQL_PASSWORD = 'admin_mysql'
        self.MYSQL_DB = 'practica1'