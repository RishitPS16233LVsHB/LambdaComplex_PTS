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
            ,[Deadline])
        OUTPUT Inserted.ID into @InsertID
        VALUES
            ('{projectData["ProjectName"]}'
            ,'{projectData["ProjectDescription"]}'
            ,-1   
            ,'{projectData["UserId"]}'
            ,'{projectData["UserId"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{projectData["Deadline"]}' as datetime));
            
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
            ,[Deadline])
        VALUES
            (@cngInsertID
            ,'{projectData["ProjectName"]}'
            ,'{projectData["ProjectDescription"]}'
            ,-1   
            ,'{projectData["UserId"]}'
            ,'{projectData["UserId"]}'
            ,1
            ,1
            ,'INITIAL'
            ,cast('{projectData["Deadline"]}' as datetime));
            """
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    
    @staticmethod
    def UpdateProject(projectData):    
        try:
            query = f"""
            UPDATE {Tables.Project} SET
            [Name] = '{projectData["ProjectName"]}'
            ,[Description] = '{projectData["ProjectDescription"]}'
            ,[RunningStatus] = -1
            ,[ModifiedBy] = '{projectData["UserId"]}'
            ,[IsStable] = 0
            ,[Version] = [Version]
            ,[ReportingStatus] = '{projectData["ReportingStatus"]}'
            ,[Deadline] = cast('{projectData["Deadline"]}' as datetime)
            WHERE [ID] = '{projectData["ID"]}' AND [IsDeleted] = 0;
             
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
            ,[Deadline])
        VALUES
            ('{projectData["ID"]}'
            ,'{projectData["ProjectName"]}'
            ,'{projectData["ProjectDescription"]}'
            ,-1   
            ,'{projectData["UserId"]}'
            ,'{projectData["UserId"]}'
            ,0
            ,1
            ,'{projectData["ReportingStatus"]}'
            ,cast('{projectData["Deadline"]}' as datetime));
            """
            
            DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise