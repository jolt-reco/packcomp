from app import create_app, db
from app.models import Purpose, Item, PurposeItem

PURPOSE_DATA = [
    {"name": "観光", "category": "定番"},
    {"name": "温泉", "category": "定番"},
    {"name": "食べ歩き", "category": "定番"},
    {"name": "帰省", "category": "定番"},
    {"name": "写真旅", "category": "定番"},
    {"name": "ドライブ", "category": "定番"},
    {"name": "ペット同伴", "category": "定番"},

    {"name": "海水浴", "category": "レジャー"},
    {"name": "登山", "category": "レジャー"},
    {"name": "キャンプ", "category": "レジャー"},
    {"name": "スキー・スノーボード", "category": "レジャー"},
    {"name": "マリンスポーツ", "category": "レジャー"},
    {"name": "ピクニック", "category": "レジャー"},

    {"name": "フェス・ライブ", "category": "イベント"},
    {"name": "スポーツ観戦", "category": "イベント"},
    {"name": "花火大会", "category": "イベント"},
    {"name": "BBQ", "category": "イベント"},
    {"name": "結婚式参列", "category": "イベント"},
    
    {"name": "サウナ巡り", "category": "趣味・体験"},
    {"name": "絵画スケッチ", "category": "趣味・体験"},
    {"name": "神社仏閣巡り", "category": "趣味・体験"},
    {"name": "ゲーム", "category": "趣味・体験"},

    {"name": "出張", "category": "ビジネス"},
    {"name": "研修・セミナー", "category": "ビジネス"},
    {"name": "学会発表", "category": "ビジネス"},
    {"name": "面接・就活", "category": "ビジネス"},
]

ITEM_DATA = {
    "衣類": [
        {"name": "Tシャツ",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "下着",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "靴下",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "パジャマ",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "部屋着",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "薄手の長袖",       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "薄手の上着",       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ヒートテック（上）", "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ヒートテック（下）", "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "厚手の上着",        "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "手袋",              "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "マフラー",          "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "予備の着替え",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "水着",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ビーチサンダル",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "サンダル",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "登山靴",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "レインジャケット",   "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "スキーウェア",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ネックウォーマー",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "浴衣",             "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "スーツ",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "革靴",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ドレス",             "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "パンプス",             "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "サウナハット",        "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
    ],

    "生活用品": [
        {"name": "歯ブラシ",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "歯磨き粉",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "タオル",              "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ハンカチ",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ティッシュ",           "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ウェットティッシュ",     "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "シャンプー（小分け）",   "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ボディソープ（小分け）", "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "洗顔料（小分け）",      "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ヘアゴム",             "for_gender": "female", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "生理用品",             "for_gender": "female", "for_season": "all","for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ビーチタオル",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
    ],

    "電子機器": [
        {"name": "スマホ",                 "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "スマホ充電器",           "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "モバイルバッテリー",     "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "イヤホン",               "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "USBケーブル",            "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "モバイルWi-Fi",          "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "ハンディファン",          "for_gender": "all", "for_season": "summer","for_weather": "all","for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "カメラ",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "防水カメラ",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "予備バッテリー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "メモリーカード / SDカード", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ポータブルゲーム機",      "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ゲームソフト",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ヘッドセット",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "コントローラー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ゲーム用充電器",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ノートPC",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "PC用充電器",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "マウス",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "社用スマホ",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "USBメモリ",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "レーザーポインター",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
    ],

    "書類・貴重品": [
        {"name": "財布",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "鍵",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "航空券／電子チケット",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "ship"], "is_general": True, "fixed_quantity": None},
        {"name": "ホテル予約確認書",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "クレジットカード",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "ETCカード",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["car"], "is_general": True, "fixed_quantity": "1"},
        {"name": "保険証",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "運転免許証",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "マイナンバーカード",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ガイドブック",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "観戦チケット",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "招待状",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ご祝儀",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "御朱印帳",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "名刺",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "書類 / 資料",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "履歴書",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
    ],

    "衛生・健康": [
        {"name": "ハンカチ",                        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "マスク",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "消毒液",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "常備薬（頭痛薬・腹痛薬・風邪薬など）", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "絆創膏",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "目薬",                            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "花粉症用薬",                       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "日焼け止め",                       "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "虫よけスプレー",                     "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "水筒",                            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "カラトリー",                       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
    ],

    "美容・スキンケア": [
        {"name": "化粧水 / 乳液 / 美容液",      "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "クレンジング / 洗顔料",       "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ファンデーション / BBクリーム", "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "アイブロウ / アイライナー",     "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "アイシャドウ / チーク",        "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "マスカラ",                    "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "リップクリーム",              "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "メイク落としシート",            "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "コットン",                    "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "パフ",                        "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name":  "化粧ポーチ",                  "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ヘアアイロン",                "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "ヘアブラシ",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ドライヤー",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "シェーバー",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "ヘアスタイリング用品",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "デオドラント",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
    ],
    
    "天候用品": [
        {"name": "折りたたみ傘",            "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "帽子",                  "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "サングラス",             "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "雨よけカバー（バッグ用）", "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "日傘",                  "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
    ],

    "季節用品": [
        {"name": "冷却シート / クールタオル", "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
        {"name": "使い捨てカイロ",          "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
    ],
    
    "交通関連": [
        {"name": "ICカード / 交通系カード", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["train", "bus"], "is_general": True, "fixed_quantity": None},
        {"name": "ブランケット / ひざ掛け", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "bus", "ship"], "is_general": True, "fixed_quantity": None},
        {"name": "アイマスク / 耳栓",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "bus", "ship"], "is_general": True, "fixed_quantity": None},
        {"name": "スマホホルダー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
    ],

    "収納用品": [
        {"name": "ポーチ / 小分け袋", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "圧縮袋",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"}, 
        {"name": "防水バッグ",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "ビニール袋",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": "1"},
        {"name": "バッグ(小さめ)",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": True, "fixed_quantity": None},
    ], 

    "ペット同伴用品": [
        {"name": "ケージ",                      "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ペット用フード",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "給水ボトル / 食器",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ペット用毛布 / タオル",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ペット用トイレ / トイレシート", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "リード / ハーネス",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ペット用ウェットティッシュ",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "おもちゃ",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "ペット用救急セット",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
    ],

    "アウトドア用品": [
        {"name": "テント",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "寝袋",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "マット",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ランタン",                "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "調理器具 / バーナー",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "食器 / カトラリー / コップ", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "食材 / 調味料",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "クーラーボックス",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "アウトドアチェア / テーブル",  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "レジャーシート",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
    ],

    "その他": [
        {"name": "お土産",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "三脚",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "浮き輪 / ビーチボール",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "防水ケース",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "非常食",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "地図 / コンパス / GPS",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": "1"},
        {"name": "スキー / スノーボード板",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ブーツ / スノーボードブーツ", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ストック（スキー用）",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ゴーグル",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "応援グッズ",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "双眼鏡",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "スケッチブック",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "鉛筆 / 色鉛筆 / 絵の具セット",  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "筆記用具",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
        {"name": "ノート",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["all"], "is_general": False, "fixed_quantity": None},
    ]
}


PURPOSE_ITEM_DATA = {
    "観光": [
        "ガイドブック", 
        "カメラ", 
        "水筒"
    ],

    "温泉": [
        "防水バッグ", 
        "水着"
    ],

    "食べ歩き": [
        "ビニール袋", 
        "カラトリー"
    ],

    "帰省": ["お土産"],

    "写真旅": [
        "カメラ", 
        "三脚", 
        "予備バッテリー", 
        "メモリーカード / SDカード"
    ],

    "ドライブ": ["スマホホルダー"],
    
    "ペット同伴": [
        "ケージ",
        "ペット用フード", 
        "給水ボトル / 食器", 
        "ペット用毛布 / タオル", 
        "ペット用トイレ / トイレシート",
        "リード / ハーネス", 
        "ペット用ウェットティッシュ", 
        "おもちゃ", 
        "ペット用救急セット"
    ],

    "海水浴": [
        "予備の着替え",
        "水着", 
        "ビーチタオル", 
        "ビーチサンダル", 
        "日焼け止め",
        "浮き輪 / ビーチボール", 
        "防水ケース"
    ],

    "登山": [
        "登山靴",
        "帽子",
        "レインジャケット",
        "水筒",
        "非常食",
        "地図 / コンパス / GPS",
    ],

    "キャンプ": [
        "テント",                   
        "寝袋",
        "マット",
        "ランタン",
        "虫よけスプレー",
        "調理器具 / バーナー",      
        "食器 / カトラリー / コップ",
        "食材 / 調味料",            
        "クーラーボックス",         
        "アウトドアチェア / テーブル"
    ],

    "スキー・スノーボード": [
        "スキーウェア",
        "手袋",
        "帽子",
        "ゴーグル",
        "ネックウォーマー",
        "ビニール袋",
        "スキー / スノーボード板",   
        "ブーツ / スノーボードブーツ",
        "ストック（スキー用）",      
    ],

    "マリンスポーツ": [
        "予備の着替え",
        "水着",
        "ビーチタオル",
        "ビーチサンダル",
        "日焼け止め",
        "防水カメラ"
    ],

    "ピクニック": [
        "レジャーシート",
        "食器 / カトラリー / コップ",
        "水筒",
        "クーラーボックス",
        "虫よけスプレー",
    ],

    "フェス・ライブ": [
        "レジャーシート",
        "レインジャケット",
        "日焼け止め",
        "帽子",
    ],

    "スポーツ観戦": [
        "観戦チケット",
        "応援グッズ",
        "レインジャケット",
        "双眼鏡",
    ],

    "花火大会": [
        "レジャーシート",
        "浴衣",
    ],

    "BBQ": [
        "虫よけスプレー",
        "調理器具 / バーナー",      
        "食器 / カトラリー / コップ",
        "食材 / 調味料",            
        "クーラーボックス",         
        "アウトドアチェア / テーブル",
    ],

    "結婚式参列": [
        "招待状",
        "ご祝儀",
        "スーツ",
        "革靴",
        "ドレス",
        "パンプス",
        "バッグ(小さめ)",
    ],

    "サウナ巡り": [
        "水着",
        "サンダル",
        "サウナハット",
        "予備の着替え"
    ],

    "絵画スケッチ": [
        "スケッチブック",
        "鉛筆 / 色鉛筆 / 絵の具セット"
    ],

    "神社仏閣巡り": [
        "御朱印帳",
        "筆記用具", 
        "水筒",
        "カメラ", 
    ],

    "ゲーム": [
        "ポータブルゲーム機",
        "ゲームソフト",
        "ヘッドセット",
        "コントローラー",
        "ゲーム用充電器",
    ],

    "出張": [
        "スーツ",
        "革靴",
        "ノートPC", 
        "PC用充電器",
        "マウス",   
        "社用スマホ",
        "USBメモリ",
        "名刺",
        "書類 / 資料",
        "筆記用具",
        "ノート"
    ],

    "研修・セミナー": [
        "ノートPC", 
        "PC用充電器",
        "マウス",
        "USBメモリ",
        "名刺",
        "書類 / 資料",
        "筆記用具",
        "ノート"
    ],

    "学会発表": [
        "ノートPC", 
        "PC用充電器",
        "マウス",
        "USBメモリ",
        "レーザーポインター",
        "名刺",
        "書類 / 資料",
        "筆記用具",
        "ノート",
    ],

    "面接・就活": [
        "スーツ",
        "革靴",
        "履歴書",
        "名刺",
        "書類 / 資料",
        "筆記用具",
        "ノート",
    ]

}

def seed_purpose():
    for p in PURPOSE_DATA:
        if not Purpose.query.filter_by(name=p["name"]).first():
           db.session.add(Purpose(name=p["name"], category=p["category"]))
    db.session.commit()

def seed_item():
    for category, items in ITEM_DATA.items():
        for item in items:
            if not Item.query.filter_by(name=item["name"]).first():
                db.session.add(
                    Item(
                        name=item["name"],
                        category=category,
                        for_gender=item.get("for_gender", "all"),
                        for_season=item.get("for_season", "all"),
                        for_weather=item.get("for_weather", "all"),
                        for_transport=item.get("for_transport", ["all"]),
                        min_days=item.get("min_days"),
                        max_days=item.get("max_days"),
                        is_general=item.get("is_general", False),
                        fixed_quantity=item.get("fixed_quantity"),
                    )
                )
    db.session.commit()

def seed_purpose_item():
    for purpose_name, items_name in PURPOSE_ITEM_DATA.items():
        purpose = Purpose.query.filter_by(name=purpose_name).first()
        if not purpose:
            continue
        items = Item.query.filter(Item.name.in_(items_name)).all()

        for item in items:
            if not PurposeItem.query.filter_by(purpose_id=purpose.id, item_id=item.id).first():
                db.session.add(PurposeItem(purpose_id=purpose.id, item_id=item.id))
    
    db.session.commit()

def ensure_seed_data():
    if Purpose.query.first():
        return
    
    seed_purpose()
    seed_item()
    seed_purpose_item()

# python seeds.py で初期データを投入
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_purpose()
        seed_item()
        seed_purpose_item()