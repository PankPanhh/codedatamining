async function loadCombos() {
    try {
        const response = await fetch('http://localhost:5000/combos');
        const combos = await response.json();
        const combosContainer = document.getElementById('combos');
        combosContainer.innerHTML = '';

        if (combos.length === 0) {
            combosContainer.innerHTML = '<p class="text-center text-gray-500">Không có combo nào.</p>';
            return;
        }

        combos.forEach(combo => {
            const comboCard = document.createElement('div');
            comboCard.className = 'combo-card bg-white p-4 rounded-lg shadow-md flex';
            comboCard.innerHTML = `
                <div class="content flex-1 pr-4">
                    <h3 class="text-lg font-semibold mb-2">Combo: ${combo.items.join(', ')}</h3>
                    <p class="text-gray-600">Giá gốc: ${combo.original_price.toLocaleString()} VNĐ</p>
                    <p class="text-green-600 font-bold">Giá chiết khấu: ${combo.discounted_price.toLocaleString()} VNĐ</p>
                    <p class="text-gray-500">Hỗ trợ: ${(combo.support * 100).toFixed(2)}%</p>
                </div>
                <div class="images flex flex-col gap-2">
                    ${combo.images.map(img => `<img src="${img}" alt="Combo item" class="w-32 h-32 object-cover rounded-md">`).join('')}
                </div>
            `;
            combosContainer.appendChild(comboCard);
        });
    } catch (error) {
        console.error('Lỗi khi lấy combo:', error);
        document.getElementById('combos').innerHTML = 
            '<p class="text-center text-red-500">Lỗi khi tải combo.</p>';
    }
}

window.onload = loadCombos;