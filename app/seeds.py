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
        {"name": "Tシャツ",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "下着",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "靴下",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "パジャマ",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "部屋着",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "薄手の長袖",       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "薄手の上着",       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヒートテック（上）", "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヒートテック（下）", "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "厚手の上着",        "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "手袋",              "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "マフラー",          "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "予備の着替え",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "水着",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ビーチサンダル",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "サンダル",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "登山靴",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "レインジャケット",   "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": "all", "is_general": "False"},
        {"name": "スキーウェア",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ネックウォーマー",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "浴衣",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "スーツ",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "革靴",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ドレス",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "パンプス",             "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "サウナハット",        "for_gender": "male", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "生活用品": [
        {"name": "歯ブラシ",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "歯磨き粉",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "タオル",              "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ハンカチ",            "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ティッシュ",           "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ウェットティッシュ",     "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "シャンプー（小分け）",   "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ボディソープ（小分け）", "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "洗顔料（小分け）",      "for_gender": "all", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヘアゴム",             "for_gender": "female", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "生理用品",             "for_gender": "female", "for_season": "all","for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ビーチタオル",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "電子機器": [
        {"name": "スマホ",                 "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "スマホ充電器",           "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "モバイルバッテリー",     "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "イヤホン",               "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "USBケーブル",            "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "モバイルWi-Fi",          "for_gender": "all", "for_season": "all","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "ハンディファン",          "for_gender": "all", "for_season": "summer","for_weather": "all","for_transport": "all", "is_general": "True"},
        {"name": "カメラ",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "防水カメラ",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "予備バッテリー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "メモリーカード / SDカード", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ポータブルゲーム機",      "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ゲームソフト",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ヘッドセット",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "コントローラー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ゲーム用充電器",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ノートPC",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "PC用充電器",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "マウス",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "社用スマホ",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "USBメモリ",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "レーザーポインター",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "書類・貴重品": [
        {"name": "財布",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "鍵",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "航空券／電子チケット",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "ship"], "is_general": "True"},
        {"name": "ホテル予約確認書",         "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "クレジットカード",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ETCカード",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["car"], "is_general": "True"},
        {"name": "保険証",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "運転免許証",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "マイナンバーカード",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ガイドブック",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "観戦チケット",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "招待状",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ご祝儀",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "御朱印帳",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "名刺",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "書類 / 資料",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "履歴書",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "衛生・健康": [
        {"name": "ハンカチ",                        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "マスク",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "消毒液",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "常備薬（頭痛薬・腹痛薬・風邪薬など）", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "絆創膏",                          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "目薬",                            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "花粉症用薬",                       "for_gender": "all", "for_season": "mid", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "日焼け止め",                       "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "虫よけスプレー",                     "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "水筒",                            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "カラトリー",                       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "美容・スキンケア": [
        {"name": "化粧水 / 乳液 / 美容液",      "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "クレンジング / 洗顔料",       "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ファンデーション / BBクリーム", "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "アイブロウ / アイライナー",     "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "アイシャドウ / チーク",        "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "マスカラ",                    "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "リップクリーム",              "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "メイク落としシート",            "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "コットン",                    "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "パフ",                        "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name":  "化粧ポーチ",                  "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヘアアイロン",                "for_gender": "female", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヘアブラシ",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ドライヤー",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "シェーバー",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ヘアスタイリング用品",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "デオドラント",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
    ],
    
    "天候用品": [
        {"name": "折りたたみ傘",            "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": "all", "is_general": "True"},
        {"name": "帽子",                  "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": "all", "is_general": "True"},
        {"name": "サングラス",             "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": "all", "is_general": "True"},
        {"name": "雨よけカバー（バッグ用）", "for_gender": "all", "for_season": "all", "for_weather": "rain", "for_transport": "all", "is_general": "True"},
        {"name": "日傘",                  "for_gender": "all", "for_season": "summer", "for_weather": "sunny", "for_transport": "all", "is_general": "True"}
    ],

    "季節用品": [
        {"name": "冷却シート / クールタオル", "for_gender": "all", "for_season": "summer", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "使い捨てカイロ",          "for_gender": "all", "for_season": "winter", "for_weather": "all", "for_transport": "all", "is_general": "True"},
    ],
    
    "交通関連": [
        {"name": "ICカード / 交通系カード", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["train", "bus"], "is_general": "True"},
        {"name": "ブランケット / ひざ掛け", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "bus", "ship"], "is_general": "True"},
        {"name": "アイマスク / 耳栓",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": ["plane", "train", "bus", "ship"], "is_general": "True"},
        {"name": "スマホホルダー",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "収納用品": [
        {"name": "ポーチ / 小分け袋", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "圧縮袋",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"}, 
        {"name": "防水バッグ",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "ビニール袋",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
        {"name": "バッグ(小さめ)",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "True"},
    ], 

    "ペット同伴用品": [
        {"name": "ケージ",                      "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ペット用フード",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "給水ボトル / 食器",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ペット用毛布 / タオル",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ペット用トイレ / トイレシート", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "リード / ハーネス",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ペット用ウェットティッシュ",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "おもちゃ",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ペット用救急セット",          "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"}
    ],

    "アウトドア用品": [
        {"name": "テント",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "寝袋",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "マット",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ランタン",                "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "調理器具 / バーナー",       "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "食器 / カトラリー / コップ", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "食材 / 調味料",             "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "クーラーボックス",           "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "アウトドアチェア / テーブル",  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "レジャーシート",            "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
    ],

    "その他": [
        {"name": "お土産",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "三脚",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "浮き輪 / ビーチボール",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "防水ケース",               "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "非常食",                   "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "地図 / コンパス / GPS",     "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "スキー / スノーボード板",    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ブーツ / スノーボードブーツ", "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ストック（スキー用）",        "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ゴーグル",                  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "応援グッズ",                 "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "双眼鏡",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "スケッチブック",              "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "鉛筆 / 色鉛筆 / 絵の具セット",  "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "筆記用具",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
        {"name": "ノート",                    "for_gender": "all", "for_season": "all", "for_weather": "all", "for_transport": "all", "is_general": "False"},
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
        "ペット用トイレ / トイレシート"
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
        "スキーウェア"
        "手袋",
        "帽子",
        "ゴーグル",
        "ネックウォーマー",
        "ビニール袋"
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
    for i in ITEM_DATA:
        for category, items in ITEM_DATA.items():
            for item in items:
                if not Item.query.filter_by(name=item["name"]).first():
                    db.session.add(
                        Item(
                            name=i["name"],
                            category=category,
                            for_gender=i.get("for_gender", "all"),
                            for_season=i.get("for_season", "all"),
                            for_weather=i.get("for_weather", "all"),
                            for_transport=i.get("for_transport", "all"),
                            min_days=i.get("min_days"),
                            max_days=i.get("max_days")
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

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_purpose()
        seed_item()
        seed_purpose_item()