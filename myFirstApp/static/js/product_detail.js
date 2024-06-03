function toggleDescription(button) {
    document.getElementById('description').classList.add('visible');
    document.getElementById('description').classList.remove('hidden');
    document.getElementById('specification').classList.add('hidden');
    document.getElementById('specification').classList.remove('visible');
    
    button.classList.add('active');
    document.getElementById('specificationBtn').classList.remove('active');
}

function toggleSpecification(button) {
    document.getElementById('specification').classList.add('visible');
    document.getElementById('specification').classList.remove('hidden');
    document.getElementById('description').classList.add('hidden');
    document.getElementById('description').classList.remove('visible');
    
    button.classList.add('active');
    document.getElementById('descriptionBtn').classList.remove('active');
}

function increaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    const maxValue = parseInt(quantityInput.max);
    if (currentValue < maxValue) {
        quantityInput.value = currentValue + 1;
        updateSubtotal();
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    const minValue = parseInt(quantityInput.min);
    if (currentValue > minValue) {
        quantityInput.value = currentValue - 1;
        updateSubtotal();
    }
}

function validateQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    const maxValue = parseInt(quantityInput.max);
    const minValue = parseInt(quantityInput.min);
    if (currentValue > maxValue) {
        quantityInput.value = maxValue;
    } else if (currentValue < minValue) {
        quantityInput.value = minValue;
    }
    updateSubtotal();
}

function updateSubtotal() {
    const quantityInput = document.getElementById('quantityInput');
    const currentValue = parseInt(quantityInput.value);
    const productPrice = parseFloat(document.getElementById('productPrice').innerText.replace('$', ''));
    const subtotal = currentValue * productPrice;
    document.getElementById('subtotal').innerText = `$${subtotal.toFixed(2)}`;
}
