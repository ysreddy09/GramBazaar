document.addEventListener('DOMContentLoaded', function () {
    // ... (your existing code for image preview)

    const form = document.querySelector('.personal-info-form');
    const removePhotoBtn = document.getElementById('removePhoto');
    const removePhotoField = document.getElementById('removePhotoField');

    // Remove photo
    removePhotoBtn.addEventListener('click', function () {
        // ... (your code)
        removePhotoField.value = 'true'; // Set hidden field to signal removal
    });

    // Submit the form on update with validation
    form.addEventListener('submit', function(event) {
        if (!validateForm()) { // Call a validation function
            event.preventDefault(); // Prevent submission if validation fails
        }
    });

    function validateForm() {
        // Add your client-side validation logic here for postal code, phone number, etc.
        // Example:
        const postalCodeInput = document.getElementById('postalCode');
        if (!postalCodeInput.checkValidity()) {
           alert('Please enter a valid postal code.');
           return false;
        }
        // ... add more validation checks
        return true; // Indicate successful validation
    }
});
