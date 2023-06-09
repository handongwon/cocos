from flask import url_for, Flask, render_template, redirect, request, session, flash
from DB_handler import DBModule


app = Flask(__name__)
app.secret_key ="cocos1998@naver.com"
DB = DBModule()

headings = {"Seller ID", "Coin Num", "Coin Price", "Total Price"}

@app.route("/")
def index():
    data = DB.sells_table()
    username = session.get("uid")
    usermoney = DB.db.child("users").child(username).child("money").get().val()
    usercoin = DB.db.child("users").child(username).child("coin").get().val()
    marketcoin = DB.db.child("users").child("MarketPlace").child("coin").get().val()
    
    price = DB.db.child("recentPrice").get()
    Price_data = price.val()
    print(Price_data)
    data_list = [(key, value) for key, value in Price_data.items()]
     #----------------------------------------------- 

    labels = [row[0] for row in data_list]
    values = [row[1] for row in data_list]
    # --------------------------------------------------

    if "uid" in session:
        return render_template("index.html", headings = headings, data = data ,username = username, usermoney = usermoney, usercoin = usercoin, marketcoin = marketcoin, labels= labels, values = values, login = True)
    else:
       return render_template("index.html", headings=headings, data = data, labels= labels, values = values,
                              login = False)
    
@app.route("/logout")
def logout():
    if "uid" in session:
        session.pop("uid")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))
    
@app.route("/login")
def login():
    if "uid" in session:
        return redirect(url_for("index"))
    return render_template("Login.html")

@app.route("/login_done", methods = ["get"])
def login_done():
    _id_ = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.login(_id_,pwd):
        session["uid"] = _id_
        return redirect(url_for("index"))
    else:
        flash("ID or PASSWORD ins't right")
        return redirect(url_for("login"))

@app.route("/signin")
def signin():
     return render_template("Signin.html")

@app.route("/signin_done", methods =["get"])
def signin_done():
    email = request.args.get("email")
    _id_ = request.args.get("id")
    pwd = request.args.get("pwd")
    name = request.args.get("name")
    
    if DB.signin(_id_, pwd, name, email):
        return redirect(url_for("index"))
    else:
        flash("ID is arleady exist ")
        return redirect(url_for("signin"))

@app.route("/chargePage")
def charge_page():
    if "uid" in session:
        return render_template("ChargeMoney.html")
    else:
       return redirect(url_for("index"))

@app.route("/charge_money")
def charge_money():
    amount = request.args.get("amount")
    username = session.get("uid")
    if DB.charge_money(amount, username):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("charge_page"))
    
@app.route("/withdrawPage")
def withdraw_page():
    if "uid" in session:
        return render_template("WithdrawMoney.html")
    else:
       return redirect(url_for("index"))

@app.route("/withdraw_money")
def withdraw_money():
    amount = request.args.get("amount")
    username = session.get("uid")
    if DB.withdraw_money(amount, username):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("withdraw_page"))

@app.route("/buy")
def buy():
    marketcoin = DB.db.child("users").child("MarketPlace").child("coin").get().val()
    
    if "uid" in session:
       return render_template("buy.html", marketcoin= marketcoin)
    else:
       return redirect(url_for("index"))

@app.route("/buy_coin")
def buy_coin():
    quantity = request.args.get("quantity")
    username = session.get("uid")
    if DB.buy_coin(quantity, username):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("buy"))

@app.route("/sell")
def sell():
   if "uid" in session:
       return render_template("sell.html")
   else:
       return redirect(url_for("index"))

@app.route("/sell_coin")
def sell_coin():
    quantity = request.args.get("quantity")
    price = request.args.get("price")
    username = session.get("uid")

    if DB.sell_coin(quantity, price ,username):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("sell"))

@app.route("/userBuy")
def userbuy():
    if "uid" in session:
       return render_template("userBuy.html")
    else:
       return redirect(url_for("index"))

@app.route("/userbuy_done")
def userbuy_done():
    seller_id = request.args.get("seller_id")
    username = session.get("uid")
    if DB.userbuy_done(seller_id, username):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("userbuy"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

