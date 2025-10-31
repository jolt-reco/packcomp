from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import auth_bp
from app.models import User

# ログインページ
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"ログインしました。ようこそ{user.user_name}さん！")
            return redirect(url_for("main.travels_list"))
        else:
            flash("メールアドレスまたはパスワードが正しくありません。")

    return render_template("auth/login.html")

# 新規登録ページ
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # 既にメールが登録されていないか確認
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("このメールアドレスはすでに登録されています。")
            return redirect(url_for("auth.login"))

        # 新規ユーザー作成
        new_user = User(user_name=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("登録が完了しました！ログインしてください。")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")

# ログアウトページ
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。")
    return redirect(url_for("auth.login"))

# ゲストログイン
@auth_bp.route("/guest_login")
def guest_login():
    guest = User.query.filter_by(email="guest@example.com").first()
    if not guest:
        guest = User(user_name="ゲスト", email="guest@example.com")
        guest.set_password("guestpass")
        db.session.add(guest)
        db.session.commit()
    login_user(guest)
    flash("ログインしました。ようこそゲストさん！")
    return redirect(url_for("main.travels_list"))
