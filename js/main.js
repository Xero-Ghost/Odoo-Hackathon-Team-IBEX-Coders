// Main JavaScript file for Skill Swap Platform

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Form validation enhancement
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Search functionality
function performSearch() {
    var searchInput = document.getElementById('searchInput');
    var searchTerm = searchInput.value.toLowerCase();
    var skillCards = document.querySelectorAll('.skill-card');
    
    skillCards.forEach(function(card) {
        var skillName = card.querySelector('.card-title').textContent.toLowerCase();
        var skillDescription = card.querySelector('.card-text').textContent.toLowerCase();
        
        if (skillName.includes(searchTerm) || skillDescription.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Loading state management
function showLoading(elementId) {
    var element = document.getElementById(elementId);
    if (element) {
        element.classList.add('loading');
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    }
}

function hideLoading(elementId, originalContent) {
    var element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
        element.innerHTML = originalContent;
    }
}

// Rating system
function setRating(rating) {
    var stars = document.querySelectorAll('.rating-star');
    var ratingInput = document.getElementById('rating');
    
    stars.forEach(function(star, index) {
        if (index < rating) {
            star.classList.add('fas');
            star.classList.remove('far');
        } else {
            star.classList.add('far');
            star.classList.remove('fas');
        }
    });
    
    if (ratingInput) {
        ratingInput.value = rating;
    }
}

// Dynamic skill matching
function findSkillMatches() {
    var userSkills = document.querySelectorAll('.user-skill');
    var wantedSkills = document.querySelectorAll('.wanted-skill');
    var matches = [];
    
    userSkills.forEach(function(userSkill) {
        var userSkillName = userSkill.textContent.toLowerCase();
        
        wantedSkills.forEach(function(wantedSkill) {
            var wantedSkillName = wantedSkill.textContent.toLowerCase();
            
            if (userSkillName.includes(wantedSkillName) || wantedSkillName.includes(userSkillName)) {
                matches.push({
                    userSkill: userSkill,
                    wantedSkill: wantedSkill
                });
            }
        });
    });
    
    return matches;
}

// Swap request form enhancement
function updateSwapRequestForm() {
    var skillOfferedSelect = document.getElementById('skill_offered_id');
    var skillWantedSelect = document.getElementById('skill_wanted_id');
    var messageTextarea = document.getElementById('message');
    
    if (skillOfferedSelect && skillWantedSelect && messageTextarea) {
        var offeredSkill = skillOfferedSelect.options[skillOfferedSelect.selectedIndex].text;
        var wantedSkill = skillWantedSelect.options[skillWantedSelect.selectedIndex].text;
        
        var defaultMessage = `Hi! I'd like to exchange my ${offeredSkill} skills for your ${wantedSkill} expertise. When would be a good time to connect?`;
        
        if (messageTextarea.value === '') {
            messageTextarea.value = defaultMessage;
        }
    }
}

// Notification system
function showNotification(message, type = 'info') {
    var notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    var container = document.querySelector('.container');
    if (container) {
        container.insertBefore(notification, container.firstChild);
        
        setTimeout(function() {
            notification.remove();
        }, 5000);
    }
}

// Admin panel functionality
function toggleUserBan(userId, currentStatus) {
    var action = currentStatus === 'banned' ? 'unban' : 'ban';
    var message = `Are you sure you want to ${action} this user?`;
    
    if (confirm(message)) {
        window.location.href = `/admin/${action}_user/${userId}`;
    }
}

// Export functionality
function exportData(type) {
    showNotification(`Exporting ${type} data...`, 'info');
    
    // This would typically make an AJAX request to generate and download the report
    setTimeout(function() {
        showNotification(`${type} data exported successfully!`, 'success');
    }, 2000);
}

// Real-time updates (would typically use WebSockets)
function checkForUpdates() {
    // This would check for new swap requests, messages, etc.
    // For now, we'll just update the notification badge
    var badge = document.querySelector('.badge');
    if (badge) {
        // Update badge count if needed
    }
}

// Initialize real-time updates
setInterval(checkForUpdates, 30000); // Check every 30 seconds

// Skill category filtering
function filterByCategory(category) {
    var skillCards = document.querySelectorAll('.skill-card');
    
    skillCards.forEach(function(card) {
        var cardCategory = card.getAttribute('data-category');
        
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Profile visibility toggle
function toggleProfileVisibility() {
    var checkbox = document.getElementById('is_public');
    var visibilityStatus = document.getElementById('visibility-status');
    
    if (checkbox && visibilityStatus) {
        visibilityStatus.textContent = checkbox.checked ? 'Public' : 'Private';
        visibilityStatus.className = checkbox.checked ? 'badge bg-success' : 'badge bg-secondary';
    }
}

// Initialize page-specific functionality
function initializePage() {
    var path = window.location.pathname;
    
    if (path.includes('/profile')) {
        // Profile page specific initialization
        var visibilityToggle = document.getElementById('is_public');
        if (visibilityToggle) {
            visibilityToggle.addEventListener('change', toggleProfileVisibility);
        }
    }
    
    if (path.includes('/browse_skills')) {
        // Browse skills page specific initialization
        var categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', function() {
                filterByCategory(this.value);
            });
        }
    }
    
    if (path.includes('/request_swap')) {
        // Swap request page specific initialization
        var skillSelects = document.querySelectorAll('select[name*="skill"]');
        skillSelects.forEach(function(select) {
            select.addEventListener('change', updateSwapRequestForm);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage);