
/**
 * To set User home screen with Session data
 * @param {any} userId
 * @param {any} role
 * @param {any} username
 */
function InitializeHomeScreenForUser(userId, role, username) {
    try {
        //----------- setting important session variables -----------//
        $("#USER_ID").val(userId);
        $("#ROLE").val(role);
        $("#txt-user-name").html(username);

        //--------- do any user init work here ----------------//
    }
    catch (e) {
        toastr.error("Error in InitializeHomeScreenForUser: " + e.message);
    }
}

function GetAllUnreadMessages(userId) {

    // TODO: Implement API to get all Unread message for this user and show it on the Messages tab
    // TODO: if the output of messages has zero unread messages then do nothing else wise show a list view of messages and new messages on the tab icon

    // You should work on :
    // #divMainPage to load the list view for all unread messages
    // 
}