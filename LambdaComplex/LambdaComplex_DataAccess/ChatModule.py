from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables

class ChatModule:
    @staticmethod
    def CreateChat(chatDetails):
        try:
            query = f"""
                INSERT INTO {Tables.Chat} 
                (Name,FirstUser,SecondUser,CreatedBy,ModifiedBy,IsDeleted)
                VALUES
                ('{chatDetails["Name"]}','{chatDetails["FirstUser"]}','{chatDetails["SecondUser"]}','{chatDetails["FirstUser"]}','{chatDetails["FirstUser"]}',0)
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            return 1
        except Exception:
            raise
        
    def DeleteChat(chatId, userId):
        try:
            query = f"""
            UPDATE {Tables.Chat} SET [IsDeleted] = 1,ModifiedOn = getdate(), ModifiedBy = '{userId}' 
            WHERE [ID] = '{chatId}'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            return 1
        except Exception:
            raise
        
    def GetChats(userId):
        try:
            query = f"""
            SELECT 
                C.ID as ChatID,
                C.Name as ChatName,
                C.SecondUser as SecondUserID,
                C.CreatedOn as ChatCreatedOn,
                C.ModifiedOn as ChatModifiedOn,                
                (U.FirstName + '.' + U.LastName) as SecondUserName,
                (LU.FirstName + '.' + LU.LastName) as LatestChangedBy,                               
            FROM {Tables.Chat} C 
            INNER JOIN {Tables.User} U WHERE C.[SecondUser] = U.[ID] AND U.[IsDeleted] = 0
            INNER JOIN {Tables.User} LU WHERE C.[ModifiedBy] = LU.[ID] AND U.[IsDeleted] = 0 
            WHERE C.[IsDeleted] = 0 AND C.[FirstUser] = '{userId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
        
    def GetChatMessagesForChat(chatId):
        try:
            query = f"""
            SELECT 
                CM.[ID] as ChatMessageID,
                CM.[Message] as ChatMessageText,                
                CM.SentByUser,
                (SU.FirstName + '.' + SU.LastName)  as SentUserName,
                CM.RecievedByUser,
                (RU.FirstName + '.' + RU.LastName)  as RecivedByUser                            
            FROM {Tables.ChatMessage} CM
            INNER JOIN {Tables.User} SU WHERE CM.[SentByUser] = SU.[ID] AND U.[IsDeleted] = 0
            INNER JOIN {Tables.User} RU WHERE CM.[RecievedByUser] = RU.[ID] AND U.[IsDeleted] = 0
            WHERE CM.[ChatID] = '{chatId}'
            """
            return DatabaseUtilities.GetListOf(query);
        except Exception:
            raise

    def AddMessageToChat(chatMessageDetails):
        try:
            query = f"""
                INSERT INTO {Tables.ChatMessage}
                (Message,SentByUser,RecievedByUser,CreatedByUser,ModifiedByUser,ChatID,IsDeleted)
                VALUES
                ('{chatMessageDetails["Message"]}','{chatMessageDetails["SentByUser"]}'
                '{chatMessageDetails["RecievedByUser"]}','{chatMessageDetails['SentByUser']}',
                '{chatMessageDetails['SentByUser']}','{chatMessageDetails['SentByUser']}',
                '{chatMessageDetails['ChatId']}',0);
                
            
            """
            DatabaseUtilities.ExecuteNonQuery(query);
            
            query = f"""            
                UPDATE {Tables.Chat}
                SET [ModifiedOn] = getdate(), [ModifiedBy] = '{chatMessageDetails['SentByUser']}'
                WHERE 
                [ID] = '{chatMessageDetails['ChatId']}' AND [IsDeleted] = 0;
            """
            DatabaseUtilities.ExecuteNonQuery(query);
            
            return 1
        except Exception:
            raise
        
    def RemoveMessageToChat(messageID,chatID,userID):
        try:            
            query = f"""            
            UPDATE {Tables.ChatMessage} SET [IsDeleted] = 1,[ModifiedOn] = getdate(), [ModifiedBy] = '{userID}' 
            WHERE [ID] = '{messageID} AND [chatID] = '{chatID}'
            """
            DatabaseUtilities.ExecuteNonQuery(query);   
            
            query = f"""            
                UPDATE {Tables.Chat}
                SET [ModifiedOn] = getdate(), [ModifiedBy] = '{userID}'
                WHERE 
                [ID] = '{chatID}' AND [IsDeleted] = 0;
            """
            DatabaseUtilities.ExecuteNonQuery(query);         
            return 1
        except Exception:
            raise