class dbTest ():
    mysql_module = "mysql+pymysql://"
    username = "root:"
    password = "root"
    address = "@localhost"
    port = ":8889"
    dbname = "/sensei"
    environment = "test"

class dbProduction ():
    mysql_module = ""
    username = ""
    password = ""
    address = ""
    port = ""
    dbname = ""
    environment = "production"

class dbDevelopment():
    mysql_module = ""
    username = ""
    password = ""
    address = ""
    port = ""
    dbname = ""
    environment = "development"

def dbConnection(environment):
    if environment == "development":
        return (dbDevelopment.mysql_module + dbDevelopment.username + dbDevelopment.password + dbDevelopment.address + dbDevelopment.port + dbDevelopment.dbname)
    elif environment == "production":
        return (dbProduction.mysql_module + dbProduction.username + dbProduction.password + dbProduction.address + dbProduction.port + dbProduction.dbname)
    else:
        return (dbTest.mysql_module + dbTest.username + dbTest.password + dbTest.address + dbTest.port + dbTest.dbname)
