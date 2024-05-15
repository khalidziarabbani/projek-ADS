document.addEventListener('DOMContentLoaded', function () {
    const phoneEmail = document.getElementById('phone-email');
    const fullnameUsername = document.getElementById('fullname-username');
    const password = document.getElementById('password');
    const previousBtn = document.getElementById('previous-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');

    let currentStep = 1;

    function validateStep() {
        switch (currentStep) {
            case 1:
                return phoneEmail.querySelector('input[type="text"]').value !== '' &&
                       phoneEmail.querySelector('input[type="email"]').value !== '';
            case 2:
                return fullnameUsername.querySelector('input[type="text"]').value !== '' &&
                       fullnameUsername.querySelector('input[type="text"]').value !== '';
            case 3:
                return password.querySelector('input[type="password"]').value !== '' &&
                       password.querySelector('input[type="password2"]').value !== '';
            default:
                return false;
        }
    }

    function updateButton() {
        previousBtn.classList.toggle('hidden', currentStep === 1);
        nextBtn.classList.toggle('hidden', currentStep === 3);
        submitBtn.classList.toggle('hidden', currentStep !== 3);
    }

    previousBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentStep > 1) {
            currentStep--;
            updateButton();
            switch (currentStep) {
                case 1:
                    phoneEmail.style.display = 'block';
                    fullnameUsername.style.display = 'none';
                    break;
                case 2:
                    fullnameUsername.style.display = 'block';
                    password.style.display = 'none';
                    break;
                default:
                    break;
            }
        }
    });

    nextBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (validateStep()) {
            currentStep++;
            updateButton();
            switch (currentStep) {
                case 2:
                    phoneEmail.style.display = 'none';
                    fullnameUsername.style.display = 'block';
                    break;
                case 3:
                    fullnameUsername.style.display = 'none';
                    password.style.display = 'block';
                    break;
                default:
                    break;
            }
        } else {
            alert('Please fill all fields.');
        }
    });
});
