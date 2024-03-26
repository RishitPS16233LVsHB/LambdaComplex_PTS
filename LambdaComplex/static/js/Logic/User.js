let ids = {
    userName: "#txtUserName",
    firstName: "#txtFirstName",
    lastName: "#txtLastName",
    mobileNumber: "#nmMobileNumber",
    role: "#txtRole",
    cmbRole: "#cmbRole",
    emailID: "#emEmailID",
    password: "#pswPassword",
    confirmPassword: "#pswConfirmPassword",
};



function GetUserDetails() {
    try {
        let userId = $(sessionIds.userId).val();
        let url = "UserAPI/GetUserDetails/" + userId;

        AjaxGETRequest(url,
            function (response) {
                if (response.WasSuccessful) {

                    let userDetail = response.Data;
                    $(ids.firstName).val(userDetail.FirstName);
                    $(ids.lastName).val(userDetail.LastName);
                    $(ids.userName).val(userDetail.Username);
                    $(ids.mobileNumber).val(userDetail.MobileNumber);
                    $(ids.emailID).val(userDetail.EmailID);
                    $(ids.role).val(userDetail.Role);
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
        toastr.error("Error occured in GetProfileDetails: " + e.message);
    }
}

function CreateUser() {
    try {
        ConfirmationAlert('Create User!', 'Are you sure to create this user?', function () {
            let userId = $(sessionIds.userId).val();
            let url = "UserAPI/CreateUser";

            // Build JSON object with updated user details
            let userDetails = {
                FirstName: $(ids.firstName).val(),
                LastName: $(ids.lastName).val(),
                UserName: $(ids.userName).val(),
                MobileNumber: $(ids.mobileNumber).val(),
                EmailID: $(ids.emailID).val(),
                Role: $(ids.cmbRole).val(),
                ID: userId,
            };
            AjaxPOSTRequest(url, userDetails,
                function (response) {
                    if (response.WasSuccessful) {
                        toastr.success("User details updated successfully");
                    } else {
                        toastr.error(response.Message + " was the error");
                    }
                },
                function (error) {
                    toastr.error("Error occurred while updating user details");
                },
                true, true, true
            );
        });

    } catch (e) {
        toastr.error("Error occurred in UpdateUserDetail: " + e.message);
    }
}

function UpdateUserDetails() {
    try {
        ConfirmationAlert('Update User!', 'Are you sure you update your profile?', function () {
            let userId = $(sessionIds.userId).val();
            let url = "UserAPI/UpdateUserDetails";

            // Build JSON object with updated user details
            let userDetails = {
                FirstName: $(ids.firstName).val(),
                LastName: $(ids.lastName).val(),
                UserName: $(ids.userName).val(),
                MobileNumber: $(ids.mobileNumber).val(),
                EmailID: $(ids.emailID).val(),
                Role: $(ids.role).val(),
                ID: userId,
            };
            AjaxPOSTRequest(url, userDetails,
                function (response) {
                    if (response.WasSuccessful) {
                        toastr.success("User details updated successfully");
                        // reflect update changes
                        InitializeHomeScreenForUser(userId, userDetails.Role, userDetails.UserName);
                    } else {
                        toastr.error(response.Message + " was the error");
                    }
                },
                function (error) {
                    toastr.error("Error occurred while updating user details");
                },
                true, true, true
            );

        });
    } catch (e) {
        toastr.error("Error occurred in UpdateUserDetail: " + e.message);
    }
}

function CheckPasswords() {
    if ($(ids.confirmPassword).val() !== $(ids.password).val()) {
        toastr.error("confirm password and password must be same");
        return false;
    }
    return true;
}

function ChangePassword() {
    try {
        if (!CheckPasswords()) return;

        Swal.fire({
            title: 'Are you sure?',
            text: "Do you want to change your password?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, change it!'
        }).then((result) => {
            if (result.isConfirmed) {
                let userId = $(sessionIds.userId).val();
                let url = "UserAPI/ChangePassword";

                let userDetails = {
                    Password: $(ids.password).val(),
                    ID: userId,
                };
                AjaxPOSTRequest(url, userDetails,
                    function (response) {
                        if (response.WasSuccessful) {
                            toastr.success("Password changed successfully");
                        } else {
                            toastr.error(response.Message + " was the error");
                        }
                    },
                    function (error) {
                        toastr.error("Error occurred while updating user details");
                    },
                    true, true, true
                );
            }
        });
    } catch (e) {
        toastr.error("Error occurred in UpdateUserDetail: " + e.message);
    }
}