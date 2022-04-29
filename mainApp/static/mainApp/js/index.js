const products_list = document.querySelector(".products-list");
const catagory_btns = document.querySelectorAll(".catagory-btn");
const location_search = document.getElementById("location-search");
const text_search = document.getElementById("text-search");
const fav_btns = document.querySelectorAll(".fav-btn");

fav_btns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    add_fav(e.target.id);
  });
});

function add_fav(product_id) {
  const url = "http://127.0.0.1:8000/product/add-fav/";
  const csrftoken = getCookie("csrftoken");
  const data = JSON.stringify({ product_id: product_id });
  fetch(url, {
    body: data,
    headers: {
      "X-CSRFToken": csrftoken,
    },
    method: "POST",
  })
    .then((jresp) => jresp.json())
    .then((resp) => {
      if (resp["message"]) {
        alert(resp["message"]);
      }
    });
}

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

catagory_btns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const data = { catagory: e.target.getAttribute("catagory") };
    search_products(data);
  });
});

text_search.addEventListener("keyup", (e) => {
  const data = { search_text: text_search.value };
  if (text_search.value.length == 0) {
    const data = { empty: true };
    search_products(data);
  }
  search_products(data);
});

location_search.addEventListener("keyup", (e) => {
  const data = { search_location: location_search.value };
  search_products(data);
});

function search_products(data) {
  const csrftoken = getCookie("csrftoken");
  const url = "http://127.0.0.1:8000/product/search/";
  fetch(url, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then((jresp) => jresp.json())
    .then((resp) => render_products(resp));
}

function render_products(resp) {
  products_list.innerHTML = "";
  for (const prod of resp) {
    products_list.appendChild(product_el(prod));
  }
}

function product_el(product) {
  let div = document.createElement("div");
  div.className = "col-lg-3 offset-lg-0 col-md-5 offset-md-1 col-sm-6 col-6";
  const img_url = "http://127.0.0.1:8000/media/" + product["fields"]["image"];
  let item_url =
    "http://127.0.0.1:8000/product/product-details/" + product.pk + "/";
    let stars=product.fields.total_rating/product.fields.no_rating
  let checked_stars = "";
  for (i = 1; i <= stars; i++) {
    checked_stars += '<span class="fa fa-star checked"></span>';
  }

  div.innerHTML = `
	<!-- product card -->
        <div class="product-item bg-light">
            <div class="card">
                <div class="thumb-content">
                    <!-- <div class="price">${product.fields.price}</div> -->
                    <a href="${item_url}">
                        <img class="card-img-top img-fluid" src="${img_url}" alt="Card image cap">
                    </a>
                </div>
                <div class="card-body">
                    <h4 class="card-title"><a href="${item_url}">${product.fields.title}</a></h4>
                    <ul class="list-inline product-meta">
                        <!-- Name of user -->
                        <li class="list-inline-item">
                            <a href="#" class=""><i class="fa fa-user"></i>by: ${product.fields.seller}</a>
                        </li>
                        <li class="list-inline-item">
                            <a href="${item_url}"><i class="fa fa-folder-open-o"></i>${product.fields.catagory}</a>
                        </li>
                        <li class="list-inline-item">
                            <a href="${item_url}"><i class="fa fa-calendar"></i>${product.fields.address}</a>
                        </li>
                    </ul>

                    <p class="card-text"> ${product.fields.price}$<br>
                       ${product.fields.desc}</p>

                       ${checked_stars}
                    <!-- ADD THIS POST TO FAVORITES  -->
                    <div class="float-right ">
                        <a href="" class="">
                            <i class="fa fa-bookmark-o "></i>
                        </a>

                    </div>

                </div>

            </div>
        </div>
`;
  return div;
}
