/* ===========================================
   UzaShop - JavaScript principal
   =========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss des alertes après 5 secondes
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmation avant suppression
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || 'Êtes-vous sûr ?')) {
                e.preventDefault();
            }
        });
    });

    // Animation du badge panier lors de l'ajout HTMX
    document.body.addEventListener('htmx:afterSwap', function(event) {
        const badge = document.getElementById('cart-badge');
        if (badge) {
            badge.classList.add('animate__animated', 'animate__bounceIn');
            setTimeout(() => {
                badge.classList.remove('animate__animated', 'animate__bounceIn');
            }, 1000);
        }
    });
});
