document.addEventListener('DOMContentLoaded', function() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const recommendationList = document.getElementById('recommendation-list');

    if (!recommendationList) {
        console.error('Recommendation list element not found');
        return;
    }

    if (cart.length === 0 || !cart[0]?.name) {
        recommendationList.innerHTML = '<p class="text-center">Vui lòng thêm sản phẩm vào giỏ hàng để nhận gợi ý.</p>';
        return;
    }

    const item = cart[0].name;
    console.log('Fetching recommendations for:', item);

    fetch(`http://localhost:5000/recommend?item=${encodeURIComponent(item)}`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(recommendations => {
            console.log('Recommendations received:', recommendations);
            if (!Array.isArray(recommendations) || recommendations.length === 0) {
                recommendationList.innerHTML = '<p class="text-center">Không có gợi ý nào cho sản phẩm này.</p>';
                return;
            }

            // Limit to only 3 recommendations
            const limitedRecommendations = recommendations.slice(0, 3);

            recommendationList.innerHTML = ''; // Clear previous content
            limitedRecommendations.forEach(item => {
                // Kiểm tra các trường bắt buộc
                if (!item.name || !item.price || !item.image) {
                    console.warn('Invalid recommendation data:', item);
                    return;
                }
                const col = document.createElement('div');
                col.className = 'col';
                col.innerHTML = `
                    <div class="card text-center">
                        <img src="${item.image}" class="card-img-top" alt="${item.name}">
                        <div class="card-body my-0">
                            <h5 class="card-title">${item.name}</h5>
                            <div class="price">
                                <span class="new-price" style="color: red;"><b>${item.price.toLocaleString('vi-VN')} VND</b></span>
                            </div>
                            <div class="btn-group" role="group">
                                <a href="./page/${item.detailPage || item.name.toLowerCase().replace(/\s+/g, '')}.html"><button type="button" class="btn btn-warning">Xem chi tiết</button></a>
                                <a href="./page/giohang.html">
                                    <button type="button" class="btn btn-success" onclick="addToCartAndRedirect('${item.name}', ${item.price})">Mua Ngay</button>
                                </a>
                            </div>
                        </div>
                    </div>
                `;
                recommendationList.appendChild(col);
            });
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error.message);
            recommendationList.innerHTML = '<p class="text-center">Không thể tải gợi ý. Vui lòng thử lại sau.</p>';
        });
});

// Hàm addToCartAndRedirect để xử lý nút "Mua Ngay"
function addToCartAndRedirect(name, price) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const existingItemIndex = cart.findIndex(item => item.name === name);

    if (existingItemIndex !== -1) {
        cart[existingItemIndex].quantity += 1;
    } else {
        cart.push({ name: name, price: price, quantity: 1 });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    window.location.href = './page/giohang.html';
}

// Hàm loadRecommendations để gọi từ giohang.html
function loadRecommendations() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const recommendationList = document.getElementById('recommendation-list');

    if (!recommendationList) {
        console.error('Recommendation list element not found');
        return;
    }

    if (cart.length === 0 || !cart[0]?.name) {
        recommendationList.innerHTML = '<p class="text-center">Vui lòng thêm sản phẩm vào giỏ hàng để nhận gợi ý.</p>';
        return;
    }

    const item = cart[0].name;
    console.log('Fetching recommendations for:', item);

    fetch(`http://localhost:5000/recommend?item=${encodeURIComponent(item)}`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(recommendations => {
            console.log('Recommendations received:', recommendations);
            if (!Array.isArray(recommendations) || recommendations.length === 0) {
                recommendationList.innerHTML = '<p class="text-center">Không có gợi ý nào cho sản phẩm này.</p>';
                return;
            }

            // Limit to only 3 recommendations
            const limitedRecommendations = recommendations.slice(0, 3);

            recommendationList.innerHTML = ''; // Clear previous content
            limitedRecommendations.forEach(item => {
                // Kiểm tra các trường bắt buộc
                if (!item.name || !item.price || !item.image) {
                    console.warn('Invalid recommendation data:', item);
                    return;
                }
                const col = document.createElement('div');
                col.className = 'col';
                col.innerHTML = `
                    <div class="card text-center">
                        <img src="${item.image}" class="card-img-top" alt="${item.name}">
                        <div class="card-body my-0">
                            <h5 class="card-title">${item.name}</h5>
                            <div class="price">
                                <span class="new-price" style="color: red;"><b>${item.price.toLocaleString('vi-VN')} VND</b></span>
                            </div>
                            <div class="btn-group" role="group">
                                <a href="./page/${item.detailPage || item.name.toLowerCase().replace(/\s+/g, '')}.html"><button type="button" class="btn btn-warning">Xem chi tiết</button></a>
                                <a href="./page/giohang.html">
                                    <button type="button" class="btn btn-success" onclick="addToCartAndRedirect('${item.name}', ${item.price})">Mua Ngay</button>
                                </a>
                            </div>
                        </div>
                    </div>
                `;
                recommendationList.appendChild(col);
            });
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error.message);
            recommendationList.innerHTML = '<p class="text-center">Không thể tải gợi ý. Vui lòng thử lại sau.</p>';
        });
}