# from flask import Flask, request, jsonify
# import numpy as np
# from itertools import combinations
# from flask_cors import CORS
# import sys
# import io

# # Set stdout encoding to UTF-8 to handle Vietnamese characters
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# app = Flask(__name__)
# # Configure CORS to allow requests from Live Server
# CORS(app, resources={r"/recommend": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

# # Transaction data
# transactions = [
#     ["Hoa Hồng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
#     ["Hoa Hồng", "Hoa Cẩm Chướng"],
#     ["Hoa Cẩm Chướng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
#     ["Hoa Hồng", "Hoa Cưới Cầm Tay Dáng Tròn"],
#     ["Hoa Sinh Nhật Dạng Hộp Giấy", "Hoa Cẩm Chướng", "Hoa Đồng Tiền"],
#     ["Hoa Cưới Cầm Tay Dáng Tròn", "Hoa Khai Trương Hồng Phát"],
#     ["Hoa Hồng", "Hoa Đồng Tiền"],
#     ["Hoa Cẩm Chướng", "Hoa Khai Trương Hồng Phát"],
#     ["Hoa Hồng", "Hoa Cẩm Chướng", "Hoa Đồng Tiền"],
#     ["Hoa Hồng", "Hoa Sinh Nhật Dạng Hộp Giấy"],
#     ["Hoa Hồng", "Hoa Cưới Cầm Tay Dáng Tròn"],
    
#     ["Hoa Tulip", "Hoa Ly"],
#     ["Hoa Tulip", "Hoa Cưới Buộc Lơi Tự Nhiên"],
#     ["Hoa Tulip", "Hoa Khai Trương Nhiệt Huyết"],
#     ["Hoa Tulip", "Hoa Cưới Cầm Tay Dáng Dài"],
#     ["Hoa Tulip", "Hoa Cẩm Chướng"],
#     ["Hoa Tulip", "Hoa Cẩm Chướng", "Hoa Cưới Buộc Lơi Tự Nhiên"],
#     ["Hoa Tulip", "Hoa Cẩm Chướng", "Hoa Ly"],
#     ["Hoa Tulip", "Hoa Cưới Cầm Tay Dáng Tròn"],
    

# ]

# # Product details
# product_details = {
#    "Hoa Hồng": {"price": 229000, "image": "/image/hoa hong.jpg"},
#     "Hoa Cẩm Chướng": {"price": 269000, "image": "/image/hoa cam chuong.jpg"},
#     "Hoa Sinh Nhật Dạng Hộp Giấy": {"price": 545000, "image": "/image/hoa sinh nhat dang hop giay.jpg"},
#     "Hoa Cưới Cầm Tay Dáng Tròn": {"price": 450000, "image": "/image/hoa cuoi dang tron.jpg"},
#     "Hoa Đồng Tiền": {"price": 479000, "image": "/image/hoa dong tien.jpg"},
#     "Hoa Khai Trương Hồng Phát": {"price": 800000, "image": "/image/hoa khai truong hong phat.jpg"},
#     "Hoa Tulip": {"price": 1000000, "image": "/image/hoa tulip.jpg"},
#     "Hoa Lan": {"price": 250000, "image": "/image/hoa lan.jpg"},
#     "Hoa Ly": {"price": 350000, "image": "/image/hoa ly.jpg"},
#     "Hoa Cẩm Tú Cầu": {"price": 950000, "image": "/image/hoa cam tu cau.jpg"},
#     "Hoa Baby Trắng": {"price": 500000, "image": "/image/hoa baby trang.jpg"},
#     "Hoa Khai Trương Nhiệt Huyết": {"price": 850000, "image": "/image/hoa khai truong nhiet huyet.jpg"},
#     "Hoa Khai Trương Cát Tường": {"price": 800000, "image": "/image/hoa khai truong cat tuong.jpg"},
#     "Hoa Cưới Cầm Tay Dáng Dài": {"price": 549000, "image": "/image/hoa cuoi dang dai.jpg"},
#     "Hoa Cưới Cầm Tay Dáng Thác Nước": {"price": 799000, "image": "/image/hoa cuoi thac do.jpg"},
#     "Hoa Cưới Buộc Lơi Tự Nhiên": {"price": 450000, "image": "/image/hoa cuoi buoc loi.png"},
#     "Hoa Sinh Nhật Dạng Bó": {"price": 510000, "image": "/image/hoa sinh nhat dang bo.jpg"},
#     "Hoa Sinh Nhật Dạng Hộp Mica": {"price": 1200000, "image": "/image/vali gio hoa sn dang hop.jpg"},
#     "Hoa Sinh Nhật Dạng Túi Mica": {"price": 999000, "image": "/image/vali gio hoa sn dang tui deo.jpg"}
# }

# # List of unique items
# items = sorted(set(item for transaction in transactions for item in transaction))
# item_to_index = {item: idx for idx, item in enumerate(items)}

# # Create bit table
# bit_table = np.zeros((len(transactions), len(items)), dtype=int)
# for i, transaction in enumerate(transactions):
#     for item in transaction:
#         bit_table[i, item_to_index[item]] = 1

# # Find frequent itemsets using bitTableFI
# def find_frequent_itemsets(bit_table, items, min_support):
#     try:
#         num_transactions = bit_table.shape[0]
#         min_support_count = min_support * num_transactions
#         print(f"Min support count: {min_support_count}")
#         frequent_itemsets = []
        
#         item_counts = np.sum(bit_table, axis=0)
#         print(f"Item counts: {dict(zip(items, item_counts))}")
#         frequent_items = [(item,) for i, item in enumerate(items) if item_counts[i] >= min_support_count]
#         frequent_itemsets.extend(frequent_items)
#         print(f"Frequent 1-itemsets: {frequent_items}")
        
#         k = 2
#         while True:
#             candidates = list(combinations(range(len(items)), k))
#             frequent_k = []
#             for candidate in candidates:
#                 bit_vector = bit_table[:, candidate[0]]
#                 for idx in candidate[1:]:
#                     bit_vector = bit_vector & bit_table[:, idx]
#                 support_count = np.sum(bit_vector)
#                 if support_count >= min_support_count:
#                     frequent_k.append(tuple(items[i] for i in candidate))
#             if not frequent_k:
#                 break
#             frequent_itemsets.extend(frequent_k)
#             print(f"Frequent {k}-itemsets: {frequent_k}")
#             k += 1
        
#         print(f"All frequent itemsets: {frequent_itemsets}")
#         return frequent_itemsets
#     except Exception as e:
#         print(f"Error in find_frequent_itemsets: {str(e)}")
#         return []

# # Generate association rules
# def generate_association_rules(frequent_itemsets, min_confidence):
#     try:
#         rules = []
#         for itemset in frequent_itemsets:
#             if len(itemset) < 2:
#                 continue
#             for i in range(1, len(itemset)):
#                 for antecedent in combinations(itemset, i):
#                     antecedent = set(antecedent)
#                     consequent = set(itemset) - antecedent
#                     antecedent_bit = np.ones(len(transactions), dtype=int)
#                     for item in antecedent:
#                         antecedent_bit = antecedent_bit & bit_table[:, item_to_index[item]]
#                     itemset_bit = np.ones(len(transactions), dtype=int)
#                     for item in itemset:
#                         itemset_bit = itemset_bit & bit_table[:, item_to_index[item]]
#                     support_antecedent = np.sum(antecedent_bit)
#                     support_itemset = np.sum(itemset_bit)
#                     if support_antecedent > 0:
#                         confidence = support_itemset / support_antecedent
#                         print(f"Rule: {antecedent} -> {consequent}, Confidence: {confidence}")
#                         if confidence >= min_confidence:
#                             rules.append((antecedent, consequent, confidence))
#         print(f"Generated rules: {rules}")
#         return rules
#     except Exception as e:
#         print(f"Error in generate_association_rules: {str(e)}")
#         return []

# # API endpoint to get recommendations
# @app.route('/recommend', methods=['GET'])
# def recommend():
#     try:
#         item = request.args.get('item')
#         print(f"Received request for item: {item}")
#         if not item or item not in product_details:
#             print(f"Item {item} not found in product_details")
#             return jsonify([])

#         min_support = 0.1
#         min_confidence = 0.2
#         frequent_itemsets = find_frequent_itemsets(bit_table, items, min_support)
#         rules = generate_association_rules(frequent_itemsets, min_confidence)

#         recommendations = []
#         for antecedent, consequent, confidence in rules:
#             if item in antecedent:
#                 for rec_item in consequent:
#                     if rec_item in product_details:
#                         recommendations.append({
#                             "name": rec_item,
#                             "price": product_details[rec_item]["price"],
#                             "image": product_details[rec_item]["image"]
#                         })
        
#         print(f"Recommendations for {item}: {recommendations}")
#         return jsonify(list({v['name']: v for v in recommendations}.values()))
#     except Exception as e:
#         print(f"Error in recommend endpoint: {str(e)}")
#         return jsonify({"error": "Internal server error"}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from itertools import combinations
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
import json
import sys
import io
import uuid

# Set stdout encoding to UTF-8 to handle Vietnamese characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
# Configure CORS to allow requests from Live Server
CORS(app, resources={r"/recommend": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

# Transaction data for recommendation (from first original file)
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

# Transaction data for combos (from second original file)
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
                    antecedent_bit = np.ones(len(transactions_1), dtype=int)
                    for item in antecedent:
                        antecedent_bit = antecedent_bit & bit_table_1[:, item_to_index_1[item]]
                    itemset_bit = np.ones(len(transactions_1), dtype=int)
                    for item in itemset:
                        itemset_bit = itemset_bit & bit_table_1[:, item_to_index_1[item]]
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
        
        return jsonify(list({v['name']: v for v in recommendations}.values()))
    except Exception as e:
        print(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Generate promotional combos using Apriori
def generate_promotional_combos():
    try:
        te = TransactionEncoder()
        te_ary = te.fit(transactions_2).transform(transactions_2)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)

        combos = []
        for _, row in frequent_itemsets.iterrows():
            if len(row['itemsets']) > 1:
                items = list(row['itemsets'])
                total_price = sum(product_details[item]["price"] for item in items)
                discounted_price = total_price * 0.9
                combos.append({
                    'items': items,
                    'original_price': total_price,
                    'discounted_price': discounted_price,
                    'support': row['support']
                })

        with open('combos.json', 'w', encoding='utf-8') as f:
            json.dump(combos, f, ensure_ascii=False, indent=4)
        
        return combos
    except Exception as e:
        print(f"Error in generate_promotional_combos: {str(e)}")
        return []

# API endpoint to get promotional combos
@app.route('/combos', methods=['GET'])
def get_combos():
    try:
        combos = generate_promotional_combos()
        return jsonify(combos)
    except Exception as e:
        print(f"Error in combos endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Generate combos when starting the server
    generate_promotional_combos()
    app.run(debug=True, port=5000)