/**
 * PulseFit Favorites AJAX Handler
 * Enables instant bookmarking/saving of workouts without full page reloads.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Delegate clicks for all favorite buttons
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.card-fav-btn') || e.target.closest('.js-fav-toggle');
        if (!btn) return;

        e.preventDefault();
        e.stopPropagation();

        const workoutId = btn.getAttribute('data-workout-id');
        if (!workoutId) return;

        // Visual feedback immediately
        const heartIcon = btn.querySelector('.fav-icon') || btn;

        try {
            const response = await fetch(`/api/favorites/toggle/${workoutId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.status === 401) {
                if (window.showToast) {
                    window.showToast('Please log in to save workouts to your dashboard!', 'error');
                } else {
                    alert('Please log in to save workouts.');
                }
                setTimeout(() => {
                    window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
                }, 1200);
                return;
            }

            const data = await response.json();

            if (data.success) {
                if (data.is_favorite) {
                    btn.classList.add('active');
                    btn.setAttribute('aria-label', 'Remove from favorites');
                    if (heartIcon.tagName === 'SPAN' || heartIcon.classList.contains('fav-icon')) {
                        heartIcon.innerHTML = '&#9829;'; // Filled heart
                    }
                } else {
                    btn.classList.remove('active');
                    btn.setAttribute('aria-label', 'Save to favorites');
                    if (heartIcon.tagName === 'SPAN' || heartIcon.classList.contains('fav-icon')) {
                        heartIcon.innerHTML = '&#9825;'; // Outline heart
                    }
                    
                    // If on dashboard, optionally remove the card
                    const dashboardCard = btn.closest('.dashboard-workout-card');
                    if (dashboardCard) {
                        dashboardCard.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                        dashboardCard.style.opacity = '0';
                        dashboardCard.style.transform = 'scale(0.9)';
                        setTimeout(() => dashboardCard.remove(), 400);
                    }
                }

                if (window.showToast) {
                    window.showToast(data.message, data.is_favorite ? 'success' : 'info');
                }
            } else {
                if (window.showToast) {
                    window.showToast(data.message || 'Action failed', 'error');
                }
            }
        } catch (err) {
            console.error('Favorites Error:', err);
            if (window.showToast) {
                window.showToast('Network error while updating favorite.', 'error');
            }
        }
    });
});
