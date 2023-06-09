document.addEventListener('DOMContentLoaded', function () {
  var quantityInput = document.getElementById('quantity');
  var priceInput = document.getElementById('price');
  var totalPriceOutput = document.getElementById('total-price');

  function calculateTotalPrice() {
    var quantity = parseInt(quantityInput.textContent);
    var price = parseInt(priceInput.textContent);
    var totalPrice = quantity * price;
    totalPriceOutput.textContent = totalPrice;
  }

  calculateTotalPrice();

  quantityInput.addEventListener('input', function () {
    calculateTotalPrice();
  });

  priceInput.addEventListener('input', function () {
    calculateTotalPrice();
  });
});
