from multiprocessing import Process,Lock,Manager
import multiprocessing
from gen_proxy import FirmsConsumer
from pprint import pprint
from Pickling import Pickling
from time import time
import traceback
import json
from cmprocess import CmProcess
from threading import Thread
loc=Lock()

def consume_process(config):
 try:
   with FirmsConsumer(config) as conn:
      print(conn)
      conn.consume(callback2)
 except KeyboardInterrupt:
     print("keyboard interrupt")
 except Exception as e:
    traceback.print_exc()
    raise 




def callback(prop,msg):
     prop=prop.headers
     msg=json.loads(msg)
     #prop=prop.update(msg)
     #print(prop,type(prop))
     #print(msg,type(msg))
     msg.update(prop)
     print(msg)
     func2(prop,msg) 
     return 1

def callback2(prop,msg):
     prop=prop.headers
     msg=json.loads(msg)
     msg.update(prop)
     print(msg)
     cm=CmProcess(msg)
     try:
       cm.process()
     except Exception as e:
        traceback.print_exc()
        raise
     print(msg)
     return 1







def func2(prop,msg):
    loc.acquire()
    print(multiprocessing.current_process().name)
    print(msg)
    #print(prop.headers)
    loc.release()


		
if __name__ == '__main__':
    
    config_cm={'userName':'kannan',
    'password':'divya123',
    'host':'rabbitmq-1',
    'port':'5672',
    'virtualHost':'change.manager',
    'exchangeName':'cm',
    'queueName':'change.manager.queue',
    'routingKey':'cm',
    'props':{'content_type' :'text/plain',
             'delivery_mode':2}
    }
	
	
	
    consumer_list = [config_cm]*2
# execute
    process_list = []
    for sub in consumer_list:
        process = Process(target=consume_process,args=(config_cm,))
        process.daemon=True
        process.start()
        process_list.append(process)
# wait for all process to finish
    for process in process_list:
        process.join()



