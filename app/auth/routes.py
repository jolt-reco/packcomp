from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import auth_bp
from app.models import User

# ログインページ
@auth_bp.route("/login")
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ログインに成功しました！")
            return redirect(url_for("main.top"))
        else:
            flash("メールアドレスまたはパスワードが正しくありません。")

    return render_template("auth/login.html")

# 新規登録ページ
@auth_bp.route("/register")
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # 既にメールが登録されていないか確認
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("このメールアドレスはすでに登録されています。")
            return redirect(url_for("auth.register"))

        # 新規ユーザー作成
        new_user = User(user_name=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("登録が完了しました！ログインしてください。")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

# ログアウトページ
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。")
    return redirect(url_for("auth.login"))