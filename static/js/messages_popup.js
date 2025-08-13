document.addEventListener('DOMContentLoaded', function () {
    // Create overlay element
    const overlay = document.createElement('div');
    overlay.id = 'popup-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.display = 'none';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = 1000;

    // Create popup container
    const popup = document.createElement('div');
    popup.id = 'popup-message';
    popup.style.backgroundColor = '#fff';
    popup.style.padding = '20px';
    popup.style.borderRadius = '8px';
    popup.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
    popup.style.maxWidth = '400px';
    popup.style.textAlign = 'center';

    // Create message text element
    const messageText = document.createElement('p');
    messageText.id = 'popup-text';
    messageText.style.marginBottom = '20px';

    // Create next button
    const nextButton = document.createElement('button');
    nextButton.textContent = 'Next';
    nextButton.style.padding = '10px 20px';
    nextButton.style.backgroundColor = '#007bff';
    nextButton.style.color = '#fff';
    nextButton.style.border = 'none';
    nextButton.style.borderRadius = '5px';
    nextButton.style.cursor = 'pointer';

    // Create close button
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.style.padding = '10px 20px';
    closeButton.style.backgroundColor = '#6c757d';
    closeButton.style.color = '#fff';
    closeButton.style.border = 'none';
    closeButton.style.borderRadius = '5px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.marginLeft = '10px';

    closeButton.addEventListener('click', function () {
        overlay.style.display = 'none';
    });

    popup.appendChild(messageText);
    popup.appendChild(nextButton);
    popup.appendChild(closeButton);
    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Function to show popup with message and optional callback for next
    function showPopup(message, onNext) {
        messageText.textContent = message;
        overlay.style.display = 'flex';

        nextButton.style.display = onNext ? 'inline-block' : 'none';

        if (onNext) {
            nextButton.onclick = function () {
                onNext();
            };
        }
    }

    // Add to Cart popup
    const addToCartForm = document.getElementById('add-to-cart-form');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const quantityInput = document.getElementById('quantity-input');
            const quantity = quantityInput ? quantityInput.value : 1;
            showPopup(`Added ${quantity} item(s) to cart.`);
            // Optionally, submit the form after showing popup
            setTimeout(() => {
                addToCartForm.submit();
            }, 1500);
        });
    }

    // Checkout popup sequence
    const checkoutBtn = document.querySelector('.checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function (e) {
            e.preventDefault();
            let step = 0;
            const messages = [
                'Please review your cart items before proceeding.',
                'Select your delivery method and payment option.',
                'Confirm your billing and shipping information.'
            ];

            function nextStep() {
                step++;
                if (step < messages.length) {
                    showPopup(messages[step], nextStep);
                } else {
                    overlay.style.display = 'none';
                    // Redirect to checkout page or complete order
                    window.location.href = '/checkout/'; // Adjust URL as needed
                }
            }

            showPopup(messages[step], nextStep);
        });
    }
});
