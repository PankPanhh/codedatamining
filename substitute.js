async function loadSubstitutes(name, button) {
    try {
        const container = document.getElementById(`substitute-${name}`);
        if (!container) {
            console.error(`Container substitute-${name} not found`);
            return;
        }

        container.innerHTML = ''; // Clear previous content
        const response = await fetch(`http://127.0.0.1:5000/substitute?item=${encodeURIComponent(name)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            container.innerHTML = `<p class="text-center text-danger">Lỗi: ${data.error}</p>`;
            return;
        }

        if (data.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">Không tìm thấy sản phẩm thay thế.</p>';
            return;
        }

        const message = document.createElement('div');
        message.className = 'out-of-stock-message text-center text-danger mb-3';
        message.textContent = 'Sản phẩm đã hết hàng, vui lòng chọn sản phẩm thay thế bên dưới';
        container.appendChild(message);

        const cardContainer = document.createElement('div');
        cardContainer.className = 'd-flex flex-wrap justify-content-center gap-3';
        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card substitute-card text-center';
            card.style.maxWidth = '200px'; // Giới hạn chiều rộng thẻ
            card.innerHTML = `
                <img src="${item.image}" class="card-img-top img-fluid rounded" alt="${item.name}" style="height: 150px; object-fit: cover;">
                <div class="card-body">
                    <h6 class="card-title">${item.name}</h6>
                    <p class="card-text">Giá: ${item.price.toLocaleString()} VNĐ</p>
                    <button type="button" class="btn btn-success btn-sm" onclick="addToCartAndRedirect('${item.name}', ${item.price})">Mua Ngay</button>
                </div>
            `;
            cardContainer.appendChild(card);
        });
        container.appendChild(cardContainer);
    } catch (error) {
        console.error('Error fetching substitutes:', error);
        const container = document.getElementById(`substitute-${name}`);
        if (container) {
            container.innerHTML = '<p class="text-center text-danger">Không thể tải sản phẩm thay thế. Vui lòng thử lại sau.</p>';
        }
    }
}