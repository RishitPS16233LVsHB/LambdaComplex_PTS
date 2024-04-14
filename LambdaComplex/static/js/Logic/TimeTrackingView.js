var timeTrackingViewIds = {
    ResourceURL: "#TIME_RESOURCE_URL",
    RenderType: "#TIME_RENDER_TYPE",

    // calendar view
    calendarReadUrl: "#CALENDAR_READ_URL",
    calendarCreateViewUrl: "#CALENDAR_CREATE_VIEW_URL",
    calendarGridViewResourceUrl: "#CALENDAR_GRIDVIEW_RESOURCE_URL",
    calendarSelectedDate: "#CALENDAR_SELECTED_DATE",
    // timeline view
    timeLineViewReadUrl: "#TIMELINE_READ_URL",

    // context buttons
    contextCreate: "#CreateCalendar",
    contextGridView: "#GridViewCalendar",
    contextTimeLineView: "#TimeLineViewCalendar",
};


function InitTimeTrackingView() {

    try {
        document.addEventListener('contextmenu', HideCalendarContextMenu);

        let resourceURL = $(timeTrackingViewIds.ResourceURL).val();
        let renderType = $(timeTrackingViewIds.RenderType).val();
        switch (renderType.toLowerCase()) {
            case "calendar":
                InitCalendarView(resourceURL);
                break;
            default:
                InitTimeLineView(resourceURL); // resource and read url are same for timeline
                break;
        };

    }
    catch (e) {
        toastr.error("Error occured while initializing Time Tracking View: " + e.message);
    }
}

function InitCalendarView(resourceURL) {
    try {
        // to get resources
        AjaxGETRequest(resourceURL,
            function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    var resourceData = response.Data;

                    var calendarReadUrl = resourceData.CalendarReadUrl
                    $(timeTrackingViewIds.calendarReadUrl).val(calendarReadUrl);

                    if (!IsNullOrEmpty(resourceData.CreateViewUrl))
                        $(timeTrackingViewIds.calendarCreateViewUrl).val(resourceData.CreateViewUrl);
                    else
                        $(timeTrackingViewIds.contextCreate).remove();

                    if (!IsNullOrEmpty(resourceData.GridViewResourceUrl))
                        $(timeTrackingViewIds.calendarGridViewResourceUrl).val(resourceData.GridViewResourceUrl);
                    else
                        $(timeTrackingViewIds.contextGridView).remove();

                    if (!IsNullOrEmpty(resourceData.TimeLineViewReadUrl))
                        $(timeTrackingViewIds.timeLineViewReadUrl).val(resourceData.TimeLineViewReadUrl);
                    else
                        $(timeTrackingViewIds.contextTimeLineView).remove();

                    var eventCount = QuickAPIRead(calendarReadUrl);
                    // init blank calendar incase of data read failure
                    if (eventCount.length == 0 || IsNullOrEmpty(eventCount)) {
                        var calendar = $("#timeTrackingView").calendarGC({
                            dayBegin: 0,
                            prevIcon: '&#x3c;',
                            nextIcon: '&#x3e;',
                            onclickDate: function (e, data) {

                                var eventDate = new Date(data.datejs.toDateString());
                                $(timeTrackingViewIds.calendarSelectedDate).val(eventDate.toDateString());
                                HideCalendarContextMenu()
                                ShowCalendarContextMenu(e);
                            }
                        });
                        return;
                    }
                    var events = [];
                    for (var i = 0; i < eventCount.length; i++) {
                        events.push({
                            date: new Date(eventCount[i].date),
                            eventName: eventCount[i].eventName,
                            className: eventCount[i].className,
                            dateColor: eventCount[i].dateColor,
                        })
                    }

                    var calendar = $("#timeTrackingView").calendarGC({
                        dayBegin: 0,
                        prevIcon: '&#x3c;',
                        nextIcon: '&#x3e;',
                        events: events,
                        onclickDate: function (e, data) {
                            var eventDate = new Date(data.datejs.toDateString());
                            $(timeTrackingViewIds.calendarSelectedDate).val(eventDate.toDateString());
                            HideCalendarContextMenu();
                            ShowCalendarContextMenu(e, "calendar event");
                        }
                    });
                }
                else {
                    toastr.error(response.Message + " was the error");
                }
            },
            function (error) {

            }, true, true, true
        );
    }
    catch (ex) {
        toastr.error("Error while initing calendar view " + ex.message);
    }
}

function InitTimeLineView(readUrl) {
    try {
        // to get resources
        AjaxGETRequest(readUrl,
            function (response) {
                response = SafeJSONparse(response);
                if (response.WasSuccessful) {
                    var resourceData = response.Data;

                    var timeLineData = resourceData.Data;
                    var dataMapping = resourceData.Mappings;

                    if (timeLineData.length == 0) {
                        toastr.info("no events were present!");
                        return;
                    }

                    var processedEvents = [];
                    for (var i = 0; i < timeLineData.length; i++) {
                        processedEvents.push(
                            {
                                time: timeLineData[i][dataMapping.time],
                                header: timeLineData[i][dataMapping.header],
                                body: [{
                                    tag: 'h1',
                                    content: timeLineData[i][dataMapping.h1Body]
                                },
                                {
                                    tag: 'p',
                                    content: DecodeHtmlEntities(timeLineData[i][dataMapping.paraBody])
                                }],
                                footer: timeLineData[i][dataMapping.footer]
                            }
                        );
                    }

                    $("#divMainPage").albeTimeline(processedEvents, {
                        effect: "zoomIn",
                        showMenu: true,
                        sortDesc: true,
                    });

                }
                else {
                    toastr.error(response.Message + " was the error");
                }
            },
            function (error) {

            }, true, true, true
        );
    }
    catch (ex) {
        toastr.error("Error while initing timeline view " + ex.message);
    }
}

// Attach event listener to the document to show context menu on right-click
document.addEventListener('contextMenu', showContextMenu);

// Attach event listener to the document to hide context menu on click outside
document.addEventListener('click', hideContextMenu);

// Function to show the context menu
function ShowCalendarContextMenu(event, calendarEvent) {
    if (IsNullOrEmpty(calendarEvent)) return;

    event.preventDefault();
    const contextMenu = document.getElementById('TimeLineContextMenu');
    contextMenu.style.display = 'block';
    contextMenu.style.left = event.clientX + 'px';
    contextMenu.style.top = event.clientY + 'px';
}

// Function to hide the context menu
function HideCalendarContextMenu() {
    const contextMenu = document.getElementById('TimeLineContextMenu');
    contextMenu.style.display = 'none';
}

function CreateCalendar() {
    try {
        HideCalendarContextMenu();

        let selectedCalendarDate = $(timeTrackingViewIds.calendarSelectedDate).val();
        var eventDate = new Date(selectedCalendarDate)

        if (eventDate < new Date()) {
            AlertError("Cannot set calendar event for past dates");
            return;
        }

        let dataToSend = {
            selectedCalendarDate: new Date(selectedCalendarDate).toDateString()
        };
        let calendarCreateView = $(timeTrackingViewIds.calendarCreateViewUrl).val();
        SetViewInMainPageUsingPost(calendarCreateView, dataToSend, true, true, "#ModalBody");
        $("#TimeTrackingViewModal").modal('show');
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function GridViewCalendarEvents() {
    try {
        HideCalendarContextMenu();
        ShowLoadingScreen();
        let calendarGridView = $(timeTrackingViewIds.calendarGridViewResourceUrl).val();
        let selectedCalendarDate = new Date($(timeTrackingViewIds.calendarSelectedDate).val())
        let selectedDate = selectedCalendarDate.getFullYear() + "-" + (selectedCalendarDate.getMonth() + 1) + "-" + selectedCalendarDate.getDate();
        let url = calendarGridView + "/" + selectedDate;
        LoadGridView(url, false, false, "#divMainPage");
        $("#btnCreate").remove();
        HideLoadingScreen();
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function TimeLineViewCalendarEvents() {
    try {
        HideCalendarContextMenu();
        ShowLoadingScreen();
        let calendarGridView = $(timeTrackingViewIds.timeLineViewReadUrl).val();
        let selectedCalendarDate = new Date($(timeTrackingViewIds.calendarSelectedDate).val())
        let selectedDate = selectedCalendarDate.getFullYear() + "-" + (selectedCalendarDate.getMonth() + 1) + "-" + selectedCalendarDate.getDate();
        let url = calendarGridView + "/" + selectedDate.replaceAll('-', 'L');
        InitTimeLineView(url);
        $("#btnCreate").remove();
        HideLoadingScreen();
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}

function OtherWay() {
    try {
        HideCalendarContextMenu();

        let calendarTimelineView = $(timeTrackingViewIds.calendarTimeLineViewUrl).val();
        let selectedCalendarDate = $(timeTrackingViewIds.calendarSelectedDate).val();
        let url = calendarTimelineView + "/" + selectedCalendarDate;
        LoadTimeLineView(url, true, true, "#ModalBody");
    }
    catch (ex) {
        toastr.error("Error while loading the Create view: " + ex.message);
    }
}


