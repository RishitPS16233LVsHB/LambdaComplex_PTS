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
            raise

    @staticmethod
    def GetConnection():
        try:
            connection_string = Credentials.ConnectionString
            return pyodbc.connect(connection_string)
        except Exception:
            raise

    @staticmethod
    def GetDataTable(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:            
                if connection:
                    return connection.execute(query).fetchall()
                return []
        except Exception:
            raise

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
                    cursor.close()
                return results
        except Exception:
            raise
        
    @staticmethod
    def ExecuteNonQuery(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:   
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.rowcount
                    cursor.close()
                    return result
        except Exception:
            raise

    @staticmethod
    def ExecuteScalar(query):
        try:
            with DatabaseUtilities.GetConnection() as connection:   
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchone()[0]
                    cursor.close()
                    return result
        except Exception:
            raise