class Credentials:
    RootPath = ""

    # Database Credentials
    DBUserName = "Server_Admin"
    DBPassword = "root"
    DB = "LambdaComplex"
    SERVER = "<Your SQL Server Name>"
    ConnectionString = "DRIVER={SQL Server}" + f";SERVER={SERVER};DATABASE={DB};UID={DBUserName};PWD={DBPassword}"
    # Email Credentials
    
