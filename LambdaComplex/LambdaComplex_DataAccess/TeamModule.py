from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities  
from LambdaComplex_Entities.Tables import Tables

class TeamModule:
    @staticmethod
    def GetTeamsForAdmin(userId):
        try:
            query = f"""
            SELECT 
            TM.[ID],
            TM.[TeamName],
            cast(TM.[TeamDescription] as xml).value('.[1]','nvarchar(max)') as [TeamDescription],
            UM.[FirstName] as LeaderFirstName,
            UM.[LastName] as LeaderLastName,
            UM1.[FirstName] as AdminFirstName,
            UM1.[LastName] as AdminLastName,
            cast(Format(TM.[CreatedOn],'dd-MM-yyyy') as varchar(30)) as CreatedOn

            FROM {Tables.Team} TM
            INNER JOIN {Tables.User} UM ON TM.[LeaderId] = UM.[ID]
            INNER JOIN {Tables.User} UM1 ON TM.[CreatedBy] = UM1.[ID]
            WHERE [CreatedBy] = '{userId}' 
            AND 
            UM.[IsDeleted] = 0 AND 
            TM.[IsDeleted] = 0 AND
            UM1.[IsDeleted] = 0"""
            result = DatabaseUtilities.GetListOf(query)
            return result
        except Exception:
            raise

    @staticmethod
    def GetTeamsForLead(userId):
        try:
            query = f"""
            SELECT 
            TM.[ID] as TeamId,
            TM.[TeamName],
            cast(TM.[TeamDescription] as xml).value('.[1]','nvarchar(max)') as [TeamDescription],
            UM.[FirstName] as LeaderFirstName,
            UM.[LastName] as LeaderLastName,
            UM1.[FirstName] as AdminFirstName,
            UM1.[LastName] as AdminLastName,   
            TM.[CreatedBy],         
            cast(Format(TM.[CreatedOn],'dd-MM-yyyy') as varchar(30)) as CreatedOn

            FROM {Tables.Team} TM
            INNER JOIN {Tables.User} UM ON TM.[LeaderId] = UM.[ID]
            INNER JOIN {Tables.User} UM1 ON TM.[CreatedBy] = UM1.[ID]
            WHERE [LeaderId] = '{userId}' 
            AND 
            UM.[IsDeleted] = 0 AND 
            TM.[IsDeleted] = 0 AND
            UM1.[IsDeleted] = 0"""
            result = DatabaseUtilities.GetListOf(query)
            return result
        except Exception:
            raise

    @staticmethod
    def GetTeamsForDev(userId):
        try:
            query = f"""
            SELECT 
            TM.[ID] as TeamId,
            TM.[TeamName],
            cast(TM.[TeamDescription] as xml).value('.[1]','nvarchar(max)') as [TeamDescription],
            UM.[FirstName] as LeaderFirstName,
            UM.[LastName] as LeaderLastName,
            UM1.[FirstName] as AdminFirstName,
            UM1.[LastName] as AdminLastName,
            cast(Format(TM.[CreatedOn],'dd-MM-yyyy') as varchar(30)) as CreatedOn

            FROM {Tables.Team} TM
            INNER JOIN {Tables.User} UM ON TM.[LeaderId] = UM.[ID]
            INNER JOIN {Tables.User} UM1 ON TM.[CreatedBy] = UM1.[ID]            
            WHERE [LeaderId] in (SELECT TeamID from {Tables.TeamMember} WHERE TeamMemberID = '{userId}') 
            AND 
            UM.[IsDeleted] = 0 AND 
            TM.[IsDeleted] = 0 AND
            UM1.[IsDeleted] = 0"""
            result = DatabaseUtilities.GetListOf(query)
            return result
        except Exception:
            raise

    @staticmethod
    def GetTeamMemberList(teamId):
        try:
            query = f"""
            SELECT 
            TM.[ID], 
            UM.[FirstName],
            UM.[LastName],
            UM.[EmailID]
            FROM {Tables.TeamMember} TM 
            INNER JOIN {Tables.User} UM ON UM.[ID] = TM.[TeamMemberID] 
            WHERE [TeamID] = '{teamId}' AND 
            UM.[IsDeleted] = 0 AND
            TM.[IsDeleted] = 0
            """
            result = DatabaseUtilities.GetListOf(query)
            return result
        except Exception:
            raise

    @staticmethod
    def GetTeamData(teamId):
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
            WHERE [ID] = '{teamId}' AND [IsDeleted] = 0
            """
            result = DatabaseUtilities.GetListOf(query)
            return result
        except Exception:
            raise
            
    @staticmethod
    def CreateTeam(teamData):
        try:
            query = f"""
            INSERT INTO {Tables.Team}
            ([TeamName]
            ,[TeamDescription]
            ,[LeaderID]
            ,[ProjectID]
            ,[CreatedBy]
            ,[ModifiedBy])
                VALUES
            (
            '{teamData["TeamName"]}'
            ,'{teamData["TeamDescription"]}'
            ,'{teamData["LeadId"]}'
            ,'{teamData["ProjectId"]}'
            ,'{teamData["UserId"]}'
            ,'{teamData["UserId"]}'
                )
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def UpdateTeam(teamData):
        try:
            query = f"""
            UPDATE {Tables.Team}
            SET [TeamName] = '{teamData["TeamName"]}'
                ,[TeamDescription] = '{teamData["TeamDescription"]}'
                ,[LeaderID] = '{teamData["LeadId"]}'
                ,[ProjectID] = '{teamData["ProjectId"]}'
                ,[ModifiedBy] = '{teamData["UserId"]}'
                ,[CreatedOn] = [CreatedOn]
            WHERE ID = '{teamData["Id"]}' AND IsDeleted = 0
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def RemoveTeam(teamId):
        try:
            query = f"""            
            UPDATE {Tables.Team}
            SET [IsDeleted] = 1
            WHERE ID = '{teamId}' AND IsDeleted = 0;

            -- to remove team members too 

            UPDATE {Tables.TeamMember}
            SET [IsDeleted] = 1
            WHERE TeamID = '{teamId}' AND IsDeleted = 0;
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
    

    @staticmethod
    def AddTeamMember(teamId, teamMemberId, userId):
        try:
            query = f"""            
            INSERT INTO {Tables.TeamMember}
                    ([TeamID]
                    ,[TeamMemberID]
                    ,[CreatedBy]
                    ,[ModifiedBy])
                VALUES
                    ('{teamId}'
                    ,'{teamMemberId}'
                    ,'{userId}'
                    ,'{userId}')
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def RemoveTeamMember(recordId):
        try:
            query = f"""            
            UPDATE {Tables.TeamMember}
            SET [IsDeleted] = 1
            WHERE ID = '{recordId}' AND IsDeleted = 0;
            """
            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise
