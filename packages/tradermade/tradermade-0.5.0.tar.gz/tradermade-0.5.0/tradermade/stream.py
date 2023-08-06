import websocket
import time
import tradermade

try:
    import thread
except ImportError:
    import _thread as thread


ws = None
_api_key = None
_symbol = 'GBPUSD'

f = open("webSocketTester.log", "a")

def set_ws_key(api_key):
    global _api_key
    _api_key = api_key

def set_symbols(symbol):
    global _symbol
    _symbol = symbol

def get_symbols():
    return _symbol

def api_key():
    return _api_key

def on_message(ws, message):
    print(message)
    f.write(message  +  "\n" )
    f.flush()



def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        cred = '{"userKey":"'+_api_key+'", "symbol":"'+_symbol+'"}'
        ws.send(cred)
    thread.start_new_thread(run, ())


def connect():
    global ws
    ws = websocket.WebSocketApp("wss://marketdata.tradermade.com/feedadv",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

# def disconnect():
#     global ws
#     ws.close()