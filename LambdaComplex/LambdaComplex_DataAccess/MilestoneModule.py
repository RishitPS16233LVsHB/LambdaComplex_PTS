from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_DataAccess.WorkTimeLineModule import WorkTimeLineModule
from LambdaComplex_Entities.Tables import Tables

class MilestoneModule:
    @staticmethod
    def CreateMilestone(milestoneData):
        try:
            query = f"""
            SET NOCOUNT ON;
            declare @InsertID table(ID varchar(36));
            declare @cngInsertID varchar(36);
            INSERT INTO {Tables.Milestone}
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
            ('{milestoneData["MilestoneName"]}'
            ,'{milestoneData["MilestoneDescription"]}'
            ,-1
            ,'{milestoneData["AssignedTo"]}'   
            ,'{milestoneData["ParentID"]}'
            ,'{milestoneData["UserID"]}'
            ,'{milestoneData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{milestoneData["MilestoneDeadLine"]}' as datetime)
            ,'{milestoneData["MilestoneRemarks"]}'
            ,{milestoneData["MilestoneRating"]});
            
            select @cngInsertID = ID from @InsertID;
            
            INSERT INTO {Tables.MilestoneChanges}
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
            ,'{milestoneData["MilestoneName"]}'
            ,'{milestoneData["MilestoneDescription"]}'
            ,-1   
            ,'{milestoneData["AssignedTo"]}' 
            ,'{milestoneData["ParentID"]}'
            ,'{milestoneData["UserID"]}'
            ,'{milestoneData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{milestoneData["MilestoneDeadLine"]}' as datetime)
            ,'{milestoneData["MilestoneRemarks"]}'
            ,{milestoneData["MilestoneRating"]});
            
            select @cngInsertID as [ID]
            """
            insertedID = DatabaseUtilities.ExecuteScalar(query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Created a milestone named: {milestoneData["MilestoneName"]}""",milestoneData["UserID"],insertedID)

        except Exception:
            raise

    @staticmethod
    def ParentUpdateMilestone(milestoneData):       
        try:
            query = f"""
                INSERT INTO {Tables.MilestoneChanges}
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
                ('{milestoneData["RecordID"]}'
                ,'{milestoneData["MilestoneName"]}'
                ,'{milestoneData["MilestoneDescription"]}'
                ,'{milestoneData["AssignedTo"]}' 
                ,'{milestoneData["ParentID"]}'
                ,-1   
                ,'{milestoneData["UserID"]}'
                ,'{milestoneData["UserID"]}'
                ,1
                ,1
                ,'PAR'
                ,cast('{milestoneData["MilestoneDeadLine"]}' as datetime)
                ,'{milestoneData["MilestoneRemarks"]}'
                ,{milestoneData["MilestoneRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Updated a milestone named: {milestoneData["MilestoneName"]}""",milestoneData["UserID"],milestoneData["RecordID"])
            
        except Exception:
            raise

    @staticmethod
    def ChildCHRUpdateMilestone(milestoneData):       
        try:
            query = f"""
                INSERT INTO {Tables.MilestoneChanges}
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
                ('{milestoneData["RecordID"]}'
                ,'{milestoneData["MilestoneName"]}'
                ,'{milestoneData["MilestoneDescription"]}'
                ,'{milestoneData["AssignedTo"]}' 
                ,'{milestoneData["ParentID"]}'
                ,-1   
                ,'{milestoneData["CreatedBy"]}'
                ,'{milestoneData["UserID"]}'
                ,1
                ,1
                ,'CHR'
                ,cast('{milestoneData["MilestoneDeadLine"]}' as datetime)
                ,'{milestoneData["MilestoneRemarks"]}'
                ,{milestoneData["MilestoneRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Applied for change request a milestone named: {milestoneData["MilestoneName"]}""",milestoneData["UserID"],milestoneData["RecordID"])
            return 1
        except Exception:
            raise

    @staticmethod
    def ChildPGRUpdateMilestone(milestoneData):       
        try:
            query = f"""          
                INSERT INTO {Tables.MilestoneChanges}
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
                ('{milestoneData["RecordID"]}'
                ,'{milestoneData["MilestoneName"]}'
                ,'{milestoneData["MilestoneDescription"]}'
                ,'{milestoneData["AssignedTo"]}' 
                ,'{milestoneData["ParentID"]}'
                ,-1   
                ,'{milestoneData["CreatedBy"]}'
                ,'{milestoneData["UserID"]}'
                ,1
                ,1
                ,'PGR'
                ,cast('{milestoneData["MilestoneDeadLine"]}' as datetime)
                ,'{milestoneData["MilestoneRemarks"]}'
                ,{milestoneData["MilestoneRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Applied for progress report a milestone named: {milestoneData["MilestoneName"]}""",milestoneData["UserID"],milestoneData["RecordID"])
            return 1
        except Exception:
            raise



    @staticmethod
    def GetLatestMilestonesForAdmins(projectId,userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.MilestoneChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Milestone changes
                SELECT 
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST( MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,CAST(FORMAT(MCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]                    
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,PM.[Name] as [ProjectName]
                    ,MCT.[ParentID]
                    ,MCT.[AssignedTo]
                FROM 
                    {Tables.MilestoneChanges} MCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = MCT.RecordID AND 
                    LT.LatestTime = MCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = MCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = MCT.[AssignedTo] 

                INNER JOIN {Tables.Project} PM
                    ON PM.ID = MCT.[ParentID] 

                WHERE 
                    MCT.[IsDeleted] = 0 AND
                    MCT.[CreatedBy] = '{userId}' AND
                    MCT.[ParentID] = '{projectId}' AND
                    MCT.[RunningStatus] = -1
            """            
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestMilestoneForLead(projectId,userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.MilestoneChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Milestone changes
                SELECT 
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST( MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,CAST(FORMAT(MCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]                    
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,PM.[Name] as [ProjectName]
                    ,MCT.[ParentID]
                    ,MCT.[AssignedTo]
                FROM 
                    {Tables.MilestoneChanges} MCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = MCT.RecordID AND 
                    LT.LatestTime = MCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = MCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = MCT.[AssignedTo] 

                INNER JOIN {Tables.Project} PM
                    ON PM.ID = MCT.[ParentID]

                WHERE 
                    MCT.[IsDeleted] = 0 AND
                    MCT.[AssignedTo] = '{userId}' AND
                    MCT.[ParentID] = '{projectId}' AND
                    MCT.[RunningStatus] = -1
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestMilestoneForDev(projectId,userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.MilestoneChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND
                        [RunningStatus] = -1 AND
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') 
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Milestone changes
                SELECT 
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST( MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,CAST(FORMAT(MCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]                    
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '.' + UM2.[LastName]) as [AssignedToName]
                    ,PM.[Name] as [ProjectName]
                    ,MCT.[ParentID]
                    ,MCT.[AssignedTo]
                FROM 
                    {Tables.MilestoneChanges} MCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = MCT.RecordID AND 
                    LT.LatestTime = MCT.CreatedOn

                INNER JOIN {Tables.User} UM
                    ON UM.ID = MCT.[CreatedBy] 

                INNER JOIN {Tables.User} UM2
                    ON UM2.ID = MCT.[AssignedTo] 

                INNER JOIN {Tables.Project} PM
                    ON PM.ID = MCT.[ParentID]

                WHERE                 
                    MCT.[ParentID] = '{projectId}' AND
                    MCT.[IsDeleted] = 0 AND
                    MCT.[RunningStatus] = -1 AND
                    MCT.[AssignedTo] in
                    (
                        SELECT 
                            TM.[LeaderID]
                        FROM {Tables.Team} TM
                        WHERE 
                            TM.[IsDeleted] = 0 AND
                            TM.[ID] in 
                            ( 
                                SELECT 
                                    TMT.[TeamID]
                                FROM {Tables.TeamMember} TMT
                                WHERE 
                                    TMT.[IsDeleted] = 0 AND
                                    TMT.[TeamMemberID] = '{userId}'
                            )
                    )
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise


    @staticmethod
    def ReviveMilestone(milestoneChangesId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
                ,'RVE' as [ReportingStatus]
                ,[Deadline]
                ,[Remarks]
                ,[Rating]
                ,getdate() as [CreatedOn]
                ,getdate() as [ModifiedOn]
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            
            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [ID] = '{milestoneChangesId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Revived a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise

    @staticmethod
    def AbandonMilestone(milestoneChangesId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            
            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [ID] = '{milestoneChangesId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Abandoned a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise
    
    @staticmethod
    def FinishMilestone(milestoneChangesId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [ID] = '{milestoneChangesId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Completed a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise

    @staticmethod
    def AcceptChangesMilestone(milestoneChangesId,userId):
        try:
            query = f"""
            UPDATE {Tables.MilestoneChanges} SET           
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn],
            [RunningStatus] = 0,
            [IsStable] = 0
            WHERE [Id] = '{milestoneChangesId}'
            """            
            DatabaseUtilities.ExecuteNonQuery(query)

             # insert a acceptance record for accepting changes 
            query = f"""            
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            # insert a flag record for accepting changes 
            query = f"""            
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [RecordID] = '{milestoneChangesId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Accepted changes for a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise

    @staticmethod
    def RejectChangesMilestone(milestoneChangesId,userId):
        try:
            query = f"""
            UPDATE {Tables.MilestoneChanges} SET           
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn],
            [IsStable] = 0,
            [RunningStatus] = 0
            WHERE [Id] = '{milestoneChangesId}'
            """            
            DatabaseUtilities.ExecuteNonQuery(query)

            # insert a record for rejecting changes 
            query = f"""            
            INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangesId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangesId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            
            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [ID] = '{milestoneChangesId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"Rejected changes milestone named: {recordName}",userId,milestoneId)
            
            return 1
        except Exception:
            raise



    @staticmethod
    def GetMacroHistory(milestoneId):        
        try:
            query = f"""
                 SELECT 
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST( MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,CAST(FORMAT(MCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]                    
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM3.[FirstName] + '-' + UM3.[LastName]) as [ModifiedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedTo]
                    ,PM.[Name] as [ProjectName]
                FROM 
                    {Tables.MilestoneChanges} MCT
                INNER JOIN 
                    {Tables.User} UM ON MCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON MCT.[AssignedTo] = UM2.[ID]
                INNER JOIN 
                    {Tables.User} UM3 ON MCT.[ModifiedBy] = UM3.[ID]
                INNER JOIN 
                    {Tables.Project} PM ON MCT.[ParentID] = PM.[ID]
                WHERE 
                    MCT.[IsDeleted] = 0 AND
                    MCT.[RecordID] = '{milestoneId}' AND
                    MCT.[IsStable] = 1 AND
                    (MCT.[ReportingStatus] != 'REJ' OR MCT.[ReportingStatus] != 'ACPT') 
                ORDER BY
                    MCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetMicroHistory(milestoneId):        
        try:
            query = f"""
                 SELECT 
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST( MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,CAST(FORMAT(MCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]                    
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                    ,(UM3.[FirstName] + '-' + UM3.[LastName]) as [ModifiedByName]                    
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                    ,(UM2.[FirstName] + '-' + UM2.[LastName]) as [AssignedTo]
                    ,PM.[Name] as [ProjectName]
                FROM 
                    {Tables.MilestoneChanges} MCT
                INNER JOIN 
                    {Tables.User} UM ON MCT.[CreatedBy] = UM.[ID]
                INNER JOIN 
                    {Tables.User} UM2 ON MCT.[AssignedTo] = UM2.[ID]
                INNER JOIN 
                    {Tables.User} UM3 ON MCT.[ModifiedBy] = UM3.[ID]
                INNER JOIN 
                    {Tables.Project} PM ON MCT.[ParentID] = PM.[ID]
                WHERE 
                    MCT.[IsDeleted] = 0 AND
                    MCT.[RecordID] = '{milestoneId}'
                ORDER BY
                    MCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestStableVersionOfMilestone(milestoneId):
        try:
            query = f"""
                 SELECT 
                    TOP (1)
                    MCT.[ID]
                    ,MCT.[RecordID]
                    ,MCT.[Name]
                    ,CAST(MCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,MCT.[CreatedBy]
                    ,MCT.[CreatedOn]
                    ,MCT.[AssignedTo]
                    ,MCT.[ParentID]
                    ,MCT.[IsStable]
                    ,MCT.[ReportingStatus]
                    ,CAST(FORMAT(MCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,MCT.[Rating]
                    ,MCT.[Remarks]
                FROM 
                    {Tables.MilestoneChanges} MCT
                WHERE 
                    MCT.[IsDeleted] = 0 AND
                    MCT.[RecordID] = '{milestoneId}' AND
                    MCT.[IsStable] = 1 AND
                    (MCT.[ReportingStatus] != 'REJ' OR MCT.[ReportingStatus] != 'ACPT') AND
                    MCT.[RunningStatus] = -1
                ORDER BY
                    MCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise



    @staticmethod
    def Reversion(milestoneChangeId,userId):
        try:
            # insert a reversion flag record 
            query = f"""            
           INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangeId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneChangeId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE ID = '{milestoneChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [RecordID],[Name] FROM {Tables.MilestoneChanges} WHERE [ID] = '{milestoneChangeId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            milestoneId = record["RecordID"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Reverted a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise

    @staticmethod
    def Reboot(milestoneId,userId):
        try:
            # insert a reboot flag record 
            query = f"""            
           INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE 
                [RecordID] = '{milestoneId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.MilestoneChanges}
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
                '{milestoneId}' as [ID]
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
            FROM {Tables.MilestoneChanges}
            WHERE 
                [RecordID] = '{milestoneId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)

            query = f"""SELECT TOP(1) [Name] FROM {Tables.Milestone} WHERE [ID] = '{milestoneId}' AND [IsDeleted] = 0;"""
            record = DatabaseUtilities.GetListOf(query)[0]
            recordName = record["Name"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Rebooted a milestone named: {recordName}""",userId,milestoneId)

            return 1
        except Exception:
            raise
    