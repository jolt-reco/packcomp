from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user
from . import main_bp

@main_bp.route("/")
def top():
    logout_user()
    return render_template("top.html")

@main_bp.route("/terms")
def terms():
    return render_template("terms.html")

@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = request.form.get("message")

        if not message:
            flash("お問い合わせ内容を入力してください。", "error")
            return redirect(url_for("main.contact"))

        flash("送信が完了しました！（デモのため実際の送信は行っていません）", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")
