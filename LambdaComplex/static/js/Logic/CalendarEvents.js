var calendarEventIds = {
    eventDate: "#dtEventDate",
    eventTime: "#tmEventTime",
    eventName: "#txtEventName",
    eventDescription: "#txtEventDescription",
    eventPriority: "#cmbEventPriority",

    eventId: "#hdnEventId",
}


function CreateCalendarEvent() {
    try {
        if (!ValidateForm()) return;

        let userId = $(sessionIds.userId).val();

        let dataToSend = {
            UserId: userId,
            EventPriority: $(calendarEventIds.eventPriority).val(),
            EventDate: $(calendarEventIds.eventDate).val(),
            EventTime: $(calendarEventIds.eventTime).val(),
            EventDescription: $(calendarEventIds.eventDescription).val(),
            EventName: $(calendarEventIds.eventName).val(),
        }

        let url = "CalendarEventAPI/CreateCalendarEvent/";
        AjaxPOSTRequest(url, dataToSend,
            function (response) {
                try {
                    if (response.WasSuccessful) {
                        AlertSuccess('Event Created!');
                        LoadCalendarView('CalendarEventAPI/CalendarViewResource', true, true)
                    }
                    else {
                        toastr.error('Error occured due to: ' + response.Message);
                    }
                }
                catch (e) {
                    toastr.error('error occured due to : ' + e.message);
                }
            },
            function (error) {
                toastr.error('unexpected error occured due to : ' + error);
            }, true, true, true);

    }
    catch (e) {
        toastr.error("error occured while Getting User calendar events: " + e.message);
    }
}

function UpdateCalendarEvent() {
    try {
        if (!ValidateForm()) return;

        let userId = $(sessionIds.userId).val();

        let dataToSend = {
            EventId: $(calendarEventIds.eventId).val(),
            UserId: userId,
            EventPriority: $(calendarEventIds.eventPriority).val(),
            EventDate: $(calendarEventIds.eventDate).val(),
            EventTime: $(calendarEventIds.eventTime).val(),
            EventDescription: $(calendarEventIds.eventDescription).val(),
            EventName: $(calendarEventIds.eventName).val(),
        }

        let url = "CalendarEventAPI/UpdateCalendarEvent/";
        AjaxPOSTRequest(url, dataToSend,
            function (response) {
                try {
                    if (response.WasSuccessful) {
                        AlertSuccess('Event Updated!');
                        LoadCalendarView('CalendarEventAPI/CalendarViewResource', true, true)
                    }
                    else {
                        toastr.error('Error occured due to: ' + response.Message);
                    }
                }
                catch (e) {
                    toastr.error('error occured due to : ' + e.message);
                }
            },
            function (error) {
                toastr.error('unexpected error occured due to : ' + error);
            }, true, true, true);

    }
    catch (e) {
        toastr.error("error occured while Getting User calendar events: " + e.message);
    }
}

function DeleteCalendarEvent(eventId) {
    try {
        let userId = $(sessionIds.userId).val();
        let url = "CalendarEventAPI/DeleteCalendarEvent/";

        let dataToSend = {
            UserId: userId,
            EventId: eventId,
        };

        AjaxPOSTRequest(url, dataToSend,
            function (response) {
                try {
                    if (response.WasSuccessful) {
                        AlertSuccess('Event Deleted!');
                        LoadCalendarView('CalendarEventAPI/CalendarViewResource', true, true)
                    }
                    else {
                        toastr.error('Error occured due to: ' + response.Message);
                    }
                }
                catch (e) {
                    toastr.error('error occured due to : ' + e.message);
                }
            },
            function (error) {
                toastr.error('unexpected error occured due to : ' + error);
            },
            true, true, true
        );

    }
    catch (e) {
        toastr.error(" error occured while deleting Calendar event: " + e.message);
    }
}

function InitCalendarEventCreate() {
    try {
        var editor = $(calendarEventIds.eventDescription).kendoEditor({
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

        var dateString = new Date($(calendarEventIds.eventDate).attr('valueAttr')).toISOString().slice(0, 10);
        $(calendarEventIds.eventDate).val(dateString);
    }
    catch (ex) {
        toastr.error("error while initing the calendar event create view: " + ex.message);
    }
}