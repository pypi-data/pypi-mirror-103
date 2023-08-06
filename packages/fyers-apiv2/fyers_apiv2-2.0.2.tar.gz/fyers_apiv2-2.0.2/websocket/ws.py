import os
import json
import time
import struct 
import asyncio
import logging
import traceback
from struct import Struct
from IPython import embed
from websockets import connect
from logging.config import dictConfig


class FyersSocket():

    def __init__(self, access_token=None, data_type=None, symbol=None):
        self.access_token = access_token # access token of the user
        self.data_type = data_type # type of data requested by the user
        self.ws_link = None
        self.ws = None 
        self.connected_flag = True
        self.transmit_flag = True
        self.receive_flag = False
        self.transmit_message = None
        self.data = None
        self.reconnect_counter = 0
        self.reconnect_flag = False
        self.symbol = symbol
        self.message = None
        self.response = {"s":"","code":"","message":""}
        
        # logger setup
        self.logger_setup()
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.access_token)

        # struct init
        self.FY_P_ENDIAN	    = '> '
        self.FY_P_HEADER_FORMAT = Struct(self.FY_P_ENDIAN + "Q L H H H 6x")
        self.FY_P_COMMON_7208   = Struct(self.FY_P_ENDIAN + "10I Q")
        self.FY_P_EXTRA_7208    = Struct(self.FY_P_ENDIAN + "4I 2Q")
        self.FY_P_MARKET_PIC    = Struct(self.FY_P_ENDIAN + "3I")
        self.FY_P_LENGTH        = Struct(self.FY_P_ENDIAN + "H")

        # packet length define
        self.FY_P_LEN_NUM_PACKET 	= 2
        self.FY_P_LEN_HEADER 		= 24
        self.FY_P_LEN_COMN_PAYLOAD	= 48 
        self.FY_P_LEN_EXTRA_7208	= 32 
        self.FY_P_LEN_BID_ASK 		= 12 
        self.FY_P_BID_ASK_CNT 		= 10
        self.FY_P_LEN_RES           = 6 

        # Aux
        self.counter = 0

    def logger_setup(self):
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'formatter': 'verbose',
                    'filename': 'fyers_socket.log'
                }
            },
            'loggers': {
                'fyers_socket': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propagate': False,
                }
            },
        }

        dictConfig(LOGGING)
        self.logger = logging.getLogger('fyers_socket')

    def on_message(self):
        """
            Called when a new message is received from websocket
        """
        if self.data_type == "symbolData":
            self.parse_symbol_data()
        else:
            print(str(self.data))

    def verify_msg(self,msg):
        try:
            # import ipdb; ipdb.set_trace()
            if type(msg) == str:
                msg = json.loads(msg)
            self.response["s"] = msg["s"]
            if "code" in msg:
                self.response["code"] = msg["code"]
                self.response["message"] = msg["message"] 
            return self.response
        except Exception as e:
            self.logger.error(str(traceback.format_exc()))
        # self.response = self.response

    def export_data(self, packet_data):
        self.counter += 1
        location = "/home/fyers/fyers/fyers-api-py/websocket/data/biocon"
        if not os.path.exists(location):
            os.makedirs(location)

        with open(os.path.join(location, str(self.counter) + ".json"), 'w+') as outfile:
            json.dump(packet_data, outfile)


    def parse_symbol_data(self):
        """
            Called when data_type is symbolData
        """
        self.message = self.data
        # print("-=-=-=-=-=-=-=-=-=-=-")
        # print(len(self.message))
        packet_length = int(len(self.message)/224)
        # print(packet_length, "this is div")
        if packet_length == 0:
            return
        # (packet_length, ) = self.FY_P_LENGTH.unpack(self.message[:self.FY_P_LEN_NUM_PACKET])
        # print(packet_length, "this is pack len")
        for i in range(packet_length):
            (fyToken, timestamp, fyCode, fyFlag, pktLen) = self.FY_P_HEADER_FORMAT.unpack(self.message[:self.FY_P_LEN_HEADER])
            packet_data = {"fyToken": fyToken, "timestamp": timestamp, "fyCode": fyCode, "fyFlag": fyFlag, "pktLen": pktLen}
            self.message = self.message[self.FY_P_LEN_HEADER:]

            pc, ltp, op, hp, lp, cp, mop, mhp, mlp, mcp, mv = self.FY_P_COMMON_7208.unpack(self.message[: self.FY_P_LEN_COMN_PAYLOAD])
            
            packet_data["ltp"] = ltp/pc
            packet_data["open_price"] = op/pc
            packet_data["high_price"] = hp/pc
            packet_data["low_price"] = lp/pc
            packet_data["close_price"] = cp/pc
            packet_data["min_open_price"] = mop/pc
            packet_data["min_high_price"] = mhp/pc
            packet_data["min_low_price"] = mlp/pc
            packet_data["min_close_price"] = mcp/pc
            packet_data["min_volume"] = mv
            
            self.message = self.message[self.FY_P_LEN_COMN_PAYLOAD:]
            ltq, ltt, atP, vtt, totBuy, totSell = self.FY_P_EXTRA_7208.unpack(self.message[: self.FY_P_LEN_EXTRA_7208])
            packet_data["last_traded_qty"] = ltq
            packet_data["last_traded_time"] = ltt
            packet_data["avg_trade_price"] = atP
            packet_data["vol_traded_today"] = vtt
            packet_data["tot_buy_qty"] = totBuy
            packet_data["tot_sell_qty"] = totSell
            
            packet_data["market_pic"] = []
            
            self.message = self.message[self.FY_P_LEN_EXTRA_7208:]
            for i in range(0, 10):
                prc, qty, num_ord = self.FY_P_MARKET_PIC.unpack(self.message[:self.FY_P_LEN_BID_ASK])
                packet_data["market_pic"].append({"price": prc/pc, "qty": qty, "num_orders": num_ord})
                self.message = self.message[self.FY_P_LEN_BID_ASK:]
                
            self.logger.info(packet_data)
            # print(packet_data)
            self.export_data(packet_data)

        # print(len(self.message))


    def on_error(self):
        print("error please view the fyers_socket.logs")
        return 


    def on_close(self):
        print("### closed ###")


    def close_socket(self):
        self.connected_flag = False


    def reset_reconnect_counter(self):
        self.reconnect_flag = False
        self.reconnect_counter = 0


    def reconnect(self):
        """
            will check the counter and initiate reconnection
        """
        
        if self.reconnect_counter < 3:
            self.logger.info("reconnecting initiating in 10 seconds")
            time.sleep(10)
            self.connected_flag = True
            self.reconnect_counter += 1
            self.receive()
        else:
            self.connected_flag = False
            self.logger.critical("reconnecting failed, please check your network")  


    def socket_data_define(self):
        """
            Map requested data_type to trasmit message for subscription
        """
        self.transmit_flag = True
        self.logger.info("requesting data for " + self.data_type)

        if self.data_type == "orderUpdate":
            self.transmit_message = {"T":"SUB_ORD", "SLIST":["orderUpdate"], "SUB_T": 1}
            self.ws_link = "wss://data.fyers.in/orderSock?type=orderUpdate&access_token="+ self.access_token +"&user-agent=fyers-api"

        elif self.data_type == "symbolData":
            self.transmit_message = {"T":"SUB_L2","L2LIST":[self.symbol],"SUB_T":1}
            self.ws_link = "wss://data.fyers.in/dataSock?access_token=" + self.access_token

        else:
            self.response["s"]="error"
            self.response["code"]=324
            self.response["message"]="please provide valid dataType"
            return self.response
        # self.ws = connect("wss://data.fyers.in/dataSockDev?token_id=<tokenHash>&type=orderUpdate")
        self.ws = connect(self.ws_link)
        self.logger.info("Connection Initiated")

    async def start_stream(self):
        async with self.ws as websocket:
            
            while self.connected_flag:
                
                if self.receive_flag:

                    if websocket.open:
                        self.reset_reconnect_counter()
            
                        try:
                            msg = await websocket.recv()

                            if type(msg)==str:
                                if "error" in msg:
                                    msg = json.loads(msg)
                                    processed_response = self.verify_msg(msg=msg)
                                    self.connected_flag= False
                                    self.reconnect_flag = False
                                    print(processed_response)
                                    
                                else:
                                    self.data = msg
                                    self.on_message()
                            else:
                                self.data = msg
                                self.on_message()

                        except Exception as e:
                            self.logger.error(str(traceback.format_exc()))
                            self.logger.debug(self.message)
                            print("Exception is", e)

                    else:
                        self.reconnect_flag = True
                        self.connected_flag = False

                if self.transmit_flag:
                    t = await websocket.send(json.dumps(self.transmit_message))
                    self.logger.info("transmitted connection settings")
                    self.transmit_flag = False
                    self.receive_flag = True
        

    def receive(self):
        resp = self.socket_data_define()
        if str(resp)!= "None":
            if resp["s"] == "error":
                self.logger.error(resp)
                return print(resp)
        try:
            asyncio.get_event_loop().run_until_complete(self.start_stream()) 
        except Exception as e:
            self.logger.error(e)
            self.logger.error(str(traceback.format_exc()))

            self.logger.info("Initiating reconnection after failure")
            if self.reconnect_flag:
                self.reconnect()

   

    
if __name__ == "__main__":
    pass
    # # API V2
    # access_token = "O3E6QXGC72-102:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MTk1ODcxODAsImV4cCI6MTYxOTY1NjI0MCwibmJmIjoxNjE5NTg3MTgwLCJhdWQiOlsieDoyIiwieDoxIiwieDowIiwiZDoxIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCZ2lQQnNyWFhoWlAwOHVUYzd3bGdvUWJ2TmpPaWtiQWh3OWpsaWpEeGtQNEh2dVZNRWlaaXlyM3ZBUjFuWWtxWEVOaklGNTVSM2JhOE9LdXlVTV8xSFlJT0NQTzZ0VlVZWTF0SkpiNFJzN245Vl9qQT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDIsInBvYV9mbGFnIjoiTiJ9.5I79TXoo7-rYnoQk7GjdWVQmCARGvScpvd1rZuRlkTE"
    
    # # API V1
    # # access_token ="zqyEYv3aLvkZX58xHtJFJbBr4j-kyHYoPdICS5x7EWaV7FinVtLpmLI6FL26umhhRXekXANXZow="
    
    # data_type = "orderUpdate"
    # data_type = "symbolData"

    # # symbol = "NSE:PNB-EQ"
    # # symbol = "NSE:SBIN-EQ"
    # symbol = "NSE:BIOCON-EQ"
    # # symbol = "BSE:PNB-A" 
    # symbol = "MCX:SILVERMIC21JUNFUT"
    # # symbol = ""
    # # def custom_message(self):
    # #     print ("Custom " + self.data)    
    # # FyersSocket.on_message = custom_message 

    # fs = FyersSocket(access_token=access_token, data_type=data_type,symbol=symbol)
    # # import ipdb; ipdb.set_trace()
    # fs.receive()

 