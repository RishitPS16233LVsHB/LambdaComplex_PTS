var projectIds = {
    projectName: "#txtProjectName",
    projectDeadLine: "#dtExpectedDeadLine",
    projectDescription: "#txtProjectDescription",
    projectRemarks: "#txtProjectRemarks",
    projectRating: "#rtProjectRating",

    projectId: "#hdnProjectId",
}

function InitProjectCreate() {
    try {
        $(projectIds.projectDescription).kendoEditor(kendoEditorConfig($(projectIds.projectDescription).val()));
        $(projectIds.projectRating).kendoRating();
    }
    catch (ex) {
        toastr.error("Error while initing project create: " + ex.message);
    }
}
function InitProjectUpdate() {
    try {
        $(projectIds.projectDescription).kendoEditor(kendoEditorConfig($(projectIds.projectDescription).val()));
        var deadLine = new Date($(projectIds.projectDeadLine).attr('valueAttr')).toISOString().slice(0, 10);
        $(projectIds.projectDeadLine).val(deadLine);
        $(projectIds.projectRating).kendoRating();
    }
    catch (ex) {
        toastr.error("Error while initing project create: " + ex.message);
    }
}

function CreateProject() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Create Project...", "Are you sure you want to create new project?", function (value) {

            var dataToSend = {
                ProjectName: $(projectIds.projectName).val(),
                ProjectDescription: $(projectIds.projectDescription).val(),
                ProjectDeadLine: $(projectIds.projectDeadLine).val(),
                ProjectRemarks: $(projectIds.projectRemarks).val(),
                ProjectRating: $(projectIds.projectRating).val(),
                UserID: $(sessionIds.userId).val(),
            }

            var url = "ProjectAPI/CreateProject/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Project created successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Project creation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while creating project " + ex.message);
    }
}
function UpdateProject() {
    try {
        if (!ValidateForm()) return;

        ConfirmationAlert("Update Project...", "Are you sure you want to update this project?", function (value) {

            var dataToSend = {
                ProjectName: $(projectIds.projectName).val(),
                ProjectDescription: $(projectIds.projectDescription).val(),
                ProjectDeadLine: $(projectIds.projectDeadLine).val(),
                ProjectRemarks: $(projectIds.projectRemarks).val(),
                ProjectRating: $(projectIds.projectRating).val(),
                RecordID: $(projectIds.projectId).val(),
                UserID: $(sessionIds.userId).val(),
            }

            var url = "ProjectAPI/UpdateProject/";
            AjaxPOSTRequest(url, dataToSend, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    AlertSuccess("Project updated successfully");
                    RefreshDataView();
                }
                else {
                    AlertError("Project updation error: " + response.Message);
                }
            }, function (error) {
                Toastr.error(str(error));
            }, true, true, true);
        });
    }
    catch (ex) {
        toastr.error("Error while updating project " + ex.message);
    }
}

function FinishProject(projectChangeID = null) {
    try {
        if (IsNullOrEmpty(projectChangeID)) return;
        ConfirmationAlert('Project', 'Do you really want to finsh this project?', function (value) {
            var url = 'ProjectAPI/FinishProject/' + projectChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertSuccess("Yay! Finished project....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error finishing project: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing project: " + ex.message);
    }
}
function AbandonProject(projectChangeID = null) {
    try {
        if (IsNullOrEmpty(projectChangeID)) return;
        ConfirmationAlert('Project', 'Do you really want to abandon this project?', function (value) {
            var url = 'ProjectAPI/AbandonProject/' + projectChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Abandoned project....");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error abandoning project: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while finishing project: " + ex.message);
    }
}

function RebootProject(projectID = null) {
    try {
        if (IsNullOrEmpty(projectID)) return;
        ConfirmationAlert('Project', 'Do you really want to reboot this project?', function (value) {
            var url = 'ProjectAPI/RebootProject/' + projectID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Rebooted project!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error rebooting project: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while rebooting project: " + ex.message);
    }
}
function ReversionProject(projectChangeID = null) {
    try {
        if (IsNullOrEmpty(projectChangeID)) return;
        ConfirmationAlert('Project', 'Do you really want to reversion this project to an older version?', function (value) {
            var url = 'ProjectAPI/ReversionProject/' + projectChangeID
            AjaxGETRequest(
                url,
                function (response) {
                    response = SafeJSONparse(response);
                    if (response.WasSuccessful) {
                        AlertWarning("Reversioned project!");
                        RefreshDataView();
                    }
                    else {
                        toastr.error("Alas! Error reversioning project: " + response.Message);
                    }
                },
                function (error) {

                }, true, true, true
            );
        });
    }
    catch (ex) {
        toastr.error("Error while reversioning project: " + ex.message);
    }
}
function LoadProjectReversionView(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "ProjectAPI/ProjectReversionGridViewResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Project reversion tracking in grid: ' + ex.message);
    }
}


function DisplayMacroTrackingForProjectInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "ProjectAPI/MacroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the project in grid: ' + ex.message);
    }
}
function DisplayMacroTrackingForProjectInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "ProjectAPI/MacroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the project in timeline: ' + ex.message);
    }
}

function DisplayMicroTrackingForProjectInGrid(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "ProjectAPI/MicroTrackingGridResource/" + recordID;
        LoadGridView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Micro Tracking for the project in grid: ' + ex.message);
    }
}
function DisplayMicroTrackingForProjectInTimeLine(recordID = null) {
    try {
        if (IsNullOrEmpty(recordID)) return;
        var resourceUrl = "ProjectAPI/MicroTrackingTimeLineRead/" + recordID;
        LoadTimeLineView(resourceUrl, true, true, divMainPage);
    }
    catch (ex) {
        toastr.error('Error while displaying Macro Tracking for the project in timeline: ' + ex.message);
    }
}


function LoadMileStones(recordId = null) {
    try {
        if (IsNullOrEmpty(recordId)) return;
        LoadGridView("MilestoneAPI/Resource/" + recordId);
    }
    catch (ex) {
        toastr.error("Error while loading list of milestones: " + ex.message);
    }
}
function LoadMileStonesHierarchy(recordId = null) {
    try {
        if (IsNullOrEmpty(recordId)) return;
        LoadGridView("MilestoneAPI/WorkHierarchyResource/" + recordId);
    }
    catch (ex) {
        toastr.error("Error while loading list of milestones: " + ex.message);
    }
}