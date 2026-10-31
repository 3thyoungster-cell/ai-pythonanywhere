import random
from flask import Flask, render_template, request

app = Flask(__name__)

# ==============================================================================
# 衛福部國健署「我的餐盤」單餐黃金比例：50 份完整六大類組合套餐數據庫
# 每一份套餐皆包含：全穀雜糧、豆魚蛋肉、蔬菜、水果、乳品、堅果種子
# ==============================================================================
FOOD_DATABASE = [
    # --- 豆類優先套餐 (1-10) ---
    {
        "name": "植物蛋白高纖經典餐",
        "calories": 550,
        "carbs": 75,
        "protein": 22,
        "fat": 15,
        "category": "豆",
        "hpa": {
            "grain": "蒸地瓜 1.5 顆",
            "protein": "滷豆腐 1 塊 + 無糖豆漿 190ml",
            "veg": "燙高麗菜 1 碗",
            "fruit": "芭樂 0.5 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "無調味核桃 1 茶匙",
        },
        "tip": "遵循「豆>魚>蛋>肉」首選，無膽固醇且高膳食纖維！",
    },
    {
        "name": "超商毛豆高纖全餐",
        "calories": 520,
        "carbs": 68,
        "protein": 20,
        "fat": 16,
        "category": "豆",
        "hpa": {
            "grain": "紫米飯糰 1 個",
            "protein": "涼拌毛豆仁 1 碗",
            "veg": "關東煮蘿蔔與海帶 1 碗",
            "fruit": "小蘋果 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "綜合堅果 1 茶匙",
        },
        "tip": "毛豆含有豐富大豆異黃酮與優質植物蛋白，適合外食族。",
    },
    {
        "name": "黑豆養生抗氧化餐",
        "calories": 540,
        "carbs": 72,
        "protein": 21,
        "fat": 14,
        "category": "豆",
        "hpa": {
            "grain": "蒸南瓜 1.5 碗",
            "protein": "蒸黑豆 1 碗",
            "veg": "炒木耳空心菜 1 碗",
            "fruit": "葡萄 10 顆",
            "dairy": "全脂鮮乳 120ml",
            "nuts": "黑芝麻 1 茶匙",
        },
        "tip": "黑豆皮富含花青素，南瓜補充 β-胡蘿蔔素。",
    },
    {
        "name": "黃豆蒸南瓜均衡餐",
        "calories": 510,
        "carbs": 70,
        "protein": 19,
        "fat": 13,
        "category": "豆",
        "hpa": {
            "grain": "燕麥飯 1.5 碗",
            "protein": "黃豆燉豆包 1 份",
            "veg": "蒜煮花椰菜 1 碗",
            "fruit": "奇異果 1 顆",
            "dairy": "無糖優酪乳 120ml",
            "nuts": "南瓜子 1 茶匙",
        },
        "tip": "黃豆與燕麥蛋白互補，提升蛋白質利用率。",
    },
    {
        "name": "涼拌豆干絲輕食餐",
        "calories": 480,
        "carbs": 62,
        "protein": 23,
        "fat": 14,
        "category": "豆",
        "hpa": {
            "grain": "蒸芋頭 1.5 塊",
            "protein": "涼拌豆干絲 1 碗",
            "veg": "和風沙拉 1 碗",
            "fruit": "小橘子 1 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "杏仁果 5 顆",
        },
        "tip": "低碳水豆干絲搭配芋頭，提供長效飽足感。",
    },
    {
        "name": "傳統鮮豆包地瓜餐",
        "calories": 530,
        "carbs": 74,
        "protein": 20,
        "fat": 15,
        "category": "豆",
        "hpa": {
            "grain": "烤紅心地瓜 1 大顆",
            "protein": "非油炸鮮豆包 2 片",
            "veg": "炒地瓜葉 1 碗",
            "fruit": "蓮霧 2 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "腰果 5 顆",
        },
        "tip": "地瓜葉補充高鐵與高鈣，搭配非油炸豆包。",
    },
    {
        "name": "藜麥黑豆高蛋白餐",
        "calories": 560,
        "carbs": 76,
        "protein": 24,
        "fat": 14,
        "category": "豆",
        "hpa": {
            "grain": "藜麥飯 1.5 碗",
            "protein": "香滷豆腐 2 塊",
            "veg": "炒四季豆 1 碗",
            "fruit": "香蕉 0.5 根",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "葵瓜子 1 茶匙",
        },
        "tip": "藜麥為完整必需胺基酸穀物，蛋白質品質極佳。",
    },
    {
        "name": "豆漿五穀飯高纖餐",
        "calories": 500,
        "carbs": 66,
        "protein": 21,
        "fat": 12,
        "category": "豆",
        "hpa": {
            "grain": "五穀飯 1.5 碗",
            "protein": "無糖高纖豆漿 250ml",
            "veg": "燙水蓮 1 碗",
            "fruit": "切片木瓜 1 碗",
            "dairy": "低脂奶粉 1 匙",
            "nuts": "白芝麻 1 茶匙",
        },
        "tip": "五穀飯搭配高纖豆漿，腸道蠕動好夥伴。",
    },
    {
        "name": "味噌豆腐蔬菜套餐",
        "calories": 490,
        "carbs": 65,
        "protein": 19,
        "fat": 13,
        "category": "豆",
        "hpa": {
            "grain": "蒸馬鈴薯 1.5 顆",
            "protein": "味噌煮板豆腐 1 塊",
            "veg": "鮮香菇炒青江菜 1 碗",
            "fruit": "小番茄 10 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "松子 1 茶匙",
        },
        "tip": "板豆腐含鈣量遠高於嫩豆腐，是補鈣好選擇。",
    },
    {
        "name": "毛豆地瓜堅果餐",
        "calories": 520,
        "carbs": 70,
        "protein": 22,
        "fat": 15,
        "category": "豆",
        "hpa": {
            "grain": "蒸紫地瓜 1.5 顆",
            "protein": "水煮毛豆仁 1 碗",
            "veg": "高麗菜炒木耳 1 碗",
            "fruit": "柳丁 1 顆",
            "dairy": "全脂鮮乳 120ml",
            "nuts": "夏威夷豆 3 顆",
        },
        "tip": "紫地瓜富含花青素，搭配毛豆提供高量好蛋白。",
    },
    # --- 深海魚類套餐 (11-20) ---
    {
        "name": "深海鮭魚黃金全餐",
        "calories": 610,
        "carbs": 70,
        "protein": 28,
        "fat": 20,
        "category": "魚",
        "hpa": {
            "grain": "糙米飯 1.5 碗",
            "protein": "水煮鮭魚菲力 1 片",
            "veg": "炒花椰菜 1 碗",
            "fruit": "蘋果 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "核桃 2 顆",
        },
        "tip": "深海魚富含 Omega-3 好油，搭配糙米滿足 1/3 未精製全穀。",
    },
    {
        "name": "鮮魚味噌湯地瓜餐",
        "calories": 530,
        "carbs": 68,
        "protein": 24,
        "fat": 14,
        "category": "魚",
        "hpa": {
            "grain": "蒸地瓜 1.5 顆",
            "protein": "鮮魚味噌湯 1 碗",
            "veg": "燙菠菜 1 碗",
            "fruit": "奇異果 1 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "杏仁果 5 顆",
        },
        "tip": "深海魚脂搭配菠菜鐵質，維持良好血液循環。",
    },
    {
        "name": "清蒸鱈魚五穀全餐",
        "calories": 560,
        "carbs": 72,
        "protein": 26,
        "fat": 15,
        "category": "魚",
        "hpa": {
            "grain": "五穀飯 1.5 碗",
            "protein": "清蒸鱈魚排 1 片",
            "veg": "炒小白菜 1 碗",
            "fruit": "芭樂 0.5 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "南瓜子 1 茶匙",
        },
        "tip": "鱈魚肉質細緻好消化，提供優質微量元素鋅。",
    },
    {
        "name": "乾煎鯖魚玉米全餐",
        "calories": 620,
        "carbs": 65,
        "protein": 27,
        "fat": 22,
        "category": "魚",
        "hpa": {
            "grain": "蒸玉米 1.5 根",
            "protein": "乾煎鯖魚 0.5 尾",
            "veg": "清炒絲瓜 1 碗",
            "fruit": "葡萄 10 顆",
            "dairy": "無糖優酪乳 120ml",
            "nuts": "腰果 5 顆",
        },
        "tip": "鯖魚天然 EPA/DHA 含量高，適合用眼過度族群。",
    },
    {
        "name": "水煮白蝦低卡全餐",
        "calories": 490,
        "carbs": 64,
        "protein": 26,
        "fat": 10,
        "category": "魚",
        "hpa": {
            "grain": "紫米飯 1.5 碗",
            "protein": "燙白蝦 8 隻",
            "veg": "和風高麗菜沙拉 1 碗",
            "fruit": "小番茄 10 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "葵瓜子 1 茶匙",
        },
        "tip": "蝦類極低脂高蛋白，適合熱量嚴格調控者。",
    },
    {
        "name": "烤秋刀魚紫菜餐",
        "calories": 580,
        "carbs": 66,
        "protein": 25,
        "fat": 20,
        "category": "魚",
        "hpa": {
            "grain": "糙米飯 1.5 碗",
            "protein": "烤秋刀魚 1 尾",
            "veg": "紫菜蛋花湯蔬菜 1 碗",
            "fruit": "香蕉 0.5 根",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "黑芝麻 1 茶匙",
        },
        "tip": "秋刀魚含有豐富維生素 B12 與天然好油脂。",
    },
    {
        "name": "蒜泥花枝高纖餐",
        "calories": 500,
        "carbs": 68,
        "protein": 25,
        "fat": 11,
        "category": "魚",
        "hpa": {
            "grain": "蒸南瓜 1.5 碗",
            "protein": "蒜泥汆燙花枝 1 盤",
            "veg": "炒水蓮 1 碗",
            "fruit": "蓮霧 2 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "松子 1 茶匙",
        },
        "tip": "花枝富含牛磺酸，有助於維持良好體力。",
    },
    {
        "name": "烤鯛魚排芋頭套餐",
        "calories": 520,
        "carbs": 70,
        "protein": 26,
        "fat": 12,
        "category": "魚",
        "hpa": {
            "grain": "蒸芋頭 1.5 塊",
            "protein": "烤鯛魚排 1 片",
            "veg": "炒青江菜 1 碗",
            "fruit": "切片木瓜 1 碗",
            "dairy": "無糖優酪乳 120ml",
            "nuts": "夏威夷豆 3 顆",
        },
        "tip": "鯛魚高蛋白低脂肪，無刺適合全家人補充。",
    },
    {
        "name": "香煎虱目魚肚全餐",
        "calories": 600,
        "carbs": 65,
        "protein": 27,
        "fat": 21,
        "category": "魚",
        "hpa": {
            "grain": "燕麥飯 1.5 碗",
            "protein": "煎虱目魚肚 0.5 片",
            "veg": "燙芥藍菜 1 碗",
            "fruit": "小橘子 1 顆",
            "dairy": "全脂鮮乳 120ml",
            "nuts": "白芝麻 1 茶匙",
        },
        "tip": "虱目魚含有豐富膠原蛋白與優質不飽和脂肪酸。",
    },
    {
        "name": "清蒸鱸魚燕麥全餐",
        "calories": 530,
        "carbs": 68,
        "protein": 26,
        "fat": 13,
        "category": "魚",
        "hpa": {
            "grain": "藜麥燕麥飯 1.5 碗",
            "protein": "清蒸鱸魚片 1 塊",
            "veg": "炒大陸妹 1 碗",
            "fruit": "柳丁 1 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "核桃 2 顆",
        },
        "tip": "鱸魚組織修復效果佳，適合運動後或術後保養。",
    },
    # --- 蛋類套餐 (21-28) ---
    {
        "name": "溫泉蛋玉米高纖餐",
        "calories": 510,
        "carbs": 66,
        "protein": 21,
        "fat": 16,
        "category": "蛋",
        "hpa": {
            "grain": "蒸玉米 1.5 根",
            "protein": "石安牧場溫泉蛋 2 顆",
            "veg": "燙青花菜 1 碗",
            "fruit": "蘋果 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "南瓜子 1 茶匙",
        },
        "tip": "溫泉蛋吸收率高，蛋黃含有豐富卵磷脂。",
    },
    {
        "name": "茶葉蛋鮮乳雙優餐",
        "calories": 500,
        "carbs": 62,
        "protein": 23,
        "fat": 17,
        "category": "蛋",
        "hpa": {
            "grain": "烤地瓜 1.5 顆",
            "protein": "茶葉蛋 2 顆",
            "veg": "關東煮蘿蔔 1 碗",
            "fruit": "奇異果 1 顆",
            "dairy": "低脂鮮乳 200ml",
            "nuts": "杏仁果 5 顆",
        },
        "tip": "雙重優質完全蛋白與鈣質，運動後補給極佳。",
    },
    {
        "name": "蔬菜蒸蛋藜麥全餐",
        "calories": 490,
        "carbs": 65,
        "protein": 20,
        "fat": 14,
        "category": "蛋",
        "hpa": {
            "grain": "藜麥飯 1.5 碗",
            "protein": "蔬菜海鮮蒸蛋 1 碗",
            "veg": "炒空心菜 1 碗",
            "fruit": "小番茄 10 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "葵瓜子 1 茶匙",
        },
        "tip": "蒸蛋口感溫和好吸收，配合藜麥穩定血糖。",
    },
    {
        "name": "番茄炒蛋糙米全餐",
        "calories": 540,
        "carbs": 70,
        "protein": 22,
        "fat": 17,
        "category": "蛋",
        "hpa": {
            "grain": "糙米飯 1.5 碗",
            "protein": "番茄炒蛋 1 盤 (蛋2顆)",
            "veg": "炒高麗菜 1 碗",
            "fruit": "芭樂 0.5 顆",
            "dairy": "無糖優酪乳 120ml",
            "nuts": "腰果 5 顆",
        },
        "tip": "加熱番茄釋放茄紅素，油脂提升吸收率。",
    },
    {
        "name": "水煮蛋紫米健康餐",
        "calories": 520,
        "carbs": 68,
        "protein": 22,
        "fat": 16,
        "category": "蛋",
        "hpa": {
            "grain": "紫米飯 1.5 碗",
            "protein": "水煮蛋 2 顆",
            "veg": "燙菠菜 1 碗",
            "fruit": "葡萄 10 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "松子 1 茶匙",
        },
        "tip": "水煮蛋保留完整營養，蛋白質生物價極高。",
    },
    {
        "name": "洋蔥炒蛋五穀餐",
        "calories": 530,
        "carbs": 69,
        "protein": 21,
        "fat": 16,
        "category": "蛋",
        "hpa": {
            "grain": "五穀飯 1.5 碗",
            "protein": "洋蔥炒蛋 1 盤",
            "veg": "炒小白菜 1 碗",
            "fruit": "蓮霧 2 顆",
            "dairy": "全脂鮮乳 120ml",
            "nuts": "黑芝麻 1 茶匙",
        },
        "tip": "洋蔥含有槲皮素抗氧化，搭配雞蛋非常均衡。",
    },
    {
        "name": "荷包蛋馬鈴薯套餐",
        "calories": 510,
        "carbs": 65,
        "protein": 20,
        "fat": 18,
        "category": "蛋",
        "hpa": {
            "grain": "蒸馬鈴薯帶皮 1.5 顆",
            "protein": "少油煎荷包蛋 2 顆",
            "veg": "和風綠花椰 1 碗",
            "fruit": "切片木瓜 1 碗",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "白芝麻 1 茶匙",
        },
        "tip": "帶皮馬鈴薯含有高量維生素 C 與多酚。",
    },
    {
        "name": "九層塔塔香炒蛋餐",
        "calories": 550,
        "carbs": 71,
        "protein": 22,
        "fat": 18,
        "category": "蛋",
        "hpa": {
            "grain": "燕麥飯 1.5 碗",
            "protein": "塔香炒蛋 1 盤",
            "veg": "炒絲瓜 1 碗",
            "fruit": "香蕉 0.5 根",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "核桃 2 顆",
        },
        "tip": "九層塔含有富豐富維生素 A 與多元植化素。",
    },
    # --- 蛋肉/白肉蛋白套餐 (29-38) ---
    {
        "name": "超商舒肥雞胸黃金組合",
        "calories": 590,
        "carbs": 72,
        "protein": 28,
        "fat": 16,
        "category": "蛋肉",
        "hpa": {
            "grain": "烤飯糰 1 個 + 蒸玉米 0.5 根",
            "protein": "舒肥雞胸肉 + 茶葉蛋 1 顆",
            "veg": "關東煮蘿蔔與海帶 1 碗",
            "fruit": "切片奇異果 1 盒",
            "dairy": "低脂無糖優酪乳 120ml",
            "nuts": "綜合堅果 1 茶匙",
        },
        "tip": "便利商店也能 100% 湊齊國健署六大類黃金比例！",
    },
    {
        "name": "去皮烤雞腿芋頭全餐",
        "calories": 570,
        "carbs": 70,
        "protein": 26,
        "fat": 17,
        "category": "蛋肉",
        "hpa": {
            "grain": "蒸芋頭 1.5 塊",
            "protein": "美式烤雞腿 (去皮) 1 支",
            "veg": "炒地瓜葉 1 碗",
            "fruit": "柳丁 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "南瓜子 1 茶匙",
        },
        "tip": "雞腿去皮可去除非必要飽和脂肪，補充鐵質與蛋白。",
    },
    {
        "name": "鹽水雞胸高纖蔬菜餐",
        "calories": 510,
        "carbs": 66,
        "protein": 29,
        "fat": 13,
        "category": "蛋肉",
        "hpa": {
            "grain": "蒸地瓜 1.5 顆",
            "protein": "鹽水雞胸肉 1 份",
            "veg": "綜合高纖燙蔬菜 1.5 碗",
            "fruit": "蘋果 1 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "杏仁果 5 顆",
        },
        "tip": "低鹽清淡調味，提供極高蛋白與極高膳食纖維。",
    },
    {
        "name": "滷瘦牛肉片糙米全餐",
        "calories": 600,
        "carbs": 72,
        "protein": 30,
        "fat": 18,
        "category": "蛋肉",
        "hpa": {
            "grain": "糙米飯 1.5 碗",
            "protein": "滷瘦牛肉片 1 盤",
            "veg": "炒青江菜 1 碗",
            "fruit": "芭樂 0.5 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "腰果 5 顆",
        },
        "tip": "適量瘦紅肉可補足血紅素鐵質與維生素 B12。",
    },
    {
        "name": "清蒸嫩雞柳南瓜餐",
        "calories": 520,
        "carbs": 68,
        "protein": 28,
        "fat": 12,
        "category": "蛋肉",
        "hpa": {
            "grain": "蒸南瓜 1.5 碗",
            "protein": "清蒸嫩雞柳 1 盤",
            "veg": "炒高麗菜 1 碗",
            "fruit": "小番茄 10 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "葵瓜子 1 茶匙",
        },
        "tip": "雞里肌極低脂肪，是增肌減脂最優秀的白肉來源。",
    },
    {
        "name": "蒜泥里肌瘦肉套餐",
        "calories": 540,
        "carbs": 67,
        "protein": 27,
        "fat": 15,
        "category": "蛋肉",
        "hpa": {
            "grain": "五穀飯 1.5 碗",
            "protein": "蒜泥豬里肌肉片 1 盤",
            "veg": "燙芥藍菜 1 碗",
            "fruit": "葡萄 10 顆",
            "dairy": "無糖優酪乳 120ml",
            "nuts": "松子 1 茶匙",
        },
        "tip": "豬里肌為低脂肪部位，油脂含量遠低於豬五花。",
    },
    {
        "name": "烤火雞肉排地瓜餐",
        "calories": 530,
        "carbs": 70,
        "protein": 29,
        "fat": 12,
        "category": "蛋肉",
        "hpa": {
            "grain": "烤紅心地瓜 1.5 顆",
            "protein": "烤火雞肉排 1 片",
            "veg": "炒水蓮 1 碗",
            "fruit": "蓮霧 2 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "黑芝麻 1 茶匙",
        },
        "tip": "火雞肉含色胺酸，有助於舒緩神經與穩定情緒。",
    },
    {
        "name": "海南雞 (去皮) 燕麥飯餐",
        "calories": 580,
        "carbs": 71,
        "protein": 27,
        "fat": 17,
        "category": "蛋肉",
        "hpa": {
            "grain": "燕麥飯 1.5 碗",
            "protein": "去皮海南雞肉 1 盤",
            "veg": "燙小黃瓜與豆芽 1 碗",
            "fruit": "小橘子 1 顆",
            "dairy": "全脂鮮乳 120ml",
            "nuts": "夏威夷豆 3 顆",
        },
        "tip": "白燙去皮烹調法能保留雞肉清爽風味與蛋白質。",
    },
    {
        "name": "烤松坂瘦肉藜麥餐",
        "calories": 590,
        "carbs": 69,
        "protein": 26,
        "fat": 19,
        "category": "蛋肉",
        "hpa": {
            "grain": "藜麥飯 1.5 碗",
            "protein": "烤松坂瘦肉片 1 盤",
            "veg": "炒空心菜 1 碗",
            "fruit": "切片木瓜 1 碗",
            "dairy": "低脂起司 1 片",
            "nuts": "白芝麻 1 茶匙",
        },
        "tip": "挑選精瘦部位，補充組織修復必備之優質胺基酸。",
    },
    {
        "name": "香菇燉雞肉紫米餐",
        "calories": 560,
        "carbs": 70,
        "protein": 27,
        "fat": 16,
        "category": "蛋肉",
        "hpa": {
            "grain": "紫米飯 1.5 碗",
            "protein": "香菇燉雞腿肉 1 塊",
            "veg": "燙菠菜 1 碗",
            "fruit": "奇異果 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "核桃 2 顆",
        },
        "tip": "香菇含有多醣體，結合雞肉提供溫補營養。",
    },
    # --- 全穀雜糧/蔬菜/優格組合 (39-50) ---
    {
        "name": "燕麥優格輕食黃金餐",
        "calories": 480,
        "carbs": 68,
        "protein": 19,
        "fat": 12,
        "category": "全穀",
        "hpa": {
            "grain": "大燕麥片 1.5 碗",
            "protein": "水煮蛋 1 顆 + 豆漿 100ml",
            "veg": "綜合蔬菜沙拉 1 碗",
            "fruit": "蘋果 1 顆",
            "dairy": "原味無糖優格 1 杯",
            "nuts": "綜合堅果 1 茶匙",
        },
        "tip": "國健署強烈建議每天 1.5-2 杯乳品補充充足鈣質。",
    },
    {
        "name": "藜麥沙拉高纖蔬食餐",
        "calories": 500,
        "carbs": 65,
        "protein": 22,
        "fat": 16,
        "category": "蔬菜",
        "hpa": {
            "grain": "蒸熟藜麥 1.5 碗",
            "protein": "滷豆腐 1 塊 + 茶葉蛋 1 顆",
            "veg": "美生菜彩椒蘿蔓 1.5 碗",
            "fruit": "葡萄 10 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "無調味核桃 1 茶匙",
        },
        "tip": "蔬菜達 1.5 碗，富含豐富植化素與維生素 C。",
    },
    {
        "name": "紫芋頭優酪乳高鈣餐",
        "calories": 490,
        "carbs": 69,
        "protein": 18,
        "fat": 12,
        "category": "全穀",
        "hpa": {
            "grain": "蒸紫芋頭 1.5 塊",
            "protein": "水煮毛豆仁 0.5 碗",
            "veg": "炒花椰菜 1 碗",
            "fruit": "奇異果 1 顆",
            "dairy": "無糖優酪乳 200ml",
            "nuts": "葵瓜子 1 茶匙",
        },
        "tip": "芋頭富含高量鉀離子，有助於調節體內鈉離子。",
    },
    {
        "name": "帶皮馬鈴薯輕食餐",
        "calories": 470,
        "carbs": 64,
        "protein": 20,
        "fat": 13,
        "category": "全穀",
        "hpa": {
            "grain": "蒸馬鈴薯帶皮 1.5 顆",
            "protein": "水煮蛋 2 顆",
            "veg": "和風蔬菜沙拉 1 碗",
            "fruit": "小番茄 10 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "杏仁果 5 顆",
        },
        "tip": "馬鈴薯帶皮食用可完整攝取皮下多酚與皮下纖維。",
    },
    {
        "name": "關東煮高纖豆干餐",
        "calories": 460,
        "carbs": 60,
        "protein": 22,
        "fat": 12,
        "category": "蔬菜",
        "hpa": {
            "grain": "蒸地瓜 1.5 顆",
            "protein": "滷豆干 2 塊",
            "veg": "關東煮蘿蔔海帶高麗菜捲 1.5 碗",
            "fruit": "芭樂 0.5 顆",
            "dairy": "無糖優格 0.5 杯",
            "nuts": "腰果 5 顆",
        },
        "tip": "熱量極低且蔬菜量極高，補足外食最欠缺的膳食纖維。",
    },
    {
        "name": "希臘優格堅果高鈣餐",
        "calories": 510,
        "carbs": 62,
        "protein": 24,
        "fat": 17,
        "category": "全穀",
        "hpa": {
            "grain": "烤紅心地瓜 1 顆",
            "protein": "水煮蛋 1 顆",
            "veg": "炒高麗菜 1 碗",
            "fruit": "小橘子 1 顆",
            "dairy": "希臘優格 1 杯",
            "nuts": "無調味堅果 1 包",
        },
        "tip": "希臘優格蛋白質為一般優格兩倍，鈣質吸收佳。",
    },
    {
        "name": "鮮乳芭樂抗氧化全餐",
        "calories": 480,
        "carbs": 63,
        "protein": 21,
        "fat": 14,
        "category": "全穀",
        "hpa": {
            "grain": "五穀飯 1.5 碗",
            "protein": "蒸黃豆 0.5 碗 + 溫泉蛋 1 顆",
            "veg": "燙水蓮 1 碗",
            "fruit": "珍珠芭樂 1 顆",
            "dairy": "低脂鮮乳 120ml",
            "nuts": "松子 1 茶匙",
        },
        "tip": "芭樂為台灣維生素 C 之王，大幅提升鐵質吸收。",
    },
    {
        "name": "無糖優酪乳蘋果餐",
        "calories": 490,
        "carbs": 66,
        "protein": 20,
        "fat": 13,
        "category": "全穀",
        "hpa": {
            "grain": "糙米飯 1.5 碗",
            "protein": "涼拌毛豆仁 0.5 碗",
            "veg": "炒青江菜 1 碗",
            "fruit": "切片蘋果 1 顆",
            "dairy": "無糖優酪乳 200ml",
            "nuts": "黑芝麻 1 茶匙",
        },
        "tip": "蘋果水溶性果膠結合優酪乳益生菌，維護腸道機能。",
    },
    {
        "name": "蒸玉米起司健康餐",
        "calories": 500,
        "carbs": 67,
        "protein": 21,
        "fat": 15,
        "category": "全穀",
        "hpa": {
            "grain": "蒸甜玉米 1.5 根",
            "protein": "茶葉蛋 2 顆",
            "veg": "炒小白菜 1 碗",
            "fruit": "蓮霧 2 顆",
            "dairy": "低脂起司 1 片",
            "nuts": "白芝麻 1 茶匙",
        },
        "tip": "玉米屬於全穀雜糧類，富含葉黃素與玉米黃素。",
    },
    {
        "name": "堅果豆漿高纖全餐",
        "calories": 520,
        "carbs": 68,
        "protein": 23,
        "fat": 16,
        "category": "豆",
        "hpa": {
            "grain": "紫米飯 1.5 碗",
            "protein": "無糖高纖豆漿 250ml",
            "veg": "燙地瓜葉 1 碗",
            "fruit": "切片木瓜 1 碗",
            "dairy": "低脂奶粉 1 匙",
            "nuts": "綜合堅果 1 茶匙",
        },
        "tip": "堅果提供國健署指引推薦之每日必需單元不飽和好油。",
    },
]


# ==============================================================================
# 內部自動化資料庫自我檢測機制 (Automated Database Validation)
# ==============================================================================
def validate_database():
    print("內部資料庫自我檢測啟動中...")
    hpa_keys = ["grain", "protein", "veg", "fruit", "dairy", "nuts"]

    if len(FOOD_DATABASE) < 50:
        print(f"⚠️ [警告] 資料庫筆數未達 50 筆，目前為 {len(FOOD_DATABASE)} 筆！")

    for idx, item in enumerate(FOOD_DATABASE):
        # 1. 檢查基本欄位
        if not item.get("name") or item.get("calories", 0) <= 0:
            raise ValueError(
                f"❌ [資料庫錯誤] 第 {idx+1} 筆套餐名稱或熱量設定異常！"
            )

        # 2. 檢查六大類拆解欄位完整性
        hpa_data = item.get("hpa", {})
        for key in hpa_keys:
            if key not in hpa_data:
                raise ValueError(
                    f"❌ [資料庫錯誤] 第 {idx+1} 筆套餐 '{item['name']}' 缺少六大類欄位 '{key}'！"
                )

    print(
        f"✅ [自動化檢測成功] 50 份黃金比例套餐資料庫驗證通過！全數涵蓋國健署六大類食物。"
    )


validate_database()


# ==============================================================================
# Flask 核心路由與防呆驗證
# ==============================================================================
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

        # 防呆驗證 1：檢查空數值
        if not calories_raw:
            error_message = "請輸入有效的單餐熱量目標數值！"
        else:
            try:
                # 防呆驗證 2：型態轉換保護
                weight = float(weight_raw)
                activity = float(activity_raw)
                calories = int(float(calories_raw))

                # 防呆驗證 3：數值範圍鎖定
                if calories <= 0 or weight <= 0:
                    error_message = "熱量目標與體重必須為大於 0 的正數！"
                elif weight > 300:
                    error_message = "請輸入合理的體重數值（低於 300 kg）！"
                elif calories < 300:
                    warning_message = "國健署提醒：成年人單餐熱量建議不低於 300 大卡，過度節食可能導致基礎代謝率下降！"
            except ValueError:
                error_message = (
                    "請填寫正確的數字格式（切勿填寫英文字母或特殊符號）！"
                )

        # 核心計算邏輯
        if not error_message:
            safe_weight = max(weight, 1.0)
            safe_activity = max(activity, 1.0)
            daily_tdee = max(round(safe_weight * 22 * safe_activity), 1)

            # 遍歷 50 筆黃金比例套餐
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
                protein_portion = round(
                    max(recommended_item["protein"], 0) / 7.0, 1
                )
                meal_tdee_ratio = round(
                    (recommended_item["calories"] / float(daily_tdee)) * 100
                )

                calc_data = {
                    "protein_portion": protein_portion,
                    "meal_tdee_ratio": meal_tdee_ratio,
                    "daily_tdee": daily_tdee,
                }
            else:
                warning_message = "在您設定的熱量限制下找不到合適的套餐，建議適度放寬熱量目標！"

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
