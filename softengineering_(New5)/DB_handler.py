import pyrebase 
import json
from collections import OrderedDict

class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)
        
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def login(self, uid, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[uid]
            if userinfo["pwd"] == pwd:
                return True
            else:
                return False
        except:
            return False
    
    def signin(self, _id_, pwd, name, email):
       id = _id_
       coin =  0
       money = 0
       information = {"pwd":pwd,"uname": name,"email": email, "coin":coin, "money":money}

       if self.signin_verification(id):
            self.db.child("users").child(id).set(information)
            return True
       else:
           return False
       
    def signin_verification(self, id):
        users = self.db.child("users").get().val()
        for i in users:
            if id == i:
                return False
        return True
    
    def buy_coin(self, quantity, username):
        num = int(quantity)
        uid = username
        UserMoney = self.db.child("users").child(uid).child("money").get().val()
        UserCoin = self.db.child("users").child(uid).child("coin").get().val()
        MarketCoin = self.db.child("users").child("MarketPlace").child("coin").get().val()
        if MarketCoin >= num: #마켓에 충분한 코인이 있다면~
            if UserMoney >= num*100: #유저에게 충분한 돈이 있다면~
                NewMoney = UserMoney - num*100
                NewCoin = MarketCoin - num
                UserCoin = UserCoin + num
                self.db.child("users").child("MarketPlace").child("coin").set(NewCoin) #마켓 코인 변화
                self.db.child("users").child(uid).child("coin").set(UserCoin) #유저 코인량 변화
                self.db.child("users").child(uid).child("money").set(NewMoney) #유저 돈 변화
                self.update_coinPrice(100)
                return True
            else:
                return False
        return False
    
    def sell_coin(self, quantity, price ,  username):
       uid = username
       CoinNum = int(quantity)
       CoinPrice = int(price)
       total_price = CoinNum*CoinPrice
       information = {"quantity" : quantity, "price" :  price, "total_price" : str(total_price)}
       UserCoin = self.db.child("users").child(uid).child("coin").get().val()

       if UserCoin >= CoinNum: #유저에게 코인이 충분히 있다면~
           self.db.child("sells").child(uid).set(information) #판매 DB에 등록
           return True
       return False
   
    def charge_money(self, amount, username):
        addAmount = int(amount)
        uid = username
        UserMoneyAmount = self.db.child("users").child(uid).child("money").get().val()
        if addAmount >= 0:
            UserMoneyAmount += addAmount
            self.db.child("users").child(uid).child("money").set(UserMoneyAmount) #amount만큼 입금
            return True
        return False
    
    def withdraw_money(self, amount, username):
        subAmount = int(amount)
        uid = username
        UserMoneyAmount = self.db.child("users").child(uid).child("money").get().val()
        if subAmount <= UserMoneyAmount: #출금하려는 금액 이상을 보유하고 있다면
            UserMoneyAmount -= subAmount
            self.db.child("users").child(uid).child("money").set(UserMoneyAmount) #amount만큼 출금
            return True
        return False
    
    def show_userinfo(self, username):
        uid = username
        UserMoneyAmount = self.db.child("users").child(uid).child("money").get().val()
        result = [ uid, UserMoneyAmount ]
        return result
    
    def sells_table(self):
        data = self.db.child("sells").get().val()
        result = [(key, value['quantity'], value['price'], value['total_price']) for key, value in data.items()]
        return result
    
    def userbuy_done(self, seller_id, username):
        uid = username
        sid = seller_id
        UserMoneyAmount = self.db.child("users").child(uid).child("money").get().val()
        UserCoinAmount = self.db.child("users").child(uid).child("coin").get().val()
        SellerMoneyAmount = self.db.child("users").child(sid).child("money").get().val()
        SellerCoinAmount = self.db.child("users").child(sid).child("coin").get().val()

        try:
            seller_total= self.db.child("sells").child(sid).child("total_price").get().val() #판매자 id가 등록 되어있는 지 확인
            seller_coin = self.db.child("sells").child(sid).child("quantity").get().val()
            recentPrice = self.db.child("sells").child(sid).child("price").get().val()
            
            if UserMoneyAmount >= int(seller_total): #유저 돈이 total price보다 많다면~
                #거래 채결 , sells에서 데이터 삭제하고, seller에게 돈 주고 코인뺏고, 유저에게 코인주고 돈 뺏고
                NewMoneyU = UserMoneyAmount - int(seller_total)
                NewCoinU = UserCoinAmount + int(seller_coin)
                NewMoneyS = SellerMoneyAmount + int(seller_total)
                NewCoinS = SellerCoinAmount - int(seller_coin)

                self.db.child("users").child(uid).child("coin").set(NewCoinU) #유저 코인량 늘어남
                self.db.child("users").child(uid).child("money").set(NewMoneyU) #유저 돈 줄어듬

                self.db.child("users").child(sid).child("coin").set(NewCoinS) #판매자 코인량 줄어듬
                self.db.child("users").child(sid).child("money").set(NewMoneyS) #판매자 돈 늘어남

                self.db.child("sells").child(sid).remove() #sells 삭제
                money = int(recentPrice)
                # 동원
                self.update_coinPrice(money)

                return True
            else:
                return True
        except:
            return False
    
    def update_coinPrice(self, recentPrice):
        data = self.db.child("recentPrice").get().val()
        temp = [data['1th'],data['2th'],data['3th'],data['4th'],data['5th'],data['6th'],data['7th'],data['8th']]
        # 가장 최근 가격 업데이트
        data['1th'] = temp[1]
        data['2th'] = temp[2]
        data['3th'] = temp[3]
        data['4th'] =temp[4]
        data['5th'] = temp[5]
        data['6th'] = temp[6]
        data['7th'] = temp[7]
        data['8th'] = recentPrice  # 최근 가격 추가
        dict_data = dict(data)
        self.db.child("recentPrice").remove()

        self.db.child("recentPrice").set(dict_data)
           



       
