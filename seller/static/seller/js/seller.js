const profile_form = document.getElementById("profile-change-form");

if (profile_form) {
  profile_form.addEventListener("submit", (e) => {
    e.preventDefault();
    change_profile();
    update_usrpic();

  });
}

function change_profile() {
  const url = "http://127.0.0.1:8000/seller/become-seller/";
  const csrftoken = getCookie("csrftoken");
  const data = JSON.stringify(Form_data(profile_form));

  fetch(url, {
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
    },
    method: "POST",
    body: data,
  })
    .then((jresp) => jresp.json())
    .then((resp) => {
      show_message(resp, "update-error-msg");
    });
  update_usrpic();
}


function update_usrpic() {
  let f_data = new FormData();
  const url = "http://127.0.0.1:8000/seller/change-usrpic/";
  const usrpic = document.getElementById("usrpic");
  const csrftoken = getCookie("csrftoken");

  f_data.append("usrpic", usrpic.files[0]);
  console.log("updated");
  fetch(url, {
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
    body: f_data,
  });
}