// Lake Guardian JavaScript

// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Image preview for file uploads
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image-preview');
            if (preview) {
                preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 300px; border-radius: 8px;">`;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Dashboard charts (placeholder for future implementation)
function initDashboard() {
    // This would initialize charts and visualizations
    console.log('Dashboard initialized');
}

// Location autocomplete (placeholder)
function initLocationAutocomplete() {
    // This would integrate with a maps API for location suggestions
    console.log('Location autocomplete initialized');
}

// Initialize features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize features based on current page
    if (document.getElementById('dashboard')) {
        initDashboard();
    }
    
    if (document.getElementById('location')) {
        initLocationAutocomplete();
    }
    
    // File upload preview
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            previewImage(this);
        });
    }
});
