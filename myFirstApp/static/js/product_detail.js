function toggleDescription(button) {
    removeActiveClass();
    document.getElementById('description').classList.remove('hidden');
    document.getElementById('specification').classList.add('hidden');
    button.classList.add('active');
}

function toggleSpecification(button) {
    removeActiveClass();
    document.getElementById('description').classList.add('hidden');
    document.getElementById('specification').classList.remove('hidden');
    button.classList.add('active');

}

function removeActiveClass() {
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });
}