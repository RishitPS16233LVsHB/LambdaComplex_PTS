from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables

class GoalModule:
    @staticmethod
    def CreateGoal(goalData):
        try:
            query = f"""
            declare @InsertID table(ID varchar(36));
            declare @cngInsertID varchar(36);
            INSERT INTO {Tables.Goal}
            ([Name]
            ,[Description]
            ,[RunningStatus]
            ,[CreatedBy]
            ,[ModifiedBy]
            ,[IsStable]
            ,[Version]
            ,[ReportingStatus]
            ,[Deadline]
            ,[Remarks]
            ,[Rating]
            ,[ParentID]
            ,[AssignedTo])
        OUTPUT Inserted.ID into @InsertID
        VALUES
            ('{goalData["GoalName"]}'
            ,'{goalData["GoalDescription"]}'
            ,-1   
            ,'{goalData["UserID"]}'
            ,'{goalData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{goalData["GoalDeadLine"]}' as datetime)
            ,'{goalData["GoalRemarks"]}'
            ,{goalData["GoalRating"]}
            ,'{goalData["ParentID"]}'
            ,'{goalData["AssignedTo"]}');
            
            select @cngInsertID = ID from @InsertID;
            
            INSERT INTO {Tables.GoalChanges}
            ([RecordID]
            ,[Name]
            ,[Description]
            ,[RunningStatus]
            ,[CreatedBy]
            ,[ModifiedBy]
            ,[IsStable]
            ,[Version]
            ,[ReportingStatus]
            ,[Deadline]
            ,[Remarks]
            ,[Rating]
            ,[ParentID]
            ,[AssignedTo])
        VALUES
            (@cngInsertID
            ,'{goalData["GoalName"]}'
            ,'{goalData["GoalDescription"]}'
            ,-1   
            ,'{goalData["UserID"]}'
            ,'{goalData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{goalData["GoalDeadLine"]}' as datetime)
            ,'{goalData["GoalRemarks"]}'
            ,{goalData["GoalRating"]}
            ,'{goalData["ParentID"]}'
            ,'{goalData["AssignedTo"]}');
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def ParentUpdateGoal(goalData):       
        try:
            query = f"""
                INSERT INTO {Tables.GoalChanges}
                ([RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,[ParentID]
                ,[AssignedTo])
                 VALUES
                ('{goalData["RecordID"]}'
                ,'{goalData["GoalName"]}'
                ,'{goalData["GoalDescription"]}'
                ,-1   
                ,'{goalData["UserID"]}'
                ,'{goalData["UserID"]}'
                ,1
                ,1
                ,'PAR'
                ,cast('{goalData["GoalDeadLine"]}' as datetime)
                ,'{goalData["GoalRemarks"]}'
                ,{goalData["GoalRating"]}
                ,'{goalData["ParentID"]}'
                ,'{goalData["AssignedTo"]}');
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def GetGoalNameID(userId):        
        try:
            query = f"""
                SELECT 
                [ID],
                [Name]
                FROM {Tables.Goal}
                WHERE [IsDeleted] = 0 AND
                [CreatedBy] = '{userId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
    
    @staticmethod
    def GetLatestGoalsForAdmins(parentId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.GoalChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Goal changes
                SELECT 
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,CAST(GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,CAST(FORMAT(GCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[ReportingStatus]                    
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                    ,GCT.[AssignedTo]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.GoalChanges} GCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = GCT.RecordID AND 
                    LT.LatestTime = GCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = GCT.[CreatedBy] 
                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = GCT.[AssignedTo] 
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[ParentID] = '{parentId}' AND
                    GCT.[RunningStatus] = -1
            """            
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestGoalForLead(parentId,userId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.GoalChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Goal changes
                SELECT 
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,GCT.[AssignedTo]
                    ,CAST( GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,CAST(FORMAT(GCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[ReportingStatus]
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.GoalChanges} GCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = GCT.RecordID AND 
                    LT.LatestTime = GCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = GCT.[CreatedBy] 
                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = GCT.[AssignedTo] 
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[RunningStatus] = -1 AND
                    GCT.[CreatedBy] = '{userId}' AND
                    GCT.[ParentID] = '{parentId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestGoalForDev(parentId,userId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.GoalChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1 AND
                        [IsStable] = 1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Goal changes
                SELECT 
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,GCT.[AssignedTo]
                    ,CAST( GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,CAST(FORMAT(GCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[ReportingStatus]
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]                    
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.GoalChanges} GCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = GCT.RecordID AND 
                    LT.LatestTime = GCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = GCT.[CreatedBy] 
                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = GCT.[AssignedTo] 
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[RunningStatus] = -1 AND
                    GCT.[AssignedTo] = '{userId}' AND
                    GCT.[ParentID] = '{parentId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
    
    @staticmethod
    def AbandonGoal(goalChangeId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.GoalChanges}
                            (
                            [ID]
                            ,[RecordID]
                            ,[Name]
                            ,[Description]
                            ,[RunningStatus]
                            ,[AssignedTo]
                            ,[ParentID]
                            ,[CreatedBy]
                            ,[ModifiedBy]
                            ,[IsStable]
                            ,[Version]
                            ,[ReportingStatus]
                            ,[Deadline]
                            ,[Remarks]
                            ,[Rating]
                            ,[CreatedOn]
                            ,[ModifiedOn]
                            )
                        SELECT 
                        TOP 1
                            '{goalChangeId}' as [ID]
                            ,[RecordID]
                            ,[Name]
                            ,[Description]
                            ,-1 as [RunningStatus]
                            ,[AssignedTo]
                            ,[ParentID]
                            ,'{userId}' as [CreatedBy]
                            ,'{userId}' as [ModifiedBy]
                            ,1 as [IsStable]
                            ,1 as [Version] 
                            ,'ABD' as [ReportingStatus]
                            ,[Deadline]
                            ,[Remarks]
                            ,[Rating]
                            ,getdate() as [CreatedOn]
                            ,getdate() as [ModifiedOn]
                        FROM {Tables.GoalChanges}
                        WHERE ID = '{goalChangeId}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    
    @staticmethod
    def FinishGoal(goalChangeId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.GoalChanges}
                            (
                            [ID]
                            ,[RecordID]
                            ,[Name]
                            ,[Description]
                            ,[RunningStatus]
                            ,[AssignedTo]
                            ,[ParentID]
                            ,[CreatedBy]
                            ,[ModifiedBy]
                            ,[IsStable]
                            ,[Version]
                            ,[ReportingStatus]
                            ,[Deadline]
                            ,[Remarks]
                            ,[Rating]
                            ,[CreatedOn]
                            ,[ModifiedOn]
                            )
                        SELECT 
                        TOP 1
                            '{goalChangeId}' as [ID]
                            ,[RecordID]
                            ,[Name]
                            ,[Description]
                            ,-1 as [RunningStatus]
                            ,[AssignedTo]
                            ,[ParentID]
                            ,'{userId}' as [CreatedBy]
                            ,'{userId}' as [ModifiedBy]
                            ,1 as [IsStable]
                            ,1 as [Version] 
                            ,'CMP' as [ReportingStatus]
                            ,[Deadline]
                            ,[Remarks]
                            ,[Rating]
                            ,getdate() as [CreatedOn]
                            ,getdate() as [ModifiedOn]
                        FROM {Tables.GoalChanges}
                        WHERE ID = '{goalChangeId}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def GetMacroHistory(goalId):        
        try:
            query = f"""
                 SELECT 
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,CAST( GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,CAST(FORMAT(GCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[ReportingStatus]                    
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.GoalChanges} GCT
                INNER JOIN 
                    {Tables.User} UM ON GCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON GCT.[AssignedTo] = UM2.[ID]
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[RecordID] = '{goalId}' AND
                    GCT.[IsStable] = 1
                ORDER BY
                    GCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
    
    @staticmethod
    def GetMicroHistory(goalId):        
        try:
            query = f"""
                 SELECT 
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,CAST( GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,CAST(FORMAT(GCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[ReportingStatus]                    
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.GoalChanges} GCT
                INNER JOIN 
                    {Tables.User} UM ON GCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON GCT.[AssignedTo] = UM2.[ID]
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[RecordID] = '{goalId}'
                ORDER BY
                    GCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestStableVersionOfGoal(goalId):
        try:
            query = f"""
                 SELECT 
                    TOP (1)
                    GCT.[ID]
                    ,GCT.[RecordID]
                    ,GCT.[Name]
                    ,CAST(GCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,GCT.[CreatedBy]
                    ,GCT.[CreatedOn]
                    ,GCT.[IsStable]
                    ,GCT.[AssignedTo]
                    ,GCT.[ReportingStatus]
                    ,CAST(FORMAT(GCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,GCT.[Rating]
                    ,GCT.[Remarks]
                FROM 
                    {Tables.GoalChanges} GCT
                WHERE 
                    GCT.[IsDeleted] = 0 AND
                    GCT.[RecordID] = '{goalId}' AND
                    GCT.[IsStable] = 1 AND
                    GCT.[RunningStatus] = -1
                ORDER BY
                    GCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
        
    @staticmethod
    def Reversion(goalChangeId,userId):
        try:
            # insert a reversion flag record 
            query = f"""            
           INSERT INTO {Tables.GoalChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,[CreatedOn]
                ,[ModifiedOn]
                )
            SELECT 
            TOP 1
                '{goalChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,0 as [RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,'{userId}' as [CreatedBy]
                ,'{userId}' as [ModifiedBy]
                ,0 as [IsStable]
                ,1 as [Version] 
                ,'RVN' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.GoalChanges}
            WHERE ID = '{goalChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.GoalChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,[CreatedOn]
                ,[ModifiedOn]
                )
            SELECT 
            TOP 1
                '{goalChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,'{userId}' as [CreatedBy]
                ,'{userId}' as [ModifiedBy]
                ,1 as [IsStable]
                ,1 as [Version] 
                ,'PAR' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.GoalChanges}
            WHERE ID = '{goalChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def Reboot(goalId,userId):
        try:
            # insert a reboot flag record 
            query = f"""            
           INSERT INTO {Tables.GoalChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,[CreatedOn]
                ,[ModifiedOn]
                )
            SELECT 
            TOP 1
                '{goalId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,0 as [RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,'{userId}' as [CreatedBy]
                ,'{userId}' as [ModifiedBy]
                ,0 as [IsStable]
                ,1 as [Version] 
                ,'RBT' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.GoalChanges}
            WHERE 
                [RecordID] = '{goalId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.GoalChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,[CreatedOn]
                ,[ModifiedOn]
                )
            SELECT 
            TOP 1
                '{goalId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                ,[AssignedTo]
                ,[ParentID]
                ,'{userId}' as [CreatedBy]
                ,'{userId}' as [ModifiedBy]
                ,1 as [IsStable]
                ,1 as [Version] 
                ,'PAR' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.GoalChanges}
            WHERE 
                [RecordID] = '{goalId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    