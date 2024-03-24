from LambdaComplex_Entities.Credentials import Credentials
import pyodbc

class DatabaseUtilities:
    @staticmethod
    def CheckConnection():
        try:
            connection_string = Credentials.ConnectionString
            with pyodbc.connect(connection_string) as conn:
                return True
        except Exception:
            raise Exception

    @staticmethod
    def GetConnection():
        try:
            connection_string = Credentials.ConnectionString
            return pyodbc.connect(connection_string)
        except Exception:
            raise Exception

    @staticmethod
    def GetDataTable(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:            
                if connection:
                    return connection.execute(query).fetchall()
                return []
        except Exception:
            raise Exception

    @staticmethod
    def GetListOf(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:   
                if connection:
                    cursor = connection.execute(query)
                    dt = cursor.fetchall()
                    results = []
                    
                    columns = [column[0] for column in cursor.description]
                    for row in dt:
                        results.append(dict(zip(columns, row)))
                return results
        except Exception:
            raise Exception
        
    @staticmethod
    def ExecuteNonQuery(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:   
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.rowcount
                    return result
        except Exception:
            raise Exception