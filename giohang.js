async function loadCombos() {
    try {
        const response = await fetch('/combos.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        window.combos = await response.json();
    } catch (error) {
        console.error('Error loading combos:', error);
    }
}

function loadCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItems = document.getElementById('cart-items');
    if (!cartItems) return;

    cartItems.innerHTML = '';
    let total = 0;

    cart.forEach((item, index) => {
        const itemName = item.name.replace('Combo: ', '');
        const itemTotal = item.price * item.quantity;
        total += itemTotal;

        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item mb-3 p-3 border rounded';
        itemDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${itemName} x${item.quantity}</span>
                <span>${itemTotal.toLocaleString()} VNĐ</span>
            </div>
            <div class="d-flex justify-content-between align-items-center mt-2">
                <div class="btn-group">
                    <button class="btn btn-sm btn-secondary" onclick="updateQuantity(${index}, -1)">-</button>
                    <span class="mx-2">${item.quantity}</span>
                    <button class="btn btn-sm btn-secondary" onclick="updateQuantity(${index}, 1)">+</button>
                </div>
                <button class="btn btn-danger btn-sm" onclick="removeItem(${index})">Xóa</button>
            </div>
        `;

        // Kiểm tra combo khuyến mãi
        if (!itemName.startsWith('Combo:') && window.combos) {
            for (const combo of window.combos) {
                if (combo.items.includes(itemName)) {
                    const missingItems = combo.items.filter(i => i !== itemName);
                    if (missingItems.length === 1) {
                        const discountPercent = ((combo.original_price - combo.discounted_price) / combo.original_price * 100).toFixed(0);
                        const promoDiv = document.createElement('div');
                        promoDiv.className = 'promo-suggestion mt-2 p-2 border rounded';
                        promoDiv.style.borderColor = '#ff6200';
                        promoDiv.style.backgroundColor = '#fff';
                        promoDiv.innerHTML = `
                            <h6 style="color: #ff6200; font-weight: bold;">Khuyến mãi</h6>
                            <div class="d-flex justify-content-between align-items-center">
                                <span style="font-size: 14px;">
                                    Mua thêm <b>${missingItems[0]}</b> để được giảm <b>${discountPercent}%</b>!
                                </span>
                                <a href="./page/tatcasanpham.html" class="btn btn-sm text-white" style="background-color: #ff6200;">Xem thêm</a>
                            </div>
                        `;
                        itemDiv.appendChild(promoDiv);
                        break;
                    }
                }
            }
        }

        cartItems.appendChild(itemDiv);
    });

    document.getElementById('total-price').textContent = total.toLocaleString() + ' VNĐ';
}

function updateQuantity(index, change) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart[index].quantity + change > 0) {
        cart[index].quantity += change;
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    loadCart();
}

function removeItem(index) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCart();
}

window.onload = async function() {
    await loadCombos();
    loadCart();
};