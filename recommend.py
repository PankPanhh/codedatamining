from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from itertools import combinations
import sys
import io

# Set stdout encoding to UTF-8 to handle Vietnamese characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)  # Allow all origins for development

# Transaction data for recommendation
transactions_1 = [
    ["Hoa Hồng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
    ["Hoa Hồng", "Hoa Cẩm Chướng"],
    ["Hoa Cẩm Chướng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
    ["Hoa Hồng", "Hoa Cưới Cầm Tay Dáng Tròn"],
    ["Hoa Sinh Nhật Dạng Hộp Giấy", "Hoa Cẩm Chướng", "Hoa Đồng Tiền"],
    ["Hoa Cưới Cầm Tay Dáng Tròn", "Hoa Khai Trương Hồng Phát"],
    ["Hoa Hồng", "Hoa Đồng Tiền"],
    ["Hoa Cẩm Chướng", "Hoa Khai Trương Hồng Phát"],
    ["Hoa Hồng", "Hoa Cẩm Chướng", "Hoa Đồng Tiền"],
    ["Hoa Hồng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
    ["Hoa Hồng", "Hoa Cưới Cầm Tay Dáng Tròn"],
    ["Hoa Tulip", "Hoa Ly"],
    ["Hoa Tulip", "Hoa Cưới Buộc Lơi Tự Nhiên"],
    ["Hoa Tulip", "Hoa Khai Trương Nhiệt Huyết"],
    ["Hoa Tulip", "Hoa Cưới Cầm Tay Dáng Dài"],
    ["Hoa Tulip", "Hoa Cẩm Chướng"],
    ["Hoa Tulip", "Hoa Cẩm Chướng", "Hoa Cưới Buộc Lơi Tự Nhiên"],
    ["Hoa Tulip", "Hoa Cẩm Chướng", "Hoa Ly"],
    ["Hoa Tulip", "Hoa Cưới Cầm Tay Dáng Tròn"],
]

# Transaction data for combos
transactions_2 = [
    ['Hoa Hồng', 'Hoa Tulip'],
    ['Hoa Cẩm Chướng', 'Hoa Sinh Nhật Dạng Hộp Giấy'],
    ['Hoa Cưới Cầm Tay Dáng Tròn', 'Hoa Khai Trương Hồng Phát'],
    ['Hoa Hồng', 'Hoa Cẩm Chướng'],
    ['Hoa Tulip', 'Hoa Sinh Nhật Dạng Hộp Giấy'],
    ['Hoa Hồng', 'Hoa Tulip', 'Hoa Cẩm Chướng'],
    ['Hoa Cưới Cầm Tay Dáng Tròn', 'Hoa Khai Trương Nhiệt Huyết'],
    ['Hoa Sinh Nhật Dạng Hộp Giấy', 'Hoa Cẩm Chướng'],
    ['Hoa Hồng', 'Hoa Tulip'],
    ['Hoa Cưới Cầm Tay Dáng Tròn', 'Hoa Khai Trương Hồng Phát']
]

# Product details
product_details = {
    "Hoa Hồng": {"price": 229000, "image": "/image/hoa hong.jpg"},
    "Hoa Cẩm Chướng": {"price": 269000, "image": "/image/hoa cam chuong.jpg"},
    "Hoa Sinh Nhật Dạng Hộp Giấy": {"price": 545000, "image": "/image/hoa sinh nhat dang hop giay.jpg"},
    "Hoa Cưới Cầm Tay Dáng Tròn": {"price": 450000, "image": "/image/hoa cuoi dang tron.jpg"},
    "Hoa Đồng Tiền": {"price": 479000, "image": "/image/hoa dong tien.jpg"},
    "Hoa Khai Trương Hồng Phát": {"price": 800000, "image": "/image/hoa khai truong hong phat.jpg"},
    "Hoa Tulip": {"price": 1000000, "image": "/image/hoa tulip.jpg"},
    "Hoa Lan": {"price": 250000, "image": "/image/hoa lan.jpg"},
    "Hoa Ly": {"price": 350000, "image": "/image/hoa ly.jpg"},
    "Hoa Cẩm Tú Cầu": {"price": 950000, "image": "/image/hoa cam tu cau.jpg"},
    "Hoa Baby Trắng": {"price": 500000, "image": "/image/hoa baby trang.jpg"},
    "Hoa Khai Trương Nhiệt Huyết": {"price": 850000, "image": "/image/hoa khai truong nhiet huyet.jpg"},
    "Hoa Khai Trương Cát Tường": {"price": 800000, "image": "/image/hoa khai truong cat tuong.jpg"},
    "Hoa Cưới Cầm Tay Dáng Dài": {"price": 549000, "image": "/image/hoa cuoi dang dai.jpg"},
    "Hoa Cưới Cầm Tay Dáng Thác Nước": {"price": 799000, "image": "/image/hoa cuoi thac do.jpg"},
    "Hoa Cưới Buộc Lơi Tự Nhiên": {"price": 450000, "image": "/image/hoa cuoi buoc loi.png"},
    "Hoa Sinh Nhật Dạng Bó": {"price": 510000, "image": "/image/hoa sinh nhat dang bo.jpg"},
    "Hoa Sinh Nhật Dạng Hộp Mica": {"price": 1200000, "image": "/image/vali gio hoa sn dang hop.jpg"},
    "Hoa Sinh Nhật Dạng Túi Mica": {"price": 999000, "image": "/image/vali gio hoa sn dang tui deo.jpg"}
}

# Prepare data for recommendation (bitTableFI)
items_1 = sorted(set(item for transaction in transactions_1 for item in transaction))
item_to_index_1 = {item: idx for idx, item in enumerate(items_1)}
bit_table_1 = np.zeros((len(transactions_1), len(items_1)), dtype=int)
for i, transaction in enumerate(transactions_1):
    for item in transaction:
        bit_table_1[i, item_to_index_1[item]] = 1

# Prepare data for combos (bitTableFI)
items_2 = sorted(set(item for transaction in transactions_2 for item in transaction))
item_to_index_2 = {item: idx for idx, item in enumerate(items_2)}
bit_table_2 = np.zeros((len(transactions_2), len(items_2)), dtype=int)
for i, transaction in enumerate(transactions_2):
    for item in transaction:
        bit_table_2[i, item_to_index_2[item]] = 1

# Find frequent itemsets using bitTableFI
def find_frequent_itemsets(bit_table, items, min_support):
    try:
        num_transactions = bit_table.shape[0]
        min_support_count = min_support * num_transactions
        frequent_itemsets = []
        
        item_counts = np.sum(bit_table, axis=0)
        frequent_items = [(item,) for i, item in enumerate(items) if item_counts[i] >= min_support_count]
        frequent_itemsets.extend(frequent_items)
        
        k = 2
        while True:
            candidates = list(combinations(range(len(items)), k))
            frequent_k = []
            for candidate in candidates:
                bit_vector = bit_table[:, candidate[0]]
                for idx in candidate[1:]:
                    bit_vector = bit_vector & bit_table[:, idx]
                support_count = np.sum(bit_vector)
                if support_count >= min_support_count:
                    frequent_k.append(tuple(items[i] for i in candidate))
            if not frequent_k:
                break
            frequent_itemsets.extend(frequent_k)
            k += 1
        
        return frequent_itemsets
    except Exception as e:
        print(f"Error in find_frequent_itemsets: {str(e)}")
        return []

# Generate association rules
def generate_association_rules(frequent_itemsets, min_confidence, bit_table, items, transactions):
    try:
        rules = []
        for itemset in frequent_itemsets:
            if len(itemset) < 2:
                continue
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = set(antecedent)
                    consequent = set(itemset) - antecedent
                    antecedent_bit = np.ones(len(transactions), dtype=int)
                    for item in antecedent:
                        antecedent_bit = antecedent_bit & bit_table[:, item_to_index_2[item] if bit_table is bit_table_2 else item_to_index_1[item]]
                    itemset_bit = np.ones(len(transactions), dtype=int)
                    for item in itemset:
                        itemset_bit = itemset_bit & bit_table[:, item_to_index_2[item] if bit_table is bit_table_2 else item_to_index_1[item]]
                    support_antecedent = np.sum(antecedent_bit)
                    support_itemset = np.sum(itemset_bit)
                    if support_antecedent > 0:
                        confidence = support_itemset / support_antecedent
                        if confidence >= min_confidence:
                            rules.append((antecedent, consequent, confidence))
        return rules
    except Exception as e:
        print(f"Error in generate_association_rules: {str(e)}")
        return []

# API endpoint to get recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        item = request.args.get('item')
        if not item or item not in product_details:
            return jsonify([])
        min_support = 0.1
        min_confidence = 0.2
        frequent_itemsets = find_frequent_itemsets(bit_table_1, items_1, min_support)
        rules = generate_association_rules(frequent_itemsets, min_confidence, bit_table_1, items_1, transactions_1)
        recommendations = []
        for antecedent, consequent, confidence in rules:
            if item in antecedent:
                for rec_item in consequent:
                    if rec_item in product_details:
                        recommendations.append({
                            "name": rec_item,
                            "price": product_details[rec_item]["price"],
                            "image": product_details[rec_item]["image"]
                        })
        return jsonify(list({v['name']: v for v in recommendations}.values()))
    except Exception as e:
        print(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# API endpoint to get promotional combos using bitTableFI
@app.route('/combos', methods=['GET'])
def get_combos():
    try:
        min_support = 0.2
        min_confidence = 0.2
        frequent_itemsets = find_frequent_itemsets(bit_table_2, items_2, min_support)
        combos = []
        for itemset in frequent_itemsets:
            if len(itemset) > 1:
                items = list(itemset)
                total_price = sum(product_details[item]["price"] for item in items)
                discounted_price = total_price * 0.9
                bit_vector = bit_table_2[:, item_to_index_2[items[0]]]
                for item in items[1:]:
                    bit_vector = bit_vector & bit_table_2[:, item_to_index_2[item]]
                support = np.sum(bit_vector) / len(transactions_2)
                # Lấy danh sách hình ảnh (tối đa 2 ảnh)
                images = [product_details[item]["image"] for item in items[:2]]
                combos.append({
                    'items': items,
                    'original_price': total_price,
                    'discounted_price': discounted_price,
                    'support': support,
                    'images': images
                })
        return jsonify(combos)
    except Exception as e:
        print(f"Error in combos endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)