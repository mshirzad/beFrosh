const register_form = document.getElementById("register-form");


if (register_form) {
  register_form.addEventListener("submit", (e) => {
    e.preventDefault();
    register();
  });
}

function register() {
  const url = "http://127.0.0.1:8000/seller/register/";
  const csrftoken = getCookie("csrftoken");
  const data = JSON.stringify(Form_data(register_form));
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
      show_message(resp, "reg-error-msg");
    });
}
