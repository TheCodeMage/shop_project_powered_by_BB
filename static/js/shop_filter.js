// static/js/shop_filter.js

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const productCards = document.querySelectorAll(".product-card");

    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase();

        productCards.forEach(card => {
            const name = card.getAttribute("data-name");

            if (name.includes(filter)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
