 const changepass_form = document.getElementById("changepass-form");

if (changepass_form) {
  changepass_form.addEventListener("submit", (e) => {
    e.preventDefault();
    changepass();
  });
}

function changepass() {
  const csrftoken = getCookie("csrftoken");
  const data = JSON.stringify(Form_data(changepass_form));
  const url = "http://127.0.0.1:8000/seller/change-password/";
  fetch(url, {
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
    },
    body: [data],
    method: "POST",
  })
    .then((jresp) => jresp.json())
    .then((resp) => {
      show_message(resp, "changepass-error");
    })
    .catch((error) => {
      console.log(error);
    });
}
