// SkillSwap Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Profile visibility toggle
    const profileVisibilityToggle = document.getElementById('profileVisibility');
    if (profileVisibilityToggle) {
        profileVisibilityToggle.addEventListener('change', function() {
            const isPublic = this.checked;
            
            // Send AJAX request to update profile visibility
            fetch('/profile/visibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ is_public: isPublic })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateVisibilityText(isPublic);
                    showToast('Profile visibility updated successfully', 'success');
                } else {
                    // Revert toggle if update failed
                    this.checked = !isPublic;
                    showToast('Failed to update profile visibility', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert toggle if request failed
                this.checked = !isPublic;
                showToast('Network error occurred', 'error');
            });
        });
    }

    // Star rating functionality
    initializeStarRating();

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize skill tag animations
    initializeSkillTags();

    // Initialize search functionality
    initializeSearch();

    // Initialize form validation
    initializeFormValidation();
});

function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

function updateVisibilityText(isPublic) {
    const text = document.querySelector('.profile-visibility small');
    if (text) {
        text.textContent = `Your profile is currently ${isPublic ? 'public' : 'private'}`;
    }
}

function showToast(message, type = 'info') {
    // Create toast element
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = createToastElement(message, type);
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

function createToastElement(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    return toast;
}

function initializeStarRating() {
    const ratingStars = document.querySelectorAll('.rating-star');
    const ratingInput = document.getElementById('rating');
    
    ratingStars.forEach((star, index) => {
        star.addEventListener('click', function() {
            const rating = index + 1;
            if (ratingInput) {
                ratingInput.value = rating;
            }
            
            // Update visual state
            ratingStars.forEach((s, i) => {
                s.classList.toggle('active', i < rating);
            });
        });
        
        star.addEventListener('mouseenter', function() {
            const rating = index + 1;
            
            ratingStars.forEach((s, i) => {
                s.classList.toggle('hover', i < rating);
            });
        });
        
        star.addEventListener('mouseleave', function() {
            ratingStars.forEach(s => s.classList.remove('hover'));
        });
    });
}

function initializeSkillTags() {
    const skillTags = document.querySelectorAll('.skill-tag');
    
    skillTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

function initializeSearch() {
    const searchInput = document.querySelector('input[name="search_query"]');
    const searchForm = document.querySelector('form');
    
    if (searchInput && searchForm) {
        // Add search icon click handler
        const searchIcon = document.querySelector('.input-group-text i');
        if (searchIcon) {
            searchIcon.addEventListener('click', function() {
                searchForm.submit();
            });
        }
        
        // Add enter key handler
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchForm.submit();
            }
        });
    }
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Admin dashboard functions
function downloadReport() {
    // In a real implementation, this would generate and download a report
    showToast('Report generation started. You will receive an email when ready.', 'info');
}

function viewAnalytics() {
    // In a real implementation, this would open an analytics dashboard
    showToast('Analytics dashboard coming soon!', 'info');
}

// Image upload preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Skill management functions
function addSkill(skillName, skillType, category) {
    const formData = new FormData();
    formData.append('skill_name', skillName);
    formData.append('skill_type', skillType);
    formData.append('category', category);
    formData.append('csrf_token', getCsrfToken());
    
    fetch('/profile/add_skill', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Skill added successfully!', 'success');
            // Refresh the skills list
            location.reload();
        } else {
            showToast(data.message || 'Failed to add skill', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Network error occurred', 'error');
    });
}

function removeSkill(skillId, skillType) {
    if (confirm('Are you sure you want to remove this skill?')) {
        fetch(`/profile/remove_skill/${skillType}/${skillId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Skill removed successfully!', 'success');
                // Remove the skill element from DOM
                const skillElement = document.querySelector(`[data-skill-id="${skillId}"]`);
                if (skillElement) {
                    skillElement.remove();
                }
            } else {
                showToast(data.message || 'Failed to remove skill', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Network error occurred', 'error');
        });
    }
}

// Swap request functions
function sendSwapRequest(userId, skillOffered, skillWanted, message) {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('skill_offered', skillOffered);
    formData.append('skill_wanted', skillWanted);
    formData.append('message', message);
    formData.append('csrf_token', getCsrfToken());
    
    fetch('/send_request', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Swap request sent successfully!', 'success');
        } else {
            showToast(data.message || 'Failed to send request', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Network error occurred', 'error');
    });
}

// Animation helpers
function animateElement(element, animation) {
    element.classList.add('animate__animated', `animate__${animation}`);
    
    element.addEventListener('animationend', function() {
        element.classList.remove('animate__animated', `animate__${animation}`);
    }, { once: true });
}

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeLazyLoading();
});
