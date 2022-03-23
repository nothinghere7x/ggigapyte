import requests,random,string
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask import *
app = Flask(__name__)
req=requests.Session()
@app.route("/")
def add():
    try:
    	number = str(request.args.get('n'))
    	pwd = str(request.args.get('p'))
    	def generationLink(stringLingth):
    	   latters = string.ascii_lowercase
    	   return ''.join(random.choice(latters) for i in range(stringLingth))
    	url = f'https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/auth?client_id=website&redirect_uri=https%3A%2F%2Fweb.vodafone.com.eg%2Far%2FKClogin&state=286d1217-db14-4846-86c1-9539beea01ed&response_mode=query&response_type=code&scope=openid&nonce={generationLink(10)}&kc_locale=en'
    	responsePageLogin = req.get(url)
    	soup = BeautifulSoup(responsePageLogin.content, 'html.parser')
    	getUrlAction = soup.find('form').get('action')
    	headerRequest = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,ar;q=0.8,ar-EG;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'web.vodafone.com.eg',
    'Origin': 'https://web.vodafone.com.eg',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    
    	formData = {'username':number,'password':pwd}
    	sendUserData = req.post(getUrlAction,headers=headerRequest,data=formData)
    	checkRegistry = sendUserData.url
    	_checkRegistry = checkRegistry.find('KClogin')
    	if _checkRegistry != -1:
    		code = checkRegistry
    		_code = code[code.index('code=') + 5:]
    		header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.9,ar;q=0.8,ar-EG;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-type': 'application/x-www-form-urlencoded',
        'Host': 'web.vodafone.com.eg',
        'Origin': 'https://web.vodafone.com.eg',
        'Referer': 'https://web.vodafone.com.eg/ar/KClogin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
    		
    		formDataAccessToken = {
'code': _code,
        'grant_type': 'authorization_code',
        'client_id': 'website',
        'redirect_uri': 'https://web.vodafone.com.eg/ar/KClogin'
        }
    		sendDataAccessToken = req.post('https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token',headers=header,data=formDataAccessToken)
    		jwt = sendDataAccessToken.json()['access_token']
    		ur= "https://mobile.vodafone.com.eg/services/dxl/promo/promotion?$.context.type=basePromo&@type=Promo"
    		hd = {"User-Agent": "ismail", "channel": "MOBILE", "Accept-Language": "En", "api-version": "v2", "Authorization": "Bearer "+(jwt)+"", "Accept": "application/json", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "msisdn": number}
    		t=requests.get(ur, headers=hd)
    		if 'id' not in  t.text:
    		    return {"result":"offer not vaild to you"}
    		else:
    		    id=t.json()[0]['id']
    		    link = "https://mobile.vodafone.com.eg/services/dxl/promo/promotion/"+(id)+""
    		    hsd = {"Host": "mobile.vodafone.com.eg",
"Cache-Control": "no-cache",
"Charset": "utf-8",
"Content-Length": "105",
"User-Agent": "ismail", "channel": "MOBILE", "Accept-Language": "En", "api-version": "v2", "Authorization": "Bearer "+(jwt)+"", "Accept": "application/json", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "msisdn": number, "Connection": "close"}
    		    json={
  "@type" : "Promo",
  "channel" : {
    "id" : "5"
  },
  "context" : {
    "type" : "basePromo"
  }
}
    		    zxc=requests.patch(link, headers=hsd, json=json).json()
    		    reason=zxc["reason"]
    		    if "Generic System Error" in reason:
    		        return {"result":"You Take this offer before"}
    		    else:
    		        return {"result":"Done ADD offer"}
    	else:
    		return {"result":"Error number or password"}
    except:
        return {"result":"Worng in Script"}
if __name__ == "__main__":
    app.run(debug=True)