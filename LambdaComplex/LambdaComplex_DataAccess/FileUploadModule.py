import os
from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities
from LambdaComplex_Entities import Credentials
from LambdaComplex_Entities.Tables import Tables
from LambdaComplex_DataAccess.WorkTimeLineModule import WorkTimeLineModule

class FileUploadModule:
    @staticmethod
    def SaveFile(recordId,userId,fileList):
        try:
            if len(fileList) == 0:
                return 
            
            for f in fileList:
                query = f"""
                        SET NOCOUNT ON; 
                        DECLARE @InsertID varchar(36) = newid();                        
                        INSERT INTO {Tables.File}
                            (
                            [ID]
                            ,[UserID]
                            ,[RecordID]
                            ,[FileName]
                            ,[FileType]
                            ,[StoredFileName]
                            ,[CreatedBy]
                            ,[ModifiedBy])
                            VALUES
                            (@InsertID
                            ,'{userId}'
                            ,'{recordId}'
                            ,'{f["filename"]}'
                            ,'{f["ext"]}'
                            ,@InsertID+ '-{f["filename"]}'
                            ,'{userId}'
                            ,'{userId}')

                        SELECT @InsertID + '-{f["filename"]}' as [FileName]
                """
                fileName = DatabaseUtilities.ExecuteScalar(query)
                f['file'].save(Credentials.RootPath.replace('/','\\') + "\\static\\Uploads\\" + fileName)

                totalFiles = len(fileList)
                WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Uploaded {totalFiles} file(s)""",userId,recordId)
        except Exception:
            raise

    @staticmethod
    def RemoveFile(id,userId):
        try:
            # Update IsDeleted field to True for the records related to the given recordId
            update_query = f"""
                            UPDATE {Tables.File}
                            SET                             
                            [IsDeleted] = 1,
                            [ModifiedBy] = '{userId}',
                            [CreatedOn] = [CreatedOn],
                            [ModifiedOn] = getdate()
                            WHERE 
                            [ID] = '{id}' and [IsDeleted] = 0
                            """
            DatabaseUtilities.ExecuteNonQuery(update_query)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f"""Removed a file""",userId,id)
        except Exception:
            raise

    @staticmethod
    def GetFileSubmission(recordId):
        try:
            query = f"""
                        SELECT 
                            [ID]
                            ,[FileName]
                            ,[FileType]
                            ,[StoredFileName]
                            ,cast(Format([CreatedOn],'yyyy-MM-dd') as varchar(30)) as [CreatedOn]
                        FROM {Tables.File}
                        WHERE 
                        [recordID] = '{recordId}' AND 
                        [IsDeleted] = 0 
                    """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise