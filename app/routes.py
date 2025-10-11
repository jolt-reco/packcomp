from flask import Blueprint, render_template, request

bp = Blueprint("main", __name__)

@bp.route("/")
def top():
    return render_template("top.html")

@bp.route("/form")
def new_travel():
    return render_template("new_travel.html")

@bp.route("/list", methods=["POST"])
def items():
    # travel情報の受信(テスト用のみの記述:削除予定)
        travel_title = request.form.get("title")
        destination = request.form.get("destination")
        male_count = request.form.get("male_count")
        female_count = request.form.get("female_count")
        child_count = request.form.get("child_count")

    # 仮アイテムの受信(削除予定)
        mock_items = [
            {"name": "歯ブラシ", "quantity": 1},
            {"name": "パスポート", "quantity": 1},
            {"name": "オムツ", "quantity": child_count},
        ]

        return render_template(
            "items_list.html",
            title=travel_title,
            destination=destination,
            items=mock_items
        )