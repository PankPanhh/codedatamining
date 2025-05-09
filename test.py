from flask import Flask, request, jsonify
import numpy as np
from itertools import combinations
from flask_cors import CORS
import sys
import io

# Set stdout encoding to UTF-8 to handle Vietnamese characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
# Configure CORS to allow requests from Live Server
CORS(app, resources={r"/recommend": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

# Transaction data
transactions = [
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

# Product details
product_details = {
    "Hoa Hồng": {"price": 229000, "image": "/image/hoa hong.jpg"},
    "Hoa Cẩm Chướng": {"price": 269000, "image": "/image/hoa cam chuong.jpg"},
    "Hoa Sinh Nhật Dạng Hộp Giấy": {"price": 545000, "image": "/image/hoa sinh nhat dang hop giay.jpg"},
    "Hoa Cưới Cầm Tay Dáng Tròn": {"price": 450000, "image": "/image/hoa cuoi dang tron.jpg"},
    "Hoa Đồng Tiền": {"price": 479000, "image": "/image/hoa dong tien.jpg"},
    "Hoa Khai Trương Hồng Phát": {"price": 800000, "image": "/image/hoa khai truong hong phat.jpg"},
    "Hoa Tulip": {"price": 1000000, "image": "/image/hoa tulip.jpg"}
}

# List of unique items
items = sorted(set(item for transaction in transactions for item in transaction))
item_to_index = {item: idx for idx, item in enumerate(items)}

# Create bit table
bit_table = np.zeros((len(transactions), len(items)), dtype=int)
for i, transaction in enumerate(transactions):
    for item in transaction:
        bit_table[i, item_to_index[item]] = 1

# Find frequent itemsets using bitTableFI
def find_frequent_itemsets(bit_table, items, min_support):
    try:
        num_transactions = bit_table.shape[0]
        min_support_count = min_support * num_transactions
        print(f"Min support count: {min_support_count}")
        frequent_itemsets = []
        
        item_counts = np.sum(bit_table, axis=0)
        print(f"Item counts: {dict(zip(items, item_counts))}")
        frequent_items = [(item,) for i, item in enumerate(items) if item_counts[i] >= min_support_count]
        frequent_itemsets.extend(frequent_items)
        print(f"Frequent 1-itemsets: {frequent_items}")
        
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
            print(f"Frequent {k}-itemsets: {frequent_k}")
            k += 1
        
        print(f"All frequent itemsets: {frequent_itemsets}")
        return frequent_itemsets
    except Exception as e:
        print(f"Error in find_frequent_itemsets: {str(e)}")
        return []

# Generate association rules
def generate_association_rules(frequent_itemsets, min_confidence):
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
                        print(f"Rule: {antecedent} -> {consequent}, Confidence: {confidence}")
                        if confidence >= min_confidence:
                            rules.append((antecedent, consequent, confidence))
        print(f"Generated rules: {rules}")
        return rules
    except Exception as e:
        print(f"Error in generate_association_rules: {str(e)}")
        return []

# API endpoint to get recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        item = request.args.get('item')
        print(f"Received request for item: {item}")
        if not item or item not in product_details:
            print(f"Item {item} not found in product_details")
            return jsonify([])

        min_support = 0.1
        min_confidence = 0.2
        frequent_itemsets = find_frequent_itemsets(bit_table, items, min_support)
        rules = generate_association_rules(frequent_itemsets, min_confidence)

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
        
        print(f"Recommendations for {item}: {recommendations}")
        return jsonify(list({v['name']: v for v in recommendations}.values()))
    except Exception as e:
        print(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)