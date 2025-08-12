// Cart JavaScript functionality for quantity adjustment

function updateQuantity(itemId, change) {
    const quantityDisplay = document.getElementById(`quantity-${itemId}`);
    const totalDisplay = document.getElementById(`total-${itemId}`);
    const cartTotal = document.getElementById('cart-total');

    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `action=${change > 0 ? 'increase' : 'decrease'}`
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.removed) {
                    // Remove the item from DOM
                    const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
                    if (itemElement) {
                        itemElement.remove();
                    }
                } else {
                    // Update quantity display
                    quantityDisplay.textContent = data.new_quantity;

                    // Update item total
                    totalDisplay.textContent = `$${data.new_total}`;
                }

                // Update cart total
                cartTotal.textContent = data.cart_total;

                // Check if cart is empty
                const cartItems = document.querySelectorAll('.cart-item');
                if (cartItems.length === 0) {
                    location.reload();
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

function removeItem(itemId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        fetch(`/cart/remove-item/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the item from DOM
                    const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
                    if (itemElement) {
                        itemElement.remove();
                    }

                    // Update cart total
                    document.getElementById('cart-total').textContent = data.cart_total;

                    // Check if cart is empty
                    const cartItems = document.querySelectorAll('.cart-item');
                    if (cartItems.length === 0) {
                        location.reload();
                    }
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add event listeners for quantity buttons
document.addEventListener('DOMContentLoaded', function () {
    // Add any additional initialization here if needed
    console.log('Cart JavaScript loaded successfully');
});
