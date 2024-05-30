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
    quantityInput.value = currentValue + 1;
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}