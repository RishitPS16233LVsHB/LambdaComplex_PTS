from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_DataAccess.WorkTimeLineModule import WorkTimeLineModule
from LambdaComplex_Entities.Tables import Tables

class TaskModule:
    @staticmethod
    def CreateTask(taskData):
        try:
            query = f"""
            SET NOCOUNT ON;
            declare @InsertID table(ID varchar(36));
            declare @cngInsertID varchar(36);
            INSERT INTO {Tables.Task}
            ([Name]
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
            ,[Rating])
        OUTPUT Inserted.ID into @InsertID
        VALUES
            ('{taskData["TaskName"]}'
            ,'{taskData["TaskDescription"]}'
            ,-1
            ,'{taskData["AssignedTo"]}'   
            ,'{taskData["ParentID"]}'
            ,'{taskData["UserID"]}'
            ,'{taskData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{taskData["TaskDeadLine"]}' as datetime)
            ,'{taskData["TaskRemarks"]}'
            ,{taskData["TaskRating"]});
            
            select @cngInsertID = ID from @InsertID;
            
            INSERT INTO {Tables.TaskChanges}
            ([RecordID]
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
            ,[Rating])
        VALUES
            (@cngInsertID
            ,'{taskData["TaskName"]}'
            ,'{taskData["TaskDescription"]}'
            ,-1   
            ,'{taskData["AssignedTo"]}' 
            ,'{taskData["ParentID"]}'
            ,'{taskData["UserID"]}'
            ,'{taskData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{taskData["TaskDeadLine"]}' as datetime)
            ,'{taskData["TaskRemarks"]}'
            ,{taskData["TaskRating"]});

            SELECT @cngInsertID as [ID]
            """
            insertID = DatabaseUtilities.ExecuteScalar(query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Created a task named: {taskData["TaskName"]}""",taskData["UserID"],insertID)
            return 1
        except Exception:
            raise

    @staticmethod
    def ParentUpdateTask(taskData):       
        try:
            query = f"""
                INSERT INTO {Tables.TaskChanges}
                ([RecordID]
                ,[Name]
                ,[Description]
                ,[AssignedTo]
                ,[ParentID]
                ,[RunningStatus]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating])
                 VALUES
                ('{taskData["RecordID"]}'
                ,'{taskData["TaskName"]}'
                ,'{taskData["TaskDescription"]}'
                ,'{taskData["AssignedTo"]}' 
                ,'{taskData["ParentID"]}'
                ,-1   
                ,'{taskData["UserID"]}'
                ,'{taskData["UserID"]}'
                ,1
                ,1
                ,'PAR'
                ,cast('{taskData["TaskDeadLine"]}' as datetime)
                ,'{taskData["TaskRemarks"]}'
                ,{taskData["TaskRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)

            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Updated a task named: {taskData["TaskName"]}""",taskData["UserID"],taskData["RecordID"])

            return 
        except Exception:
            raise

    @staticmethod
    def ChildCHRUpdateTask(taskData):       
        try:
            query = f"""
                INSERT INTO {Tables.TaskChanges}
                ([RecordID]
                ,[Name]
                ,[Description]
                ,[AssignedTo]
                ,[ParentID]
                ,[RunningStatus]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating])
                 VALUES
                ('{taskData["RecordID"]}'
                ,'{taskData["TaskName"]}'
                ,'{taskData["TaskDescription"]}'
                ,'{taskData["AssignedTo"]}' 
                ,'{taskData["ParentID"]}'
                ,-1   
                ,'{taskData["CreatedBy"]}'
                ,'{taskData["UserID"]}'
                ,1
                ,1
                ,'CHR'
                ,cast('{taskData["TaskDeadLine"]}' as datetime)
                ,'{taskData["TaskRemarks"]}'
                ,{taskData["TaskRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)

            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Applied for change request for task named: {taskData["TaskName"]}""",taskData["UserID"],taskData["RecordID"])

            return 1
        except Exception:
            raise

    @staticmethod
    def ChildPGRUpdateTask(taskData):       
        try:
            query = f"""
                INSERT INTO {Tables.TaskChanges}
                ([RecordID]
                ,[Name]
                ,[Description]
                ,[AssignedTo]
                ,[ParentID]
                ,[RunningStatus]
                ,[CreatedBy]
                ,[ModifiedBy]
                ,[IsStable]
                ,[Version]
                ,[ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating])
                 VALUES
                ('{taskData["RecordID"]}'
                ,'{taskData["TaskName"]}'
                ,'{taskData["TaskDescription"]}'
                ,'{taskData["AssignedTo"]}' 
                ,'{taskData["ParentID"]}'
                ,-1   
                ,'{taskData["CreatedBy"]}'
                ,'{taskData["UserID"]}'
                ,1
                ,1
                ,'PGR'
                ,cast('{taskData["TaskDeadLine"]}' as datetime)
                ,'{taskData["TaskRemarks"]}'
                ,{taskData["TaskRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)

            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Applied for progress report for task named: {taskData["TaskName"]}""",taskData["UserID"],taskData["RecordID"])
            
            return 1
        except Exception:
            raise

    @staticmethod
    def GetLatestTasksForLeads(goalId,userId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.TaskChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Task changes
                SELECT 
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST( TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,CAST(FORMAT(TCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]                    
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,GM.[Name] as [GoalName]
                    ,TCT.[ParentID]
                    ,TCT.[AssignedTo]
                FROM 
                    {Tables.TaskChanges} TCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = TCT.RecordID AND 
                    LT.LatestTime = TCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = TCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = TCT.[AssignedTo] 

                INNER JOIN {Tables.Goal} GM
                    ON GM.ID = TCT.[ParentID] 

                WHERE 
                    TCT.[IsDeleted] = 0 AND
                    TCT.[CreatedBy] = '{userId}' AND
                    TCT.[ParentID] = '{goalId}' AND
                    TCT.[RunningStatus] = -1
            """            
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestTaskForDevs(goalId,userId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.TaskChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Task changes
                SELECT 
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST( TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,CAST(FORMAT(TCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]                    
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,GM.[Name] as [GoalName]
                    ,TCT.[ParentID]
                    ,TCT.[AssignedTo]
                FROM 
                    {Tables.TaskChanges} TCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = TCT.RecordID AND 
                    LT.LatestTime = TCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = TCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = TCT.[AssignedTo] 

                INNER JOIN {Tables.Goal} GM
                    ON GM.ID = TCT.[ParentID]

                WHERE 
                    TCT.[IsDeleted] = 0 AND
                    TCT.[AssignedTo] = '{userId}' AND
                    TCT.[ParentID] = '{goalId}' AND
                    TCT.[RunningStatus] = -1
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestTaskForAdmins(goalId):
        try:
            query = f"""
                -- get CTE of goals with latest stable update goal changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.TaskChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND
                        [RunningStatus] = -1 AND
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') 
                    GROUP BY [RecordID]
                )
                
                -- join the latest update goal records with Task changes
                SELECT 
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST( TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,CAST(FORMAT(TCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]                    
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,GM.[Name] as [GoalName]
                    ,TCT.[ParentID]
                    ,TCT.[AssignedTo]
                FROM 
                    {Tables.TaskChanges} TCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = TCT.RecordID AND 
                    LT.LatestTime = TCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = TCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = TCT.[AssignedTo] 

                INNER JOIN {Tables.Goal} GM
                    ON GM.ID = TCT.[ParentID]

                WHERE                 
                    TCT.[ParentID] = '{goalId}' AND
                    TCT.[IsDeleted] = 0 AND
                    TCT.[RunningStatus] = -1
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise



    @staticmethod
    def AbandonTask(taskId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.TaskChanges}
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
                '{taskId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            
            query = f"""SELECT TOP(1) [RecordID][Name] FROM {Tables.TaskChanges} WHERE [RecordID] = '{taskId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            taskId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Abandoned a task named: {recordName}""",userId,taskId)

            return 1

        except Exception:
            raise
    
    @staticmethod
    def FinishTask(taskId,userId):
        try:
            # insert a completion record for accepting changes 
            query = f"""            
            INSERT INTO {Tables.TaskChanges}
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
                '{taskId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID][Name] FROM {Tables.TaskChanges} WHERE [RecordID] = '{taskId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            taskId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Completed a task named: {recordName}""",userId,taskId)

            return 1
        except Exception:
            raise

    @staticmethod
    def AcceptChangesTask(taskChangeId,userId):
        try:
            query = f"""
            UPDATE {Tables.TaskChanges} SET           
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn],
            [RunningStatus] = 0,
            [IsStable] = 0
            WHERE [Id] = '{taskChangeId}'
            """            
            DatabaseUtilities.ExecuteNonQuery(query)

             # insert a acceptance record for accepting changes 
            query = f"""            
            INSERT INTO {Tables.TaskChanges}
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
                '{taskChangeId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            # insert a flag record for accepting changes 
            query = f"""            
            INSERT INTO {Tables.TaskChanges}
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
                '{taskChangeId}' as [ID]
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
                ,'ACPT' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID][Name] FROM {Tables.TaskChanges} WHERE [ID] = '{taskChangeId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            taskId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Accepted changes for goal named: {recordName}""",userId,taskId)

            return 1
        except Exception:
            raise

    @staticmethod
    def RejectChangesTask(taskChangeId,userId):
        try:
            query = f"""
            UPDATE {Tables.TaskChanges} SET           
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn],
            [IsStable] = 0,
            [RunningStatus] = 0
            WHERE [Id] = '{taskId}'
            """            
            DatabaseUtilities.ExecuteNonQuery(query)

            # insert a record for rejecting changes 
            query = f"""            
            INSERT INTO {Tables.TaskChanges}
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
                '{taskChangeId}' as [ID]
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
                ,'REJ' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID][Name] FROM {Tables.TaskChanges} WHERE [ID] = '{taskChangeId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            taskId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Accepted changes for goal named: {recordName}""",userId,taskId)
            
            return 1
        except Exception:
            raise


    @staticmethod
    def GetMacroHistory(taskId):        
        try:
            query = f"""
                 SELECT 
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST( TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,CAST(FORMAT(TCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]                    
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM3.[FirstName] + '-' + UM3.[LastName]) as [ModifiedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedTo]
                    ,GM.[Name] as [GoalName]
                FROM 
                    {Tables.TaskChanges} TCT
                INNER JOIN 
                    {Tables.User} UM ON TCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON TCT.[AssignedTo] = UM2.[ID]
                INNER JOIN 
                    {Tables.User} UM3 ON TCT.[ModifiedBy] = UM3.[ID]
                INNER JOIN 
                    {Tables.Goal} GM ON TCT.[ParentID] = GM.[ID]
                WHERE 
                    TCT.[IsDeleted] = 0 AND
                    TCT.[RecordID] = '{taskId}' AND
                    TCT.[IsStable] = 1 AND
                    (TCT.[ReportingStatus] != 'REJ' OR TCT.[ReportingStatus] != 'ACPT') 
                ORDER BY
                    TCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetMicroHistory(taskId):        
        try:
            query = f"""
                 SELECT 
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST( TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,CAST(FORMAT(TCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]                    
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM3.[FirstName] + '-' + UM3.[LastName]) as [ModifiedByName]                    
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedTo]
                    ,GM.[Name] as [GoalName]
                FROM 
                    {Tables.TaskChanges} TCT
                INNER JOIN 
                    {Tables.User} UM ON TCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON TCT.[AssignedTo] = UM2.[ID]
                INNER JOIN 
                    {Tables.User} UM3 ON TCT.[ModifiedBy] = UM3.[ID]
                INNER JOIN 
                    {Tables.Goal} GM ON TCT.[ParentID] = GM.[ID]
                WHERE 
                    TCT.[IsDeleted] = 0 AND
                    TCT.[RecordID] = '{taskId}'
                ORDER BY
                    TCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestStableVersionOfTask(taskId):
        try:
            query = f"""
                 SELECT 
                    TOP (1)
                    TCT.[ID]
                    ,TCT.[RecordID]
                    ,TCT.[Name]
                    ,CAST(TCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,TCT.[CreatedBy]
                    ,TCT.[CreatedOn]
                    ,TCT.[AssignedTo]
                    ,TCT.[ParentID]
                    ,TCT.[IsStable]
                    ,TCT.[ReportingStatus]
                    ,CAST(FORMAT(TCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,TCT.[Rating]
                    ,TCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) AS [CreatedByName]
                    ,(UM1.[FirstName] + '.' + UM1.[LastName]) AS [AssignedToName]
                FROM 
                    {Tables.TaskChanges} TCT
                INNER JOIN 
                    {Tables.User} UM 
                    ON UM.[ID] = TCT.[CreatedBy]
                INNER JOIN 
                    {Tables.User} UM1 
                    ON UM1.[ID] = TCT.[AssignedTo]                
                WHERE 
                    TCT.[IsDeleted] = 0 AND
                    TCT.[RecordID] = '{taskId}' AND
                    TCT.[IsStable] = 1 AND
                    (TCT.[ReportingStatus] != 'REJ' OR TCT.[ReportingStatus] != 'ACPT') AND
                    TCT.[RunningStatus] = -1
                ORDER BY
                    TCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

        
    @staticmethod
    def GetGoalAssignedToNameAndID(goalId):
        try:
            query = f"""
                 SELECT 
                    UM.[ID] as AssignedToID,
                    (UM.[FirstName] + '.' + UM.[LastName]) as [AssignedToName]
                FROM 
                    {Tables.Goal} GMT
                INNER JOIN 
                    {Tables.User} UM ON UM.[ID] = GMT.[AssignedTo]
                WHERE 
                    GMT.[IsDeleted] = 0 AND
                    GMT.[ID] = '{goalId}' AND
                    GMT.[IsStable] = 1 AND
                    (GMT.[ReportingStatus] != 'REJ' OR GMT.[ReportingStatus] != 'ACPT') AND
                    GMT.[RunningStatus] = -1
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise


    @staticmethod
    def Reversion(taskChangeId,userId):
        try:
            # insert a reversion flag record 
            query = f"""            
           INSERT INTO {Tables.TaskChanges}
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
                '{taskChangeId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.TaskChanges}
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
                '{taskChangeId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE ID = '{taskChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID][Name] FROM {Tables.TaskChanges} WHERE [ID] = '{taskChangeId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            taskId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Reverted a goal named: {recordName}""",userId,taskId)

            return 1
        except Exception:
            raise

    @staticmethod
    def Reboot(taskId,userId):
        try:
            # insert a reboot flag record 
            query = f"""            
           INSERT INTO {Tables.TaskChanges}
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
                '{taskId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE 
                [RecordID] = '{taskId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.TaskChanges}
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
                '{taskId}' as [ID]
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
            FROM {Tables.TaskChanges}
            WHERE 
                [RecordID] = '{taskId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [Name] FROM {Tables.TaskChanges} WHERE [RecordID] = '{taskId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Rebooted a task named: {recordName}""",userId,taskId)

            return 1
        except Exception:
            raise
    