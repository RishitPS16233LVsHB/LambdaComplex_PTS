function InitCalendarEvents() {
    try {

        let userId = $(sessionIds.userId).val();
        let url = "CalendarEventAPI/GetCalendarEvent/" + userId;
        let events = [];

        AjaxGETRequest(url,
            function (response) {
                var events = [];

                if (response.WasSuccessful) {
                    var eventLists = IsNullOrEmpty(response.Data) ? [] : response.Data;

                    for (var i = 0; i < eventLists.length; i++) {
                        events.push({
                            date: new Date(eventLists[i].EventDate),
                            eventName: "<input type='hidden' eventID='" + eventLists[i].ID + "'> <p>" + eventLists[i].EventDescription + "</p>",
                            className: "badge bg-success",
                            dateColor: "green",
                            onclick: function (e) {
                            }
                        });
                    }
                }
                else {
                    toastr.error(response.Message + " was the error");
                }

                var calendar = $("#calendar").calendarGC({
                    dayBegin: 0,
                    prevIcon: '&#x3c;',
                    nextIcon: '&#x3e;',
                    events: events,
                    onclickDate: function (e, data) {
                        var currentDate = new Date();
                        var eventDate = new Date(data.datejs.toDateString());

                        // if there is an event then prompt to delete the event
                        if ($(e.currentTarget).parent().children().length > 1) {

                            var eventId = $($(e.currentTarget).parent().children()[1]).find('input[type="hidden"]').attr('eventid');
                            ConfirmationAlert("Are you sure you want to remove this event?", function () {
                                DeleteCalendarEvent(eventId);
                            });
                        }
                        // else prompt to create an event
                        else {
                            if (eventDate.getTime() < currentDate.getTime()) {
                                AlertError('Date is of past');
                                return;
                            }

                            PromptAlert('textarea', 'Event for the day', 'Enter event', function (value) {
                                var day = new Date(data.datejs.toDateString()).getDate();
                                var month = new Date(data.datejs.toDateString()).getMonth() + 1;
                                var year = new Date(data.datejs.toDateString()).getFullYear();
                                var eventDate = `${year}-${month}-${day}`;
                                CreateCalendarEvent(value, eventDate);
                            });
                        }
                    }
                });

            },
            function (error) {

            },
            true, true, true
        );

    }
    catch (e) {
        toastr.error("error occured while calendar init: " + e.message);
    }
}

function CreateCalendarEvent(value, eventDate) {
    try {
        let userId = $(sessionIds.userId).val();
        let priority = 'LOW';
        let eventDescription = value;

        let dataToSend = {
            UserId: userId,
            EventPriority: priority,
            EventDate: eventDate,
            EventDescription: eventDescription,
        }

        let url = "CalendarEventAPI/CreateCalendarEvent/";
        AjaxPOSTRequest(url, dataToSend,
            function (response) {
                try {
                    if (response.WasSuccessful) {
                        AlertSuccess('Event Created!');
                        InitCalendarEvents();
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
                        InitCalendarEvents();
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