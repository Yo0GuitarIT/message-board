function validateForm(inputElementId, errorElementId, errorMessage) {
  let inputValue = document.getElementById(inputElementId).value;
  let errorText = document.getElementById(errorElementId);

  if (inputValue.trim() === "") {
    errorText.innerHTML = errorMessage;
    errorText.style.display = "block";
    return false;
  } else {
    errorText.style.display = "none";
    return true;
  }
}

let validateFormForSignup = () => {
  return (
    validateForm(
      "registerName",
      "errorTextForSignup",
      "Please enter your Name"
    ) &&
    validateForm(
      "registerUsername",
      "errorTextForSignup",
      "Please enter your Username"
    ) &&
    validateForm(
      "registerPassword",
      "errorTextForSignup",
      "Please enter your Password"
    )
  );
};

let validateFormForSignin = () => {
  return (
    validateForm(
      "signinUsername",
      "errorTextForSignin",
      "Please enter your Username"
    ) &&
    validateForm(
      "signinPassword",
      "errorTextForSignin",
      "Please enter your Password"
    )
  );
};

function hideErrorMessage(errorTextFor) {
  document.getElementById(errorTextFor).style.display = "none";
}

hideErrorMessage("errorTextForSignup");
hideErrorMessage("errorTextForSignin");

document.getElementById("registerName").addEventListener("input", function () {
  hideErrorMessage("errorTextForSignup");
});
document
  .getElementById("registerUsername")
  .addEventListener("input", function () {
    hideErrorMessage("errorTextForSignup");
  });
document
  .getElementById("registerPassword")
  .addEventListener("input", function () {
    hideErrorMessage("errorTextForSignup");
  });
document
  .getElementById("signinUsername")
  .addEventListener("input", function () {
    hideErrorMessage("errorTextForSignin");
  });
document
  .getElementById("signinPassword")
  .addEventListener("input", function () {
    hideErrorMessage("errorTextForSignin");
  });
