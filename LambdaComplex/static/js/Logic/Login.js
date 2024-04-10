/**
 * Checks for User Login by calling MVC Controller
 */
function CheckLogin() {
    try {

        var form = document.getElementById("FORM");
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        };


        var username = $("#txt-username").val();
        var password = $("#txt-password").val();

        var dataToSend = {
            UserName: username,
            Password: password
        }

        var url = "Login/UserLogin";
        AjaxPOSTRequest(url, dataToSend, function (res) {
            let recievedData = res;

            $("#loader-screen").show();
            if (recievedData.WasSuccessful) {
                window.location.href = "/";
            }
            else {
                $("#loader-screen").hide();
                Swal.fire({
                    icon: 'error',
                    title: 'Alas!',
                    text: 'Provided password and username were wrong...\n Please try again...',
                    confirmButtonText: 'OK'
                });
            }
        }, function (err) {
            toastr.error("AJAX error Occured due to: " + err.message);
        }, true, true, false);

    }
    catch (e) {
        toastr.error("Error in login: " + e.message);
    }
}