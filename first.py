from flask import Flask, request
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws,order_ws
from flask_cors import CORS
app = Flask(__name__)
client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

CORS(app, resources={
    r"/buy": {"origins": "*"},
    r"/subscribe": {"origins": "*"},
    r"/sell": {"origins": "*"},
    r"/holdings": {"origins": "*"}
})
@app.route("/holdings", methods=["GET"])
def holdings():
    response = fyers.holdings()
    return response

@app.route("/buy", methods=["POST"])
def buy():
    type1 = request.form.get('type')
    if type1 =="Limit_Order":
        type1 = 1
    elif type1 == "Market_Order":
        type1 = 2
    elif type1 == "Stop_Order":
        type1 == 3
    elif type1 == "StopLimit_Order":
        type1 == 4

    data =  {
    "symbol": request.form.get('symbol'),
    "qty": int(request.form.get('qty')),
    "type": int(type1),
    "side": 1, # 1 for buy order
    "productType": "INTRADAY",
    "limitPrice": 0,
    "stopPrice": 0,
    "validity": "DAY",
    "disclosedQty": 0,
    "offlineOrder": False,
    "orderTag": "tag1"
    }
    response = fyers.place_order(data)
    print(response)
    return response

@app.route("/sell", methods=["POST"])
def sell():
    type1 = request.form.get('type')
    if type1 =="Limit_Order":
        type1 = 1
    elif type1 == "Market_Order":
        type1 = 2
    elif type1 == "Stop_Order":
        type1 == 3
    elif type1 == "StopLimit_Order":
        type1 == 4
    data = {
    "symbol": request.form.get('symbol'),
    "qty": int(request.form.get('qty')),
    "type": int(type1),
    "side": 1, # 1 for buy order
    "productType": "INTRADAY",
    "limitPrice": 0,
    "stopPrice": 0,
    "validity": "DAY",
    "disclosedQty": 0,
    "offlineOrder": False,
    "orderTag": "tag1"
    }
    response = fyers.place_order(data)
    return response

@app.route("/subscribe", methods=["GET"])
def subscribe():
   
    ws.connect()
    return "Subscribed"

def onopen():
    data_type = "SymbolUpdate"
    
    # Subscribe to the specified symbols and data type
    symbols = ["NSE:NIFTY50-INDEX" , "NSE:NIFTYBANK-INDEX"]
    ws.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data
    ws.keep_running()
    print("Websocket connected")

def onclose(message):
    print("Websocket closed",message)

def onerror(message):
    print("Error:", message)

def onmessage(message):
    print("Response:", message)


ws = data_ws.FyersDataSocket(
    access_token=client_id+":"+ access_token, #clientid:token recieved
    log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=False,                  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,              # Save response in a log file instead of printing it.
    reconnect=True,
    on_connect=onopen,
    on_close=onclose,
    on_error=onerror,
    on_message=onmessage,
)


if __name__ == "__main__":
    app.run(debug=True)