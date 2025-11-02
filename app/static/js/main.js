// Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Fetch and display crypto prices
async function fetchCryptoPrices() {
    try {
        const response = await fetch('/api/crypto-prices');
        const data = await response.json();
        if (data.success) {
            console.log('Cryptocurrency Prices:', data.data);
            return data.data;
        }
    } catch (error) {
        console.error('Error fetching crypto prices:', error);
    }
}

// Add to cart functionality
function addToCart(minerId, quantity = 1) {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existingItem = cart.find(item => item.minerId === minerId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ minerId, quantity });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`Added ${quantity} item(s) to cart`);
}

// Get cart from localStorage
function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}

// Clear cart
function clearCart() {
    localStorage.removeItem('cart');
}

// Toggle favorite (needs authentication)
async function toggleFavorite(minerId) {
    try {
        const isFavorited = document.querySelector('.favorite-btn').classList.contains('liked');
        const url = isFavorited ? 
            `/api/miner/${minerId}/remove-from-favorites` : 
            `/api/miner/${minerId}/add-to-favorites`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        if (data.success) {
            document.querySelector('.favorite-btn').classList.toggle('liked');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Export functions for use in templates
window.formatCurrency = formatCurrency;
window.fetchCryptoPrices = fetchCryptoPrices;
window.addToCart = addToCart;
window.getCart = getCart;
window.clearCart = clearCart;
window.toggleFavorite = toggleFavorite;
