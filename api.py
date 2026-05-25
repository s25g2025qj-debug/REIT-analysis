import csv
from collections import Counter
import requests

url = "https://fudosandb.jp/v1/reit/properties"

params = {"area": "福岡市", "limit": 10000}

headers = {"X-API-Key": "fdb_7f0ec13..."}

res = requests.get(url, headers=headers, params=params)
data = res.json()

results = []
# 区ごとの物件数を数えるためのカウンターを準備
ward_counter = Counter()

for item in data["data"]["properties"]:
    location = item.get("location", "")
    reit_name = item.get("reit_name", "")
    asset_type = item.get("asset_category", "")
    cap_rate = item.get("cap_rate_pct", "")
    occupancy = item.get("occupancy_pct")

    results.append([reit_name, location, asset_type, cap_rate, occupancy])

    # 【追加】locationから「区」までを切り出してカウントする
    ku_index = location.find("区")
    if ku_index != -1:
        ward = location[: ku_index + 1]
        ward_counter[ward] += 1

# 1. 従来の物件詳細CSVの保存
filename = "fukuoka_reit_properties.csv"
with open(filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["reit_name", "location", "asset_type", "cap_rate_pct", "occupancy"]
    )
    writer.writerows(results)

print(f"{len(results)}件の物件詳細を '{filename}' に保存しました。")


# 2. 【追加】区ごとの総数を新しいCSVに保存
count_filename = "fukuoka_ward_counts.csv"
with open(count_filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ward", "property_count"])  # ヘッダー

    # 物件数が多い区の順番（降順）でCSVに書き込む
    for ward, count in ward_counter.most_common():
        writer.writerow([ward, count])

print(f"区ごとの総数を '{count_filename}' に保存しました。")


# 3. 【追加】コンソール（画面）にも集計結果を表示
print("\n【市・区ごとのREIT物件総数】")
for ward, count in ward_counter.most_common():
    print(f"{ward}: {count}件")

print(f"\n{len(results)}件のデータを取りました。")