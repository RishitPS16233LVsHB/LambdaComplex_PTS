from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities.Tables import Tables

class ProjectModule:
    @staticmethod
    def CreateProject(projectData):
        try:
            query = f"""
            declare @InsertID table(ID varchar(36));
            declare @cngInsertID varchar(36);
            INSERT INTO {Tables.Project}
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
            ,[Rating])
        OUTPUT Inserted.ID into @InsertID
        VALUES
            ('{projectData["ProjectName"]}'
            ,'{projectData["ProjectDescription"]}'
            ,-1   
            ,'{projectData["UserID"]}'
            ,'{projectData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{projectData["ProjectDeadLine"]}' as datetime)
            ,'{projectData["ProjectRemarks"]}'
            ,{projectData["ProjectRating"]});
            
            select @cngInsertID = ID from @InsertID;
            
            INSERT INTO {Tables.ProjectChanges}
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
            ,[Rating])
        VALUES
            (@cngInsertID
            ,'{projectData["ProjectName"]}'
            ,'{projectData["ProjectDescription"]}'
            ,-1   
            ,'{projectData["UserID"]}'
            ,'{projectData["UserID"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{projectData["ProjectDeadLine"]}' as datetime)
            ,'{projectData["ProjectRemarks"]}'
            ,{projectData["ProjectRating"]});
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def ParentUpdateProject(projectData):       
        try:
            query = f"""
                INSERT INTO {Tables.ProjectChanges}
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
                ,[Rating])
                 VALUES
                ('{projectData["RecordID"]}'
                ,'{projectData["ProjectName"]}'
                ,'{projectData["ProjectDescription"]}'
                ,-1   
                ,'{projectData["UserID"]}'
                ,'{projectData["UserID"]}'
                ,1
                ,1
                ,'PAR'
                ,cast('{projectData["ProjectDeadLine"]}' as datetime)
                ,'{projectData["ProjectRemarks"]}'
                ,{projectData["ProjectRating"]});
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def GetProjectNameID(userId):        
        try:
            query = f"""
                SELECT 
                [ID],
                [Name]
                FROM {Tables.Project}
                WHERE [IsDeleted] = 0 AND
                [CreatedBy] = '{userId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
    
    @staticmethod
    def GetLatestProjectsForAdmins(userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.ProjectChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Project changes
                SELECT 
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST( PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,CAST(FORMAT(PCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]                    
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                FROM 
                    {Tables.ProjectChanges} PCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = PCT.RecordID AND 
                    LT.LatestTime = PCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = PCT.[CreatedBy] 
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[CreatedBy] = '{userId}' AND 
                    PCT.[RunningStatus] = -1
            """            
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestProjectForLead(userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.ProjectChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND
                        [IsStable] = 1 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Project changes
                SELECT 
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST( PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,CAST(FORMAT(PCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                FROM 
                    {Tables.ProjectChanges} PCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = PCT.RecordID AND 
                    LT.LatestTime = PCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = PCT.[CreatedBy] 
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[RunningStatus] = -1 AND
                    PCT.[RecordID] in (
                        SELECT 
                            TM.[ProjectID]
                        FROM {Tables.Team} TM
                        WHERE 
                            [IsDeleted] = 0 AND
                            [LeaderID] = '{userId}'
                    )
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestProjectForDev(userId):
        try:
            query = f"""
                -- get CTE of projects with latest stable update project changes 
                WITH
                LatestTime AS(
                    SELECT 
                        [RecordID],
                        MAX([CreatedOn]) AS [LatestTime] 
                    FROM {Tables.ProjectChanges} 
                    WHERE 
                        [IsDeleted] = 0 AND                        
                        ([ReportingStatus] != 'REJ' AND [ReportingStatus] != 'ACPT') AND
                        [RunningStatus] = -1 AND
                        [IsStable] = 1
                    GROUP BY [RecordID]
                )
                
                -- join the latest update project records with Project changes
                SELECT 
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST( PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,CAST(FORMAT(PCT.[CreatedOn],'yyyy-MM-dd') as varchar(30)) AS [CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                    ,(UM.[FirstName] + '.' + UM.[LastName]) as [CreatedByName]
                FROM 
                    {Tables.ProjectChanges} PCT 
                INNER JOIN LatestTime LT 
                    ON LT.RecordID = PCT.RecordID AND 
                    LT.LatestTime = PCT.CreatedOn
                INNER JOIN {Tables.User} UM
                    ON UM.ID = PCT.[CreatedBy] 
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[RunningStatus] = -1 AND
                    PCT.[RecordID] in 
                    (
                        SELECT 
                            TM.[ProjectID]
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
    def AbandonProject(projectChangeId,userId):
        try:
            query = f"""
            INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE ID = '{projectChangeId}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    
    @staticmethod
    def FinishProject(projectChangeId,userId):
        try:
            query = f"""
                INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE ID = '{projectChangeId}' AND [IsDeleted] = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def GetMacroHistory(projectId):        
        try:
            query = f"""
                 SELECT 
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST( PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,CAST(FORMAT(PCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]                    
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                FROM 
                    {Tables.ProjectChanges} PCT
                INNER JOIN 
                    {Tables.User} UM ON PCT.[CreatedBy] = UM.[ID]
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[RecordID] = '{projectId}' AND
                    PCT.[IsStable] = 1
                ORDER BY
                    PCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetMicroHistory(projectId):        
        try:
            query = f"""
                 SELECT 
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST( PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,CAST(FORMAT(PCT.[CreatedOn],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]                    
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd hh:mm:ss') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                    ,(UM.[FirstName] + '-' + UM.[LastName]) as [CreatedByName]
                FROM 
                    {Tables.ProjectChanges} PCT
                INNER JOIN 
                    {Tables.User} UM ON PCT.[CreatedBy] = UM.[ID]
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[RecordID] = '{projectId}'
                ORDER BY
                    PCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetLatestStableVersionOfProject(projectId):
        try:
            query = f"""
                 SELECT 
                    TOP (1)
                    PCT.[ID]
                    ,PCT.[RecordID]
                    ,PCT.[Name]
                    ,CAST(PCT.[Description] as XML).value('.[1]','nvarchar(MAX)') as [Description]
                    ,PCT.[CreatedBy]
                    ,PCT.[CreatedOn]
                    ,PCT.[IsStable]
                    ,PCT.[ReportingStatus]
                    ,CAST(FORMAT(PCT.[Deadline],'yyyy-MM-dd') as varchar(30)) AS [Deadline]
                    ,PCT.[Rating]
                    ,PCT.[Remarks]
                FROM 
                    {Tables.ProjectChanges} PCT
                WHERE 
                    PCT.[IsDeleted] = 0 AND
                    PCT.[RecordID] = '{projectId}' AND
                    PCT.[IsStable] = 1 AND
                    PCT.[RunningStatus] = -1
                ORDER BY
                    PCT.[CreatedOn] DESC
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def GetTeamList(projectId):        
        try:
            query = f"""
                SELECT [ID]
            ,[TeamName]
            ,[TeamDescription]
            ,[LeaderID]
            ,[ProjectID]
            ,[IsDeleted]
            ,[CreatedBy]
            ,[ModifiedBy]
            ,[CreatedOn]
            ,[ModifiedOn]
            FROM {Tables.Team}
            WHERE [IsDeleted] = 0 AND [ProjectID] = '{projectId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise
        
    @staticmethod
    def Reversion(projectChangeId,userId):
        try:
            # insert a reversion flag record 
            query = f"""            
           INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,0 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE ID = '{projectChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectChangeId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE ID = '{projectChangeId}' AND [IsDeleted] = 0
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def Reboot(projectId,userId):
        try:
            # insert a reboot flag record 
            query = f"""            
           INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,0 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE 
                [RecordID] = '{projectId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
            # insert a actual par  record 
            query = f"""            
           INSERT INTO {Tables.ProjectChanges}
                (
                [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,[RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
                '{projectId}' as [ID]
                ,[RecordID]
                ,[Name]
                ,[Description]
                ,-1 as [RunningStatus]
                -- ,[AssignedTo]
                -- ,[ParentID]
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
            FROM {Tables.ProjectChanges}
            WHERE 
                [RecordID] = '{projectId}' AND 
                [IsDeleted] = 0 AND
                [ReportingStatus] = 'INITIAL'
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    