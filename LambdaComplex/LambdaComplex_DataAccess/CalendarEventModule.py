from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables

class CalendarEventModule:
    
    @staticmethod
    def GetCalendarEvent(userId):
        try:
            # already expire out of date events
            CalendarEventModule.ExpireOutOfDateEvents()

            query = f"""
                SELECT
                [ID]
                ,[EventDescription]
                ,[EventDate]
                ,[CreatedOn]
                ,[EventPriority]
                FROM {Tables.CalendarEvent} Where CreatedBy = '{userId}' and IsDeleted = 0;
            """
            events = DatabaseUtilities.GetListOf(query)
            return events if events else None
        except Exception:
            raise

    @staticmethod
    def GetPriorityEventCount(userId):
        try:
            query = f"""
                SELECT
                COUNT(*) PriorityEvents
                FROM {Tables.CalendarEvent} Where CreatedBy = '{userId}' and EventPriority = 'HIGH' and IsDeleted = 0;
            """
            events = DatabaseUtilities.GetListOf(query)
            return events if events else 0
        except Exception:
            raise


    @staticmethod
    def ExpireOutOfDateEvents():
        try:
            query = f"""
            UPDATE {Tables.CalendarEvent}
            SET 
                [IsDeleted] = 1,
                [ModifiedOn] = getdate(),
                [ModifiedBy] = 'SYSTEM'
            WHERE [EventDate] < GetDate()
            """

            rowsAffected = DatabaseUtilities.ExecuteNonQuery(query)
            return rowsAffected
        except Exception:
            raise

    @staticmethod
    def CreateCalendarEvent(eventDetails):
        try:
            query = f"""
            INSERT INTO {Tables.CalendarEvent}
           ([EventDescription]
           ,[EventDate]
           ,[CreatedBy]
           ,[ModifiedBy]
           ,[EventPriority])
            VALUES
           ('{eventDetails["EventDescription"]}'
           ,'{eventDetails["EventDate"]}'           
           ,'{eventDetails["UserId"]}'           
           ,'{eventDetails["UserId"]}'
           ,'{eventDetails["EventPriority"]}')
            """

            rowsAffected = DatabaseUtilities.ExecuteNonQuery(query)
            return True if rowsAffected == 1 else False
        except Exception:
            raise

    @staticmethod
    def DeleteCalendarEvent(eventDetails):
        try:
            query = f"""
            UPDATE {Tables.CalendarEvent}
            SET 
                [IsDeleted] = 1,
                [ModifiedOn] = getdate(),
                [ModifiedBy] = '{eventDetails["UserId"]}'
            WHERE [ID] = '{eventDetails["EventId"]}'
            """

            rowsAffected = DatabaseUtilities.ExecuteNonQuery(query)
            return True if rowsAffected == 1 else False
        except Exception:
            raise

