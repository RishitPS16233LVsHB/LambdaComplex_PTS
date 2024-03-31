var dataViewIds = {
    ResourceURL: "#RESOURCE_URL",
    RenderType: "#RENDER_TYPE",
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
        let template = "";
        let readUrl = "";

        // to get resources
        AjaxGETRequest(resourceURL,
            function (response) {
                if (response.WasSuccessful) {

                    var resourceData = response.Data;
                    resourceData = safeJSONparse(resourceData);

                    template = resourceData.Template;
                    readUrl = resourceData.ReadURL;

                    $("#dataView").kendoGrid({
                        dataSource: {
                            transport: {
                                read: function (options) {
                                    ReadData(readUrl, options);
                                },
                            },
                            pageSize: 10,
                            schema: {
                                model: {
                                    fields: safeJSONparse(resourceData.Fields),
                                }
                            }
                        },
                        height: "100%",
                        sortable: true,
                        pageable: true,
                        resizable: true,
                        groupable: true,

                        toolbar: ["excel", "pdf"],

                        excel: {
                            allPages: true,
                        },
                        pdf: {
                            allPages: true,
                        },

                        columns: safeJSONparse(resourceData.Columns),
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
                    resourceData = safeJSONparse(resourceData);

                    template = resourceData.Template;
                    readUrl = resourceData.ReadURL;

                    $("#dataView").kendoListView({
                        dataSource: {
                            transport: {
                                read: function (options) {
                                    ReadData(readUrl, options);
                                },
                                pageSize: 10,
                                schema: {
                                    model: {
                                        fields: safeJSONparse(resourceData.Fields),
                                    }
                                }
                            }
                        },
                        height: "100%",
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

                if (response) {
                    response = safeJSONparse(response);
                    options.success(response);
                }
                else {
                    toastr.error("data not available");
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