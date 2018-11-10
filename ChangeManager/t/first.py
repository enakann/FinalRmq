from multiprocessing import Process,Lock,Manager,Queue
from pprint import pprint
from Pickling import Pickling
ls2=[]

def work(msg,loc):
    d={}
    #print(pending)
    loc.acquire()
    p=Pickling("mp_picling_db")
    data=p.read()
    pending=data['pending']
    done=data['done']
    if msg['corrid'] in pending.keys():
        if msg["status"]=="done":
            for item in  pending[msg["corrid"]]:
        #        print(item)
                if msg["type"] in item.keys():
                    done[msg["corrid"]]=pending.pop(msg["corrid"])
                    break
            else:
                pending[msg["corrid"]].append({msg["type"]:msg})
                done[msg["corrid"]]=pending.pop(msg["corrid"])
                    #print(msg)
       #         print("popped in else part")
              
        else:
      #      print("pending for {}".format(msg))
            for item in  pending[msg["corrid"]]:
                if msg["type"] in item.keys():
                    break
            else:
                pending[msg["corrid"]].append({msg["type"]:msg})
    else:
        pending[msg["corrid"]]=[]
        pending[msg["corrid"]].append({msg["type"]:msg})
    d["pending"]=pending
    d["done"]=done
    p.write(d)
    loc.release()


def work2(msg,loc):
    loc.acquire()
    d={}
    p=Pickling("mp_picling_db")
    data=p.read()
    #pending={}
    #done={}
    pending=data['pending']
    done=data['done']
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

    messages=[msg1,msg2,msg3,msg4,msg5,msg6]+[msg11,msg12,msg13,msg14,msg15,msg16]
    
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


    print ("*********** pending *****************")
    print(pending)


    print ("*************** done *****************")
    print(done)

    print(ls2)




