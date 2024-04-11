from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables


class WorkTimeLineModule:
    @staticmethod
    def CreateWorkTimeLineEntry(message,userId,recordId):
        try:
            query = f"""
                INSERT INTO {Tables.WorkTimeLine}
                    (
                    [Message]
                    ,[RecordID]
                    ,[CreatedBy]
                    ,[ModifiedBy]
                    )
                VALUES
                    (
                    '{message}'
                    ,'{recordId}'
                    ,'{userId}'
                    ,'{userId}'
                )
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    
    @staticmethod
    def GetWorkTimeLineForDate(userId,dateString):
        try:
            query = f"""            
            SELECT 
                WT.[ID] as WorkTimeLineID,
                WT.[Message],
                WT.[RecordID],
                cast(Format(WT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) as [CreatedOn],
                MDT.[ID] as [AffectedRecordID],
                MDT.[Name] as [AffectedEntityName],
                MDT.[AffectedModule],
                UM.[ID] as [ActionDoneByID],
                UM.[FirstName] + '.' + UM.[LastName] as [ActionDoneBy]
            FROM [LambdaComplex].[dbo].[LambdaComplex_WorkTimeline_Trn_Tbl] WT
            INNER JOIN
            (
                SELECT 
                    [ID],
                    [FirstName]+'.'+[LastName] as [Name],
                    'USER' as [AffectedModule] 
                    FROM {Tables.User} 
                    WHERE [IsDeleted] = 0
                UNION ALL
                SELECT 
                    [ID],
                    [Name],'PROJECT' as [AffectedModule] 
                    FROM {Tables.Project} 
                    WHERE [IsDeleted] = 0
                UNION ALL
                SELECT 
                    [ID],
                    [Name],
                    'MILESTONE' as [AffectedModule] 
                    FROM {Tables.Milestone} 
                    WHERE [IsDeleted] = 0
                UNION ALL
                SELECT 
                    [ID],
                    [Name],
                    'GOAL' as [AffectedModule] 
                    FROM {Tables.Goal} 
                    WHERE [IsDeleted] = 0
                UNION ALL
                SELECT 
                    [ID],
                    [Name],
                    'TASK' as [AffectedModule] FROM {Tables.Task} 
                    WHERE [IsDeleted] = 0
                UNION ALL
                SELECT 
                    [ID],
                    [TeamName] as [Name],
                    'TEAM' as [AffectedModule] 
                    FROM {Tables.Team} WHERE 
                    [IsDeleted] = 0
            ) 
            as MDT on MDT.[ID] = WT.[RecordID]
            INNER JOIN {Tables.User} UM on WT.[CreatedBy] = UM.[ID]
            WHERE 
            WT.[IsDeleted] = 0 AND
            WT.[CreatedBy] = '{userId}' AND
            Format(WT.[CreatedOn],'yyyy-MM-dd') = Format(Cast('{dateString.replace('L','-')}' as datetime),'yyyy-MM-dd')

            ORDER BY WT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)

        except Exception:
            raise

    @staticmethod
    def GetWorkTimelineGroupedByDate(userId):
        try:
            query = f"""               
                SELECT
                    CAST(Format([CreatedOn],'yyyy-MM-dd') as varchar(30)) as [date],
                    CAST(count(*) as varchar(10)) + ' Activities done' as [eventName],
                    'badge bg-success' as [className],
                    'green' as [dateColor]
                FROM {Tables.WorkTimeLine} 
                WHERE 
                    CreatedBy = '{userId}' AND
                    IsDeleted = 0
                GROUP BY FORMAT([CreatedOn], 'yyyy-MM-dd');
 
            """
            return DatabaseUtilities.GetListOf(query)

        except Exception:
            raise