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

# Transaction data for recommendation and substitute
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

    # ["Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Sinh Nhật Dạng Hộp Giấy", "Hoa Sinh Nhật Dạng Túi Mica"],  # Liên kết với giao dịch mẫu
    # ["Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Sinh Nhật Dạng Túi Mica"],  # Giá gần, cùng danh mục
    # ["Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Tulip"],                  # Giá gần, cùng danh mục
    # ["Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Sinh Nhật Dạng Hộp Giấy", "Hoa Sinh Nhật Dạng Túi Mica"],  # Liên kết với giao dịch mẫu
    # ["Hoa Sinh Nhật Dạng Túi Mica", "Hoa Sinh Nhật Dạng Hộp Mica"],  # Tăng support cho cặp phổ biến
    # ["Hoa Cẩm Tú Cầu", "Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Tulip"]   # Tăng support cho các sản phẩm giá cao
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



# Transaction data for substitute recommendations (expanded for better coverage)
transactions_3 = [
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
    # Additional transactions to improve coverage
    ["Hoa Cưới Cầm Tay Dáng Dài", "Hoa Cưới Cầm Tay Dáng Tròn", "Hoa Cưới Buộc Lơi Tự Nhiên"],
    ["Hoa Cưới Cầm Tay Dáng Dài", "Hoa Cưới Cầm Tay Dạng Thác Nước"],
    ["Hoa Cưới Cầm Tay Dáng Dài", "Hoa Baby Trắng"],
    ["Hoa Khai Trương Cát Tường", "Hoa Khai Trương Hồng Phát", "Hoa Khai Trương Nhiệt Huyết"],
    ["Hoa Khai Trương Cát Tường", "Hoa Cẩm Chướng"],
    ["Hoa Khai Trương Cát Tường", "Hoa Hồng"],
    ["Hoa Sinh Nhật Dạng Bó", "Hoa Sinh Nhật Dạng Hộp Giấy", "Hoa Sinh Nhật Dạng Hộp Mica"],
    ["Hoa Sinh Nhật Dạng Hộp Mica", "Hoa Sinh Nhật Dạng Túi Mica"],
    ["Hoa Lan", "Hoa Ly", "Hoa Cẩm Tú Cầu"],
    ["Hoa Baby Trắng", "Hoa Cưới Cầm Tay Dáng Tròn"],
]


# Product details with availability and category
product_details = {
    "Hoa Hồng": {"price": 229000, "image": "/image/hoa hong.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Cẩm Chướng": {"price": 269000, "image": "/image/hoa cam chuong.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Sinh Nhật Dạng Hộp Giấy": {"price": 545000, "image": "/image/hoa sinh nhat dang hop giay.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Cưới Cầm Tay Dáng Tròn": {"price": 450000, "image": "/image/hoa cuoi dang tron.jpg", "is_available": True, "category": "Hoa Cưới"},
    "Hoa Đồng Tiền": {"price": 479000, "image": "/image/hoa dong tien.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Khai Trương Hồng Phát": {"price": 800000, "image": "/image/hoa khai truong hong phat.jpg", "is_available": True, "category": "Hoa Khai Trương"},
    "Hoa Tulip": {"price": 1000000, "image": "/image/hoa tulip.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Lan": {"price": 250000, "image": "/image/hoa lan.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Ly": {"price": 350000, "image": "/image/hoa ly.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Cẩm Tú Cầu": {"price": 950000, "image": "/image/hoa cam tu cau.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Baby Trắng": {"price": 500000, "image": "/image/hoa baby trang.jpg", "is_available": True, "category": "Hoa Cưới"},
    "Hoa Khai Trương Nhiệt Huyết": {"price": 850000, "image": "/image/hoa khai truong nhiet huyet.jpg", "is_available": True, "category": "Hoa Khai Trương"},
    "Hoa Khai Trương Cát Tường": {"price": 800000, "image": "/image/hoa khai truong cat tuong.jpg", "is_available": False, "category": "Hoa Khai Trương"},
    "Hoa Cưới Cầm Tay Dáng Dài": {"price": 549000, "image": "/image/hoa cuoi dang dai.jpg", "is_available": False, "category": "Hoa Cưới"},
    "Hoa Cưới Cầm Tay Dạng Thác Nước": {"price": 799000, "image": "/image/hoa cuoi thac do.jpg", "is_available": True, "category": "Hoa Cưới"},
    "Hoa Cưới Buộc Lơi Tự Nhiên": {"price": 450000, "image": "/image/hoa cuoi buoc loi.png", "is_available": True, "category": "Hoa Cưới"},
    "Hoa Sinh Nhật Dạng Bó": {"price": 510000, "image": "/image/hoa sinh nhat dang bo.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Sinh Nhật Dạng Hộp Mica": {"price": 1200000, "image": "/image/vali gio hoa sn dang hop.jpg", "is_available": True, "category": "Hoa Sinh Nhật"},
    "Hoa Sinh Nhật Dạng Túi Mica": {"price": 999000, "image": "/image/vali gio hoa sn dang tui deo.jpg", "is_available": True, "category": "Hoa Sinh Nhật"}
}

# Prepare data for recommendation and substitute (bitTableFI)
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

# Prepare data for substitute (bitTableFI)
items_3 = sorted(set(item for transaction in transactions_3 for item in transaction))
item_to_index_3 = {item: idx for idx, item in enumerate(items_3)}
bit_table_3 = np.zeros((len(transactions_3), len(items_3)), dtype=int)
for i, transaction in enumerate(transactions_3):
    for item in transaction:
        bit_table_3[i, item_to_index_3[item]] = 1

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
def generate_association_rules(frequent_itemsets, min_confidence, bit_table, items, transactions, item_to_index):
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
                        antecedent_bit = antecedent_bit & bit_table[:, item_to_index[item]]
                    itemset_bit = np.ones(len(transactions), dtype=int)
                    for item in itemset:
                        itemset_bit = itemset_bit & bit_table[:, item_to_index[item]]
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
        rules = generate_association_rules(frequent_itemsets, min_confidence, bit_table_1, items_1, transactions_1, item_to_index_1)
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
        return jsonify({"error Angled Response": "Internal server error"}, 500)

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


# API endpoint to get substitute products with fallback using BitTableFI
@app.route('/substitute', methods=['GET'])
def substitute():
    try:
        item = request.args.get('item')
        if not item or item not in product_details:
            return jsonify({"error": "Invalid product name"}), 400
        if product_details[item]["is_available"]:
            return jsonify({"error": "Product is available, no substitutes needed"}), 400
        
        min_support = 0.05
        min_confidence = 0.1
        frequent_itemsets = find_frequent_itemsets(bit_table_3, items_3, min_support)
        rules = generate_association_rules(frequent_itemsets, min_confidence, bit_table_3, items_3, transactions_3, item_to_index_3)
        
        substitutes = []
        for antecedent, consequent, confidence in rules:
            if item in antecedent:
                for sub_item in consequent:
                    if sub_item in product_details and product_details[sub_item]["is_available"]:
                        if (product_details[sub_item]["category"] == product_details[item]["category"] or
                            abs(product_details[sub_item]["price"] - product_details[item]["price"]) <= 200000):
                            substitutes.append({
                                "name": sub_item,
                                "price": product_details[sub_item]["price"],
                                "image": product_details[sub_item]["image"],
                                "confidence": confidence
                            })
        
        # Sort by confidence and limit to 3 substitutes
        substitutes = sorted(substitutes, key=lambda x: x["confidence"], reverse=True)[:3]
        if len(substitutes) < 3:  # Ensure at least 3 substitutes
            # Fallback: Generate extended transactions from available products
            available_items = [name for name, details in product_details.items() if details["is_available"]]
            extended_transactions = []
            for name in available_items:
                if product_details[name]["category"] == product_details[item]["category"]:
                    # Create synthetic transactions based on category and price proximity
                    related_items = [other for other in available_items 
                                     if other != name and product_details[other]["category"] == product_details[item]["category"] 
                                     and abs(product_details[other]["price"] - product_details[name]["price"]) <= 200000][:2]
                    if related_items:
                        extended_transactions.append([name] + related_items)
            
            if extended_transactions:
                # Prepare BitTable for extended transactions
                ext_items = sorted(set(item for trans in extended_transactions for item in trans))
                ext_item_to_index = {item: idx for idx, item in enumerate(ext_items)}
                ext_bit_table = np.zeros((len(extended_transactions), len(ext_items)), dtype=int)
                for i, transaction in enumerate(extended_transactions):
                    for item in transaction:
                        ext_bit_table[i, ext_item_to_index[item]] = 1
                
                # Find frequent itemsets and rules with extended data
                ext_frequent_itemsets = find_frequent_itemsets(ext_bit_table, ext_items, min_support)
                ext_rules = generate_association_rules(ext_frequent_itemsets, min_confidence, ext_bit_table, ext_items, extended_transactions, ext_item_to_index)
                
                for antecedent, consequent, confidence in ext_rules:
                    if item in antecedent:
                        for sub_item in consequent:
                            if sub_item in product_details and product_details[sub_item]["is_available"]:
                                if (product_details[sub_item]["category"] == product_details[item]["category"] or
                                    abs(product_details[sub_item]["price"] - product_details[item]["price"]) <= 200000):
                                    substitutes.append({
                                        "name": sub_item,
                                        "price": product_details[sub_item]["price"],
                                        "image": product_details[sub_item]["image"],
                                        "confidence": confidence
                                    })
                # Sort and ensure at least 3 substitutes
                substitutes = sorted(substitutes, key=lambda x: x["confidence"], reverse=True)
                if len(substitutes) < 3:
                    # If still less than 3, pick top available items in the same category
                    additional_subs = [
                        {"name": name, "price": details["price"], "image": details["image"], "confidence": 0.05}
                        for name, details in product_details.items()
                        if details["is_available"] and details["category"] == product_details[item]["category"] and name != item
                    ]
                    additional_subs = sorted(additional_subs, key=lambda x: x["price"])[:3 - len(substitutes)]
                    substitutes.extend(additional_subs)
                substitutes = substitutes[:3]

        return jsonify(list({v['name']: v for v in substitutes}.values()))
    except Exception as e:
        print(f"Error in substitute endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# API endpoint to get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(product_details)

if __name__ == '__main__':
    app.run(debug=True, port=5000)