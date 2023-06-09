document.addEventListener('DOMContentLoaded', function() {
    var quantityInput = document.getElementById('quantity');
    var priceDisplay = document.getElementById('price');
    
    quantityInput.addEventListener('input', function() {
      var selectedCoin = document.getElementById('coin').value;
      var price = calculatePrice(selectedCoin, parseInt(this.value));
      priceDisplay.textContent = price + ' won';
    });
    
    function calculatePrice(coin, quantity) {
      return quantity * 100;
    }
  });