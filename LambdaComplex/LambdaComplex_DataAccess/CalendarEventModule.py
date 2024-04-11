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
            return DatabaseUtilities.GetListOf(query)            
        except Exception:
            raise

    @staticmethod
    def GetGroupedCalendarEvent(userId):
        try:
            # already expire out of date events
            CalendarEventModule.ExpireOutOfDateEvents()

            query = f"""
                SELECT
                CAST(Format([EventDate],'yyyy-MM-dd') as varchar(30)) as [date],
                CAST(count(*) as varchar(10)) + ' Event(s)' as [eventName],
                'badge bg-success' as [className],
                'green' as [dateColor]
                FROM {Tables.CalendarEvent} 
                WHERE 
                    [CreatedBy] = '{userId}' AND
                    [IsDeleted] = 0
                GROUP BY [EventDate];
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetCalendarEventsForEventDate(userId,eventDate):
        try:
            # already expire out of date events
            CalendarEventModule.ExpireOutOfDateEvents()

            query = f"""
                SELECT
                [ID]
                ,[EventName]
                ,cast([EventDescription] as xml).value('.[1]','nvarchar(max)') as [EventDescription]
                ,cast(Format([EventDate],'yyyy-MM-dd') as varchar(30)) as [EventDate]
                ,cast(Format([CreatedOn],'yyyy-MM-dd') as varchar(30)) as [CreatedOn]
                ,[EventPriority]
                ,[EventTime]
                ,[IsExpired]
                FROM {Tables.CalendarEvent} 
                WHERE [CreatedBy] = '{userId}' and [EventDate] = CAST('{eventDate}' as datetime) And IsDeleted = 0
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetEventData(recordId):
        try:
            # already expire out of date events
            CalendarEventModule.ExpireOutOfDateEvents()

            query = f"""
                SELECT
                [ID]
                ,[EventName]
                ,[EventDescription]
                ,[EventDate]
                ,[CreatedOn]
                ,[EventPriority]
                ,[EventTime]
                FROM {Tables.CalendarEvent} 
                WHERE [ID] = '{recordId}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.GetListOf(query)
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
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise


    @staticmethod
    def ExpireOutOfDateEvents():
        try:
            query = f"""
            UPDATE {Tables.CalendarEvent}
            SET 
                [IsExpired] = 1,
                [ModifiedOn] = getdate(),
                [CreatedOn] = [CreatedOn],
                [ModifiedBy] = 'SYSTEM'
            WHERE [EventDate] < GetDate()
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
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
           ,[EventPriority]
           ,[EventTime]
           ,[EventName])
            VALUES
           ('{eventDetails["EventDescription"]}'
           ,'{eventDetails["EventDate"]}'           
           ,'{eventDetails["UserId"]}'           
           ,'{eventDetails["UserId"]}'
           ,'{eventDetails["EventPriority"]}'
           ,'{eventDetails["EventTime"]}'
           ,'{eventDetails["EventName"]}');
            """
            return DatabaseUtilities.ExecuteNonQuery(query)            
        except Exception:
            raise
            
    @staticmethod
    def UpdateCalendarEvent(eventDetails):
        try:
            query = f"""
            UPDATE {Tables.CalendarEvent}
            SET [EventDescription] = '{eventDetails["EventDescription"]}',
                [EventDate] = '{eventDetails["EventDate"]}',
                [ModifiedBy] = '{eventDetails["UserId"]}',
                [EventPriority] = '{eventDetails["EventPriority"]}',
                [EventTime] = '{eventDetails["EventTime"]}',
                [EventName] = '{eventDetails["EventName"]}'
            WHERE [ID] = '{eventDetails["EventId"]}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def DeleteCalendarEvent(userId,recordId):
        try:
            query = f"""
            UPDATE {Tables.CalendarEvent}
            SET 
                [IsDeleted] = 1,
                [ModifiedOn] = getdate(),
                [ModifiedBy] = '{userId}',
                [CreatedOn] = [CreatedOn]
            WHERE [ID] = '{recordId}'
            """
            return DatabaseUtilities.ExecuteNonQuery(query)            
        except Exception:
            raise

