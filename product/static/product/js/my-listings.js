let delete_btns = document.querySelectorAll(".delete");


delete_btns.forEach((btn) => {
   btn.addEventListener("click", (e) => {
    e.preventDefault();
    delete_item(e.target.id);
  });
});

function delete_item(product_id) {
  const csrftoken = getCookie("csrftoken");
  const url = "http://127.0.0.1:8000/product/delete-product/";
  const data = JSON.stringify({ product_id: product_id });
  fetch(url, {
    body: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
  })
    .then((jresp) => jresp.json())
    .then((resp) => alert(resp.message))
    .catch((error) => console.log(error));
}
