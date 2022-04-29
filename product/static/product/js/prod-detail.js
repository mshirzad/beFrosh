const post_btn = document.querySelector(".post-btn");
const comment_form = document.getElementById("comment-form");

if (comment_form) {
  comment_form.addEventListener("submit", (e) => {
    e.preventDefault();
    add_comment();
  });
}

function add_comment() {
  const csrftoken = getCookie("csrftoken");

  const text = document.getElementById("text").value;
  const rating = document.getElementById("rating").value;

  let data = JSON.stringify({
    text: text,
    "product-id": post_btn.id,
    rating: rating,
  });
  const url = "http://127.0.0.1:8000/product/add-comment/";

  fetch(url, {
    body: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
  })
    .then((jresp) => jresp.json())
    .then((resp) => show_message(resp, "comment-msg"))
    .catch((error) => console.log(error));
}
