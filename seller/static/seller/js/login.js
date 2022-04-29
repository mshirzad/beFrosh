const login_form = document.getElementById("login-form");

if (login_form) {
  login_form.addEventListener("submit", (e) => {
    e.preventDefault();
    login();
  });
}
function login() {
  const url = "http://127.0.0.1:8000/seller/login/";
  const csrftoken = getCookie("csrftoken");
  const data = JSON.stringify(Form_data(login_form));

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
    },
    body: data,
  })
    .then((jresp) => jresp.json())
    .then((resp) => {
      show_message(resp, "login-error");
    })
    .catch((error) => {
      console.log(error);
    });
}
