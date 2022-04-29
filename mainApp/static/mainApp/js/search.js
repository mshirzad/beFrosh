let rating_search=document.getElementById('rating-search')


rating_search.addEventListener("change", (e) => {
  const data = { [e.target.value]: rating_search.value };
  search_products(data);
});