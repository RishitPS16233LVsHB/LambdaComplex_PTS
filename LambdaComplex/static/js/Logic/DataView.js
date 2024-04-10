var dataViewIds = {
    ResourceURL: "#RESOURCE_URL",
    RenderType: "#RENDER_TYPE",
    CreateView: "#CREATE_VIEW_URL",
    UpdateView: "#UPDATE_VIEW_URL",
    InformaticView: "#INFORMATIC_VIEW_URL",
    DeleteUrl: "#DELETE_URL",
}


function InitDataView() {

    try {

        let resourceURL = $(dataViewIds.ResourceURL).val();
        let renderType = $(dataViewIds.RenderType).val();
        switch (renderType.toLowerCase()) {
            case "list":
                InitListView(resourceURL);
                break;
            default:
                InitGridView(resourceURL);
                break;
        };

    }
    catch (e) {
        toastr.error("Error occured while initializing Data View: " + e.message);
    }
}

function InitGridView(resourceURL) {
    try {
        let readUrl = "";

        // to get resources
        AjaxGETRequest(resourceURL,
            function (response) {

                if (response.WasSuccessful) {

                    var resourceData = response.Data;
                    resourceData = SafeJSONparse(resourceData);

                    template = resourceData.Template;
                    readUrl = resourceData.ReadURL;
                    debugger;

                    createViewUrl = resourceData.CreateViewUrl;
                    updateViewUrl = resourceData.UpdateViewUrl;
                    informaticView = resourceData.InformaticView;
                    deleteUrl = resourceData.DeleteUrl;

                    $(dataViewIds.CreateView).val(createViewUrl);
                    $(dataViewIds.UpdateView).val(updateViewUrl);
                    $(dataViewIds.InformaticView).val(informaticView);
                    $(dataViewIds.DeleteUrl).val(deleteUrl);

                    $("#dataView").kendoGrid({
                        dataSource: {
                            transport: {
                                read: function (options) {
                                    ReadData(readUrl, options);
                                },
                            },
                            pageSize: 3,
                            schema: {
                                model: {
                                    fields: SafeJSONparse(resourceData.Fields),
                                }
                            }
                        },
                        height: IsNullOrEmpty(resourceData.GridHeight) ? "90%" : resourceData.GridHeight,
                        sortable: true,
                        pageable: true,
                        resizable: true,
                        groupable: true,
                        filterable: true,
                        searchable: true,
                        noRecords: true,
                        messages: {
                            noRecords: "There are no records..."
                        },
                        toolbar: ["excel", "pdf"],

                        excel: {
                            allPages: true,
                        },
                        pdf: {
                            allPages: true,
                        },

                        columns: SafeJSONparse(resourceData.Columns),
                        dataBound: function (e) {
                            var grid = this;
                            grid.tbody.find("[id^='progressBar']").each(function () {
                                var id = $(this).attr("id").replace("progressBar", "");
                                $(this).kendoProgressBar({
                                    type: "percent",
                                    value: grid.dataItem("tr").Progress
                                });
                            });

                            grid.tbody.find("[id^='ratingBar']").each(function () {
                                var id = $(this).attr("id").replace("ratingBar", "");
                                $(this).kendoRating({
                                    value: grid.dataItem("tr").Rating
                                });
                            });

                            grid.tbody.find("[id^='badge']").each(function () {
                                var id = $(this).attr("id").replace("badge", "");
                                var availability = grid.dataItem("tr").availability;
                                $(this).kendoBadge({
                                    themeColor: availability ? "success" : "error",
                                    text: availability ? "available" : "not available   "
                                });
                            });
                        },
                    });

                }
                else {
                    toastr.error(response.Message + " was the error");
                }
            },
            function (error) {

            },
            true, true, true
        );
    }
    catch (e) {
        toastr.error("Error occured while initializing Grid view: " + e.message);
    }
}

function InitListView(resourceURL) {
    try {
        let template = "";
        let readUrl = "";

        // to get resources
        AjaxGETRequest(resourceURL,
            function (response) {
                if (response.WasSuccessful) {
                    var resourceData = response.Data;
                    resourceData = SafeJSONparse(resourceData);

                    template = resourceData.Template;
                    readUrl = resourceData.ReadURL;

                    createViewUrl = resourceData.CreateViewUrl;
                    updateViewUrl = resourceData.UpdateViewUrl;
                    informaticView = resourceData.InformaticView;
                    deleteUrl = resourceData.DeleteUrl;

                    $(dataViewIds.CreateView).val(createViewUrl);
                    $(dataViewIds.UpdateView).val(updateViewUrl);
                    $(dataViewIds.InformaticView).val(informaticView);
                    $(dataViewIds.DeleteUrl).val(deleteUrl);

                    $("#dataView").kendoListView({
                        dataSource: {
                            transport: {
                                read: function (options) {
                                    ReadData(readUrl, options);
                                },
                                pageSize: 3,
                                schema: {
                                    model: {
                                        fields: SafeJSONparse(resourceData.Fields),
                                    }
                                }
                            }
                        },
                        height: "90%",
                        template: template,
                    });
                }
                else {
                    toastr.error(response.Message + " was the error");
                }
            },
            function (error) {

            },
            true, true, true
        );
    }
    catch (e) {
        toastr.error("Error occured while initializing List view: " + e.message);
    }
}


function ReadData(readUrl, options) {
    try {
        AjaxGETRequest(readUrl,
            function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    options.success(response.Data);
                }
                else {
                    options.error(null);
                    toastr.error("data not available " + response.Message);
                }
            },
            function (error) {

            },
            true, true, true);
    }
    catch (e) {
        toastr.error("error reading data " + e.message);
    }
}

function LoadCreateView() {
    try {
        let createView = $(dataViewIds.CreateView).val();
        SetViewInMainPageUsingGet(createView, true, true, "#ModalBody");
        $("#DataViewModal").modal('show');
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function LoadUpdateView(id = null) {
    try {
        let updateView = $(dataViewIds.UpdateView).val();
        if (!IsNullOrEmpty(id))
            updateView += ("/" + id);

        SetViewInMainPageUsingGet(updateView, true, true, "#ModalBody");
        $("#DataViewModal").modal('show');
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function LoadInformaticView(id = null) {
    try {
        let informaticView = $(dataViewIds.InformaticView).val();
        if (!IsNullOrEmpty(id))
            informaticView += ("/" + id);

        SetViewInMainPageUsingGet(informaticView, true, true, "#ModalBody");
        $("#DataViewModal").modal('show');
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function DeleteRecord(id = null) {
    try {
        ConfirmationAlert('Delete Record...', 'Are you sure you want to delete this record?', function (result) {
            let deleteUrl = $(dataViewIds.DeleteUrl).val();
            if (!IsNullOrEmpty(id))
                deleteUrl += ("/" + id);

            AjaxGETRequest(deleteUrl, function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    RefreshDataView();
                    AlertSuccess('Deleted successfully!');
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

function RefreshDataView() {
    try {

        let renderType = $(dataViewIds.RenderType).val();
        switch (renderType.toLowerCase()) {
            case "list":
                $("#dataView").data("kendoListView").dataSource.read();
                break;
            default:
                $("#dataView").data("kendoGrid").dataSource.read();
                break;
        };
    }
    catch (ex) {
        toastr.error("error refreshing data view: " + ex.message);
    }
}
