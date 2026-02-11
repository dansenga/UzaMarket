/* ===========================================
   UzaMarket — JavaScript principal
   =========================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ── Preloader ──────────────────────────
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', function () {
            preloader.classList.add('loaded');
        });
        // Fallback : retire le preloader après 3s max
        setTimeout(function () {
            preloader.classList.add('loaded');
        }, 3000);
    }

    // ── Navbar scroll effect ───────────────
    const navbar = document.querySelector('.navbar-uzashop');
    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.classList.toggle('scrolled', window.scrollY > 40);
        });
    }

    // ── Auto-dismiss alerts ────────────────
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ── Confirm delete buttons ─────────────
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm || 'Êtes-vous sûr ?')) {
                e.preventDefault();
            }
        });
    });

    // ── Scroll reveal animation ────────────
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length) {
        const revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        revealElements.forEach(function (el) {
            revealObserver.observe(el);
        });
    }

    // ── Staggered card animation ───────────
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function (card, index) {
        card.style.animationDelay = (index * 0.08) + 's';
        card.style.opacity = '0';
        card.style.animation = 'cardFadeIn 0.5s ease forwards';
        card.style.animationDelay = (index * 0.08) + 's';
    });

    // ── HTMX cart badge bounce ─────────────
    document.body.addEventListener('htmx:afterSwap', function () {
        const badge = document.getElementById('cart-badge');
        if (badge) {
            badge.style.animation = 'none';
            badge.offsetHeight; // reflow
            badge.style.animation = 'badgePop 0.3s ease';
        }
    });

    // ── Smooth scroll for anchor links ─────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});

/* Card fade-in keyframe */
var styleSheet = document.createElement('style');
styleSheet.textContent = '@keyframes cardFadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }';
document.head.appendChild(styleSheet);
