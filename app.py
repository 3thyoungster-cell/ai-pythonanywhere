import random
from flask import Flask, render_template, request

app = Flask(__name__)

# 涵蓋國健署六大類食物的外食資料庫 (List 包 Dict)
FOOD_DATABASE = [
    {
        "name": "高纖無糖豆漿 + 烤地瓜",
        "calories": 300,
        "carbs": 40,
        "protein": 18,
        "fat": 5,
        "category": "豆",
        "hpaGroup": "豆類 + 全穀雜糧類",
        "tip": "未精製全穀搭配植物性蛋白，高纖且能穩定血糖",
    },
    {
        "name": "涼拌毛豆仁 + 燕麥奶",
        "calories": 250,
        "carbs": 30,
        "protein": 12,
        "fat": 6,
        "category": "豆",
        "hpaGroup": "豆類 + 全穀雜糧類",
        "tip": "毛豆為植物蛋白首選，含豐富膳食纖維與大豆異黃酮",
    },
    {
        "name": "水煮鮭魚菲力 + 糙米飯",
        "calories": 420,
        "carbs": 45,
        "protein": 28,
        "fat": 12,
        "category": "魚",
        "hpaGroup": "魚類 + 全穀雜糧類",
        "tip": "深海魚富含 Omega-3，搭配糙米滿足每日全穀 1/3 需求",
    },
    {
        "name": "鮮魚味噌湯 + 蒸地瓜",
        "calories": 240,
        "carbs": 32,
        "protein": 15,
        "fat": 4,
        "category": "魚",
        "hpaGroup": "魚類 + 全穀雜糧類",
        "tip": "低脂優質蛋白，提供豐富微量元素與維生素 A",
    },
    {
        "name": "藜麥雞肉沙拉 + 堅果",
        "calories": 380,
        "carbs": 25,
        "protein": 26,
        "fat": 18,
        "category": "蔬菜",
        "hpaGroup": "蔬菜類 + 肉類 + 堅果類",
        "tip": "達每日蔬菜 1 份，堅果提供國健署推薦之每日好油",
    },
    {
        "name": "關東煮蘿蔔與海帶 + 滷豆腐",
        "calories": 180,
        "carbs": 15,
        "protein": 10,
        "fat": 6,
        "category": "蔬菜",
        "hpaGroup": "蔬菜類 + 豆類",
        "tip": "高纖低熱量組合，補足外食族最缺乏的膳食纖維",
    },
    {
        "name": "燕麥片 + 原味無糖優格",
        "calories": 280,
        "carbs": 38,
        "protein": 12,
        "fat": 6,
        "category": "全穀",
        "hpaGroup": "全穀雜糧類 + 乳品類",
        "tip": "國健署強烈建議每日攝取 1.5-2 杯乳品以補足鈣質",
    },
    {
        "name": "蒸玉米 + 石安牧場溫泉蛋",
        "calories": 210,
        "carbs": 26,
        "protein": 10,
        "fat": 7,
        "category": "全穀",
        "hpaGroup": "全穀雜糧類 + 蛋類",
        "tip": "未精製主食補充維生素 B 群，蛋黃富含卵磷脂",
    },
    {
        "name": "即食舒肥雞胸肉 + 烤飯糰",
        "calories": 360,
        "carbs": 42,
        "protein": 25,
        "fat": 5,
        "category": "蛋肉",
        "hpaGroup": "肉類 + 全穀雜糧類",
        "tip": "白肉低脂高蛋白，避開加工紅肉以降低飽和脂肪",
    },
    {
        "name": "茶葉蛋 + 低脂鮮乳",
        "calories": 230,
        "carbs": 12,
        "protein": 15,
        "fat": 10,
        "category": "蛋肉",
        "hpaGroup": "蛋類 + 乳品類",
        "tip": "雙重優質完全蛋白與鈣質，適合運動後快速補充",
    },
]


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error_message = None
    warning_message = None
    recommended_item = None
    calc_data = {}

    if request.method == "POST":
        weight_raw = request.form.get("weight", "60").strip()
        activity_raw = request.form.get("activity", "1.2").strip()
        calories_raw = request.form.get("calories", "").strip()
        category_select = request.form.get("category", "ALL")

        # 防呆驗證
        if not calories_raw:
            error_message = "請輸入有效的單餐熱量上限數值！"
        else:
            try:
                weight = float(weight_raw)
                activity = float(activity_raw)
                calories = int(calories_raw)

                if calories <= 0 or weight <= 0:
                    error_message = "熱量與體重必須為大於 0 的正數！"
                elif calories < 300:
                    warning_message = "國健署提醒：成年人單餐熱量建議不低於 300 大卡，過度節食可能導致基礎代謝率下降！"
            except ValueError:
                error_message = "請填寫有效的數字格式！"

        # 資料處理與篩選
        if not error_message:
            daily_tdee = round(weight * 22 * activity)

            for food in FOOD_DATABASE:
                if food["calories"] <= calories:
                    if category_select == "ALL":
                        results.append(food)
                    elif category_select == "蛋肉" and food["category"] in [
                        "蛋",
                        "肉",
                        "蛋肉",
                    ]:
                        results.append(food)
                    elif food["category"] == category_select:
                        results.append(food)

            if results:
                recommended_item = random.choice(results)
                protein_portion = round(recommended_item["protein"] / 7, 1)
                meal_tdee_ratio = round(
                    (recommended_item["calories"] / daily_tdee) * 100
                )

                calc_data = {
                    "protein_portion": protein_portion,
                    "meal_tdee_ratio": meal_tdee_ratio,
                    "daily_tdee": daily_tdee,
                }
            else:
                warning_message = "在您設定的熱量限制下找不到合適的餐點，建議適度放寬熱量限制！"

    return render_template(
        "index.html",
        results=results,
        error_message=error_message,
        warning_message=warning_message,
        recommended_item=recommended_item,
        calc_data=calc_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
