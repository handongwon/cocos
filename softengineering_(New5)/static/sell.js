document.addEventListener('DOMContentLoaded', function () {
  var quantityInput = document.getElementById('quantity');
  var priceInput = document.getElementById('price');
  var totalPriceInput = document.getElementById('total-price');

  quantityInput.addEventListener('input', calculateTotalPrice);
  priceInput.addEventListener('input', calculateTotalPrice);

  function calculateTotalPrice() {
    var quantity = parseInt(quantityInput.value);
    var price = parseFloat(priceInput.value);

    if (!isNaN(quantity) && !isNaN(price)) {
      var totalPrice = quantity * price;
      totalPriceInput.value = totalPrice;
    } else {
      totalPriceInput.value = '';
    }
  }
});