/**
 * PulseFit Main JavaScript
 * Handles mobile navbar toggle, alerts, and smooth micro-interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Mobile navigation drawer toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const isOpen = navLinks.classList.contains('open');
            mobileToggle.setAttribute('aria-expanded', isOpen);
            mobileToggle.innerHTML = isOpen ? '&#10005;' : '&#9776;';
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target) && navLinks.classList.contains('open')) {
                navLinks.classList.remove('open');
                mobileToggle.innerHTML = '&#9776;';
            }
        });
    }

    // Auto-dismiss or manual close alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 6000);
    });
});

/**
 * Global Toast Notification
 * @param {string} message - Notification text
 * @param {string} type - 'success', 'error', 'info'
 */
window.showToast = function(message, type = 'success') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = `
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 360px;
        `;
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const bg = type === 'success' ? '#131722' : type === 'error' ? '#261214' : '#131722';
    const border = type === 'success' ? '#ccff00' : type === 'error' ? '#ff4757' : '#00f0ff';
    const textColor = type === 'success' ? '#ccff00' : type === 'error' ? '#ff6b81' : '#00f0ff';

    toast.style.cssText = `
        background: ${bg};
        border: 1px solid ${border};
        border-radius: 12px;
        padding: 12px 18px;
        color: #f8fafc;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateY(20px);
        opacity: 0;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    `;

    toast.innerHTML = `
        <span style="color: ${textColor}; font-size: 1.1rem;">&#9679;</span>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    });

    // Remove after 3.5s
    setTimeout(() => {
        toast.style.transform = 'translateY(10px)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
};
