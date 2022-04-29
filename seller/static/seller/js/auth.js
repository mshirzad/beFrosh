function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function Form_data(form) {
  let data = {};
  for (const inp of form) {
    inp.classList.remove("input-error");
    if (inp.tagName == "INPUT") {
      data[inp.id] = inp.value;
    }
  }
  return data;
}

function show_message(resp, id) {
  if (resp["error-key"]) {
    document.getElementById(resp["error-key"]).classList.add("input-error");
  }
  if (resp["error"] && id) {
    document.getElementById(id).style.display = "block";
    document.getElementById(id).innerHTML = clean_msg(resp["message"]);
  } else {
    if (resp["success_url"]) {
      window.location = resp["success_url"];
    }
  }
}

function clean_msg(msg) {
  let new_msg = [];
  for (let i = 0; i < msg.length; i++) {
    let is_true = msg[i].match(/[a-z]/i);
    if (is_true) {
      new_msg.push(msg[i]);
    } else if (msg[i] == " ") {
      new_msg.push("&nbsp");
    } else {
      new_msg.push("&nbsp");
    }
  }
  console.log(new_msg);
  return new_msg.join("");
}
