from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities  
from LambdaComplex_Entities.Tables import Tables

class UserModule:
    @staticmethod
    def GetUserDetails(user_id):
        try:
            query = f"SELECT [ID], [FirstName], [LastName], [Username], [Role], [MobileNumber], [EmailID] FROM {Tables.User} WHERE ID = '{user_id}' AND IsDeleted = 0"
            users = DatabaseUtilities.GetListOf(query)
            return users[0] if users else None
        except Exception:
            raise

    @staticmethod
    def GetDeveloperNamesAndIds():
        try:
            query = f"SELECT [ID], ([FirstName] + '.' + [LastName]) as [UserName] FROM {Tables.User} WHERE lower([Role]) = 'dev' AND IsDeleted = 0"
            users = DatabaseUtilities.GetListOf(query)
            return users
        except Exception:
            raise

    @staticmethod
    def GetLeadNamesAndIds():
        try:
            query = f"SELECT [ID], ([FirstName] + '.' + [LastName]) as [UserName] FROM {Tables.User} WHERE lower([Role]) = 'lead' AND IsDeleted = 0"
            users = DatabaseUtilities.GetListOf(query)
            return users
        except Exception:
            raise
    
    @staticmethod
    def UpdateUserDetails(userDetails):
        try:
            query = f"""
                    UPDATE {Tables.User}
                    SET [FirstName] = '{userDetails["FirstName"]}',
                        [LastName] = '{userDetails["LastName"]}',
                        [UserName] = '{userDetails["UserName"]}',
                        [EmailID] = '{userDetails["EmailID"]}',
                        [CreatedOn] = [CreatedOn],
                        [ModifiedOn] = getdate(),
                        [Role] = '{userDetails["Role"]}',
                        [MobileNumber] = '{userDetails["MobileNumber"]}'
                    WHERE [ID] = '{userDetails["ID"]}';
                    """
            
            affectedRows = DatabaseUtilities.ExecuteNonQuery(query)
            return affectedRows
        except Exception:
            raise

    @staticmethod
    def CreateUser(userDetails):
        try:
            query = f"""
                    INSERT INTO {Tables.User}(
                        [FirstName],
                        [LastName],
                        [UserName],
                        [EmailID],
                        [Role],
                        [MobileNumber],
                        [Password]
                    )
                    VALUES (
                        '{userDetails["FirstName"]}',
                        '{userDetails["LastName"]}',
                        '{userDetails["UserName"]}',
                        '{userDetails["EmailID"]}',
                        '{userDetails["Role"]}',
                        '{userDetails["MobileNumber"]}',
                        HASHBYTES('SHA2_256','{userDetails["FirstName"]}.{userDetails["LastName"]}@LambdaCore')
                    )
                    """
            
            affectedRows = DatabaseUtilities.ExecuteNonQuery(query)
            return affectedRows
        except Exception:
            raise

    @staticmethod
    def ChangePassword(userDetails):
        try:
            query = f"""
                    UPDATE {Tables.User}
                    SET 
                        [Password] = HASHBYTES('SHA2_256','{userDetails["Password"]}'),
                        [ModifiedOn] = getdate()
                    WHERE [ID] = '{userDetails["ID"]}';
                    """
            
            affectedRows = DatabaseUtilities.ExecuteNonQuery(query)
            return affectedRows
        except Exception:
            raise


    