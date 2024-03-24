from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables

class LoginModule:
    @staticmethod
    def CheckLogin(username, password):
        try:
            query = f"SELECT [ID], [Username], [Role] FROM {Tables.User} WHERE ([UserName] = '{username}' OR [EmailID] = '{username}') AND [Password] = HASHBYTES('SHA2_256','{password}') AND IsDeleted = 0"
            users = DatabaseUtilities.GetListOf(query)
            return users[0] if users else None
        except Exception:
            raise