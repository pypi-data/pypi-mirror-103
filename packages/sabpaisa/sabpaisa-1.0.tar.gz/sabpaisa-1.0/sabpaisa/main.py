from . import auth
LIVE = ""
TESTING ="https://uatsp.sabpaisa.in/SabPaisa/sabPaisaInit"
class Sabpaisa:
    def __init__(self,auth=None,payerAddress="",payerEmail="",payerContact="",payerLastName="",payerFirstName="",URLfailure="",spURL="",spDomain=TESTING,username="",password="",txnId="",clientCode="",authKey="",authIV="",txnAmt="",tnxId="",URLsuccess="",email=""):
        self.auth=auth
        self.payerAddress=payerAddress
        self.payerEmail=payerEmail
        self.payerContact=payerContact
        self.payerLastName=payerLastName
        self.txnId=tnxId
        self.email=email
        self.payerFirstName=payerFirstName
        self.URLfailure=URLfailure
        self.URLsuccess=URLsuccess
        self.username=username
        self.password=password
        self.txnAmt=txnAmt
        self.authKey=authKey
        self.authIV=authIV
        self.spDomain=spDomain
        self.clientCode=clientCode
        
    def genrateLink(self):
          self.spURL = "?clientName=" + self.clientCode + "&usern=" + self.username + "&pass=" + self.password +"&amt=" +self.txnAmt + "&txnId=" + self.txnId + "&firstName=" + self.payerFirstName + "&lstName=" + self.payerLastName+"&contactNo=" + self.payerContact + "&Email=" + self.payerEmail + "&Add=" + self.payerAddress + "&ru=" + self.URLsuccess + "&failureURL=" + self.URLfailure
          authobj = auth.AESCipher(self.authKey,self.authIV)
          self.spURL = authobj.encrypt(self.spURL)
          self.spURL=str(self.spURL)
          self.spURL = self.spURL.replace("+", "%2B")
          self.spURL = "?query=" +self.spURL[2:].replace("'", "")+"&clientName="+self.clientCode
          self.spURL=self.spDomain+self.spURL
          return self.spURL

# 0QvWIQBSz4AX0VoH
if __name__=="__main__":
 dic={"username":"nishant.jha_2885","password":"SIPL1_SP2885","API_KEY":"rMnggTKFvmGx8y1z","API_IV":"0QvWIQBSz4AX0VoH","client_code":"SIPL1","email":"kanu0704@gmail.com"}
 s = Sabpaisa(URLfailure="http://localhost:8080/payment/",URLsuccess="http://localhost:8080/payment/",payerFirstName="kanishk",payerLastName="kanishk",auth=True,payerContact="+918979626196",payerAddress="ABC",tnxId="3242324csvsdd2323",username=dic["username"],password=dic["password"],authKey=dic["API_KEY"],authIV=dic["API_IV"],clientCode=dic["client_code"],payerEmail="kanu0704@gmail.com",txnAmt="400")

 print(s.genrateLink())

        
