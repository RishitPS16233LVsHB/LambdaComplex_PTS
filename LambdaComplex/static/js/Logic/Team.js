var teamIds = {
    // edit and create pages
    teamName: "#txtTeamName",
    teamDescription: "#txtTeamDescription",
    leader: "#cmbLeader",
    project: "#cmbProject",
    ID: "#hdnID",

    // team management page
    developer: "#cmbDeveloper",
    memberList: "#grdTeamMembers",
    teamId: "#hdnTeamId",
};

function LoadTeamInformaticsView(teamId) {
    try {
        ShowLoadingScreen();

        SetViewInMainPageUsingGet("Team/InformaticView/" + teamId, false, false, "#divMainPage");

        // init editor for team description
        var editor = $(teamIds.teamDescription).kendoEditor({
            encoded: true,
            readonly: true,
            value: $(teamIds.teamDescription).val(),
            tools: [
                "bold", "italic", "underline", "undo", "redo", "justifyLeft", "justifyCenter", "justifyRight", "insertUnorderedList",
                "createLink", "unlink", "insertImage", "tableWizard", "tableProperties", "tableCellProperties", "createTable",
                "addRowAbove", "addRowBelow", "addColumnLeft", "addColumnRight", "deleteRow", "deleteColumn", "mergeCellsHorizontally",
                "mergeCellsVertically", "splitCellHorizontally", "splitCellVertically", "tableAlignLeft", "tableAlignCenter",
                "tableAlignRight", "formatting",
                {
                    name: "fontName",
                    items: [
                        { text: "Andale Mono", value: "\"Andale Mono\"" }, // Font-family names composed of several words should be wrapped in \" \"
                        { text: "Arial", value: "Arial" },
                        { text: "Arial Black", value: "\"Arial Black\"" },
                        { text: "Book Antiqua", value: "\"Book Antiqua\"" },
                        { text: "Comic Sans MS", value: "\"Comic Sans MS\"" },
                        { text: "Courier New", value: "\"Courier New\"" },
                        { text: "Georgia", value: "Georgia" },
                        { text: "Helvetica", value: "Helvetica" },
                        { text: "Impact", value: "Impact" },
                        { text: "Symbol", value: "Symbol" },
                        { text: "Tahoma", value: "Tahoma" },
                        { text: "Terminal", value: "Terminal" },
                        { text: "Times New Roman", value: "\"Times New Roman\"" },
                        { text: "Trebuchet MS", value: "\"Trebuchet MS\"" },
                        { text: "Verdana", value: "Verdana" },
                    ]
                },
                "fontSize",
                "foreColor",
                "backColor",
            ],
        });
        // load leader in kendo box
        $(teamIds.leader).kendoComboBox({
            placeholder: "Select Leader...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetLeads');
                        if (result)
                            options.success(result);
                    }
                }
            },
            readonly: true,
            filter: "contains",
            suggest: true,
            separator: ", ",
            change: function (e) {

            }
        });

        // Load Team member list
        LoadGridView('TeamAPI/InformaticsMemberManagementResource/' + teamId, false, true, teamIds.memberList);
        // remove the grid record creation button
        $("#btnCreate").remove();

        HideLoadingScreen();
    }
    catch (ex) {
        toastr.error("Error while initing team create form: " + ex.message);
    }
}

function LoadTeamManagementView(teamId) {
    try {
        SetViewInMainPageUsingGet('Team/TeamMemberManagement/' + teamId, true, true, "#divMainPage");
    }
    catch (ex) {
        toastr.error("error while loading team management view: " + ex.message);
    }
}

function InitTeamCreate() {
    try {

        var editor = $(teamIds.teamDescription).kendoEditor({
            encoded: true,
            value: $(teamIds.teamDescription).val(),
            tools: [
                "bold", "italic", "underline", "undo", "redo", "justifyLeft", "justifyCenter", "justifyRight", "insertUnorderedList",
                "createLink", "unlink", "tableWizard", "tableProperties", "tableCellProperties", "createTable",
                "addRowAbove", "addRowBelow", "addColumnLeft", "addColumnRight", "deleteRow", "deleteColumn", "mergeCellsHorizontally",
                "mergeCellsVertically", "splitCellHorizontally", "splitCellVertically", "tableAlignLeft", "tableAlignCenter",
                "tableAlignRight", "formatting",
                {
                    name: "fontName",
                    items: [
                        { text: "Andale Mono", value: "\"Andale Mono\"" }, // Font-family names composed of several words should be wrapped in \" \"
                        { text: "Arial", value: "Arial" },
                        { text: "Arial Black", value: "\"Arial Black\"" },
                        { text: "Book Antiqua", value: "\"Book Antiqua\"" },
                        { text: "Comic Sans MS", value: "\"Comic Sans MS\"" },
                        { text: "Courier New", value: "\"Courier New\"" },
                        { text: "Georgia", value: "Georgia" },
                        { text: "Helvetica", value: "Helvetica" },
                        { text: "Impact", value: "Impact" },
                        { text: "Symbol", value: "Symbol" },
                        { text: "Tahoma", value: "Tahoma" },
                        { text: "Terminal", value: "Terminal" },
                        { text: "Times New Roman", value: "\"Times New Roman\"" },
                        { text: "Trebuchet MS", value: "\"Trebuchet MS\"" },
                        { text: "Verdana", value: "Verdana" },
                    ]
                },
                "fontSize",
                "foreColor",
                "backColor",
            ]
        });

        $(teamIds.leader).kendoComboBox({
            placeholder: "Select Leader...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        var result = QuickAPIRead('UserAPI/GetLeads');
                        if (result)
                            options.success(result);
                    }
                }
            },
            filter: "contains",
            suggest: true,
            separator: ", ",
            change: function (e) {

            }
        });


    }
    catch (ex) {
        toastr.error("Error while initing team create form: " + ex.message);
    }
}

function InitMemberManagement() {
    try {

        $(teamIds.developer).kendoComboBox({
            placeholder: "Select developer...",
            dataTextField: "UserName",
            dataValueField: "ID",
            dataSource: {
                transport: {
                    read: function (options) {
                        debugger;
                        var result = QuickAPIRead('UserAPI/GetDevs');
                        if (result)
                            options.success(result);
                    }
                }
            },
            filter: "contains",
            suggest: true,
            separator: ", ",
            change: function (e) {

            }
        });

        LoadGridView('TeamAPI/MemberManagementResource/' + $(teamIds.teamId).val(), false, true, teamIds.memberList);

        // remove the grid record creation button
        $("#btnCreate").remove();
    }
    catch (ex) {
        toastr.error("Error while initing team management form: " + ex.message);
    }
}

function CreateTeam() {
    try {
        ConfirmationAlert("Creat team...", "Are you sure you want to create new team?", function (value) {

            var dataToSend = {
                TeamName: $(teamIds.teamName).val(),
                TeamDescription: $(teamIds.teamDescription).val(),
                LeadId: $(teamIds.leader).val(),
                ProjectId: $(teamIds.project).val(),
                UserId: $(sessionIds.userId).val(),
            }

            var url = "TeamAPI/CreateTeam/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Team created successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Team creation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });


    }
    catch (ex) {
        toastr.error("Error while creating the team " + ex.message);
    }
}

function UpdateTeam() {
    try {
        ConfirmationAlert("Update team...", "Are you sure you want to update this team?", function (value) {

            var dataToSend = {
                Id: $(teamIds.ID).val(),
                TeamName: $(teamIds.teamName).val(),
                TeamDescription: $(teamIds.teamDescription).val(),
                LeadId: $(teamIds.leader).val(),
                ProjectId: $(teamIds.project).val(),
                UserId: $(sessionIds.userId).val(),
            }

            var url = "TeamAPI/UpdateTeam/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Team updated successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Team updation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });


    }
    catch (ex) {
        toastr.error("Error while creating the team " + ex.message);
    }
}

function AddMember() {
    try {
        if (IsNullOrEmpty($(teamIds.developer).val())) return;

        ConfirmationAlert('Team management', 'Are you sure you want to add this user to team?',
            function (result) {
                var url = "TeamAPI/AddTeamMember/";
                var dataToSend = {
                    teamId: $(teamIds.teamId).val(),
                    teamMemberId: $(teamIds.developer).val(),
                    userId: $(sessionIds.userId).val(),
                }

                AjaxPOSTRequest(url, dataToSend, function (response) {
                    if (response.WasSuccessful) {
                        AlertSuccess("Added user to the team!");
                        InitMemberManagement();
                    }
                    else {
                        AlertError("Error adding user to team! " + response.Message);
                    }
                }, function (error) {

                }, true, true, true);
            });
    }
    catch (ex) {
        toast.error("Error while adding member to team...");
    }
}

function RemoveMember(recordId) {
    try {
        ConfirmationAlert('Team management', 'Are you sure you want to remove this team member?', function (result) {
            let deleteUrl = "TeamAPI/RemoveTeamMember/" + recordId;
            AjaxGETRequest(deleteUrl, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess('Removed successfully!');
                    InitMemberManagement();
                }
                else {
                    toastr.error("error occurred while deleting: " + response.Message);
                }
            }, function (err) {

            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}