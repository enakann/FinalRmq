from multiprocessing import Process,Lock,Manager,Queue
import multiprocessing
from pprint import pprint
from Pickling import Pickling
ls2=[]



def work2(msg,loc):
    print(multiprocessing.current_process().name)
    loc.acquire()
    d={}
    p=Pickling("mp_picling_db")
    try:
        data=p.read()
        #print(data)
        if data['pending']:
             pending=data['pending']
        else:
            pending={}
        if data['done']:
            done=data['done']
        else:
            done={}
    except Exception as e:
        data={}
        pending={}
        done={}
        print("Exception has occured during Pickling {}".format(e))
    if msg["status"]=="done":
        if msg["corrid"] in pending.keys():
            pending[msg["corrid"]].append({msg["type"]:msg})
            done[msg["corrid"]]=pending.pop(msg["corrid"])
    else:
        if msg["corrid"] in pending.keys():
             pending[msg["corrid"]].append({msg["type"]:msg})
        else:
            pending[msg["corrid"]]=[]
            pending[msg["corrid"]].append({msg["type"]:msg})

    d["pending"]=pending
    d["done"]=done
    p.write(d)
    loc.release()




def manager(q,l):
    while not q.empty():
        item=q.get()
        work2(item,l)




if __name__ == '__main__':
    #manager=Manager()
    pending={}
    done={}
    lock=Lock()
    q=Queue()
    msg1={'corrid':'12134','type':'new_policy','msg':"New policy created","status":"pending"}
    msg2={'corrid':'12134','type':'approver_policy','msg':"approver policy created","status":"pending"}
    msg3={'corrid':'1235','type':'applier','msg':"New policy created","status":"pending"}
    msg4={'corrid':'1234','type':'apply_result','msg':"New policy created","status":"done"}
    msg5={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"pending"}
    msg6={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"done"}
    msg11={'corrid':'1239','type':'new_policy','msg':"New policy created","status":"pending"}
    msg12={'corrid':'1238','type':'approver_policy','msg':"approver policy created","status":"pending"}
    msg13={'corrid':'1238','type':'applier','msg':"New policy created","status":"pending"}
    msg14={'corrid':'12134','type':'apply_result','msg':"New policy created","status":"done"}
    msg15={'corrid':'1236','type':'red_flag','msg':"New policy created","status":"done"}
    msg16={'corrid':'1237','type':'new_policy','msg':"New policy created","status":"done"}

    msg17={'corrid':'12135','type':'new_policy','msg':"New policy created","status":"pending"}
    msg18={'corrid':'12135','type':'new_policy','msg':"New policy created","status":"pending"}
    msg19={'corrid':'12135','type':'new_policy','msg':"New policy created","status":"pending"}
    msg20={'corrid':'12135','type':'new_policy','msg':"New policy created","status":"pending"}
    messages=[]
    #messages=[msg1,msg2,msg3,msg4,msg5,msg6]
    #messages=messages+[msg11,msg12,msg13,msg14,msg15,msg16]
    messages=messages+[msg17,msg18,msg19,msg20]
    ls=[]
    #print(messages)
    for m in messages:
        q.put(m)
    for m in messages:
        ls.append(Process(target=manager,args=(q,lock)))
    for proc in ls:
        proc.start()
    for proc in ls:
        proc.join()


    import subprocess
    subprocess.call(['python','Pickling.py'])



