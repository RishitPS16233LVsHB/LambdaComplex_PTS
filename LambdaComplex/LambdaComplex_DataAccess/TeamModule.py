from LambdaComplex_DataAccess import UserModule
from LambdaComplex_DataAccess.DatabaseUtilities import DatabaseUtilities  
from LambdaComplex_Entities.Tables import Tables
from LambdaComplex_DataAccess.WorkTimeLineModule import WorkTimeLineModule

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
            SET NOCOUNT ON;
            DECLARE @InsertedID table(ID varchar(36));
            INSERT INTO {Tables.Team}
            ([TeamName]
            ,[TeamDescription]
            ,[LeaderID]
            ,[ProjectID]
            ,[CreatedBy]
            ,[ModifiedBy])
                OUTPUT inserted.ID into @InsertedID
                VALUES
            (
            '{teamData["TeamName"]}'
            ,'{teamData["TeamDescription"]}'
            ,'{teamData["LeadId"]}'
            ,'{teamData["ProjectId"]}'
            ,'{teamData["UserId"]}'
            ,'{teamData["UserId"]}'
                )
            SELECT ID FROM @InsertedID;
            """
            InsertedID = DatabaseUtilities.ExecuteScalar(query)
            message = f'Created a new Team named {teamData["TeamName"]}' 
            UserID = teamData["UserId"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(message,UserID,InsertedID)

            return 1 
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

            UpdateID = teamData["Id"]
            message = f'Updated Team named {teamData["TeamName"]}' 
            UserID = teamData["UserId"]
            WorkTimeLineModule.CreateWorkTimeLineEntry(message,UserID,UpdateID)

            return DatabaseUtilities.ExecuteNonQuery(query)
        except Exception:
            raise

    @staticmethod
    def RemoveTeam(userId,teamId):
        try:
            query = f"""            
            UPDATE {Tables.Team}
            SET [IsDeleted] = 1,
            [ModifiedBy] = '{userId}',
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn]
            WHERE ID = '{teamId}' AND IsDeleted = 0;

            -- to remove team members too 

            UPDATE {Tables.TeamMember}
            SET [IsDeleted] = 1,
            [ModifiedBy] = '{userId}',
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn]
            WHERE TeamID = '{teamId}' AND IsDeleted = 0;            
            """
            if DatabaseUtilities.ExecuteNonQuery(query) == 0:
                return
            
            team = TeamModule.GetTeamData(teamId)[0]
            teamMembers = TeamModule.GetTeamMemberList(teamId)
            teamName = team["TeamName"]

            # create Work time line event for main user
            message = 'Disbanded a team: ' + teamName
            WorkTimeLineModule.CreateWorkTimeLineEntry(message,userId,teamId)
            userDetails = UserModule.GetUserDetails(userId)
            firstName = userDetails["FirstName"]
            lastName = userDetails["LastName"]
            fullName = (firstName + "." + lastName)

            # then add to team members timeline
            for tm in teamMembers:
                message = f"You were forcefully exited from team {teamName} by Admin {fullName}"
                teamMemberID = tm["ID"]
                WorkTimeLineModule.CreateWorkTimeLineEntry(message,teamMemberID,teamId)

            return 1
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
            DatabaseUtilities.ExecuteNonQuery(query)

            # from Main user perspective                       
            teamName = TeamModule.GetTeamData(teamId)["TeamName"]

            userDetails = UserModule.GetUserDetails(teamMemberId);
            firstName = userDetails["FirstName"]
            lastName = userDetails["LastName"]
            fullName = (firstName + "." + lastName)            

            WorkTimeLineModule.CreateWorkTimeLineEntry(f'You made changes to team: "{teamName}" by adding a member',userId,teamId)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f'{fullName} was added as Team member into {teamName}',userId,teamMemberId)

            userDetails = UserModule.GetUserDetails(userId);
            firstName = userDetails["FirstName"]
            lastName = userDetails["LastName"]
            fullName = (firstName + "." + lastName)

            # from team member's perspective
            WorkTimeLineModule.CreateWorkTimeLineEntry(f'You were added to team {teamName} By Admin: {fullName}',teamMemberId,teamId)

            return 1
        except Exception:
            raise
    
    @staticmethod
    def GetTeamMemberRecord(recordId):
        try:
            query = f"""            
            SELECT 
                [TeamID]
                ,[TeamMemberID]
                ,[CreatedBy]
            FROM {Tables.TeamMember} 
            WHERE ID = '{recordId}'
            """
            return DatabaseUtilities.GetListOf(query)
        except Exception:
            raise

    @staticmethod
    def RemoveTeamMember(userId,recordId):
        try:
            query = f"""            
            UPDATE {Tables.TeamMember}
            SET [IsDeleted] = 1,
            [ModifiedBy] = '{userId}',
            [ModifiedOn] = getdate(),
            [CreatedOn] = [CreatedOn]
            WHERE ID = '{recordId}' AND IsDeleted = 0;
            """
            if DatabaseUtilities.ExecuteNonQuery(query) == 0:
                return


            teamMemberRecord = TeamModule.GetTeamMemberRecord(recordId)
            teamId = teamMemberRecord["TeamID"]
            teamMemberId = teamMemberRecord["TeamMemberID"]
            
            userDetails = UserModule.GetUserDetails(teamMemberId);
            firstName = userDetails["FirstName"]
            lastName = userDetails["LastName"]
            fullName = (firstName + "." + lastName)
            teamName = TeamModule.GetTeamData(teamId)["TeamName"]

            # from Main user perspective            
            WorkTimeLineModule.CreateWorkTimeLineEntry(f'You made changes to team {teamName} by removing a member {fullName}',userId,teamId)
            WorkTimeLineModule.CreateWorkTimeLineEntry(f'{fullName} was removed from the team {teamName}',userId,teamMemberId)

            userDetails = UserModule.GetUserDetails(userId)
            firstName = userDetails["FirstName"]
            lastName = userDetails["LastName"]
            fullName = (firstName + "." + lastName)

            # from team member's perspective
            WorkTimeLineModule.CreateWorkTimeLineEntry(f'You were removed from a team {teamName} By Admin {fullName}',teamMemberId,teamId)

            return 1
        except Exception:
            raise
