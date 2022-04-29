let fave_delete_btns = document.querySelectorAll(".delete");

fave_delete_btns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
    e.preventDefault();
    delete_fave(e.target.id);
  });
});


function delete_fave(product_id) {
  const csrftoken = getCookie("csrftoken");
  const url = "http://127.0.0.1:8000/product/delete-fave/";
  const data = JSON.stringify({ product_id: product_id });
  fetch(url, {
    body: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
  })
    .then((jresp) => jresp.json())
    .then((resp) => {alert(resp.message)})
    .catch((error) => console.log(error));
}
