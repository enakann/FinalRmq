from multiprocessing import Process,Lock
from pprint import pprint
pending={}
done={}


def work(msg):
    #print(pending)
    global pending
    global done
    if msg['corrid'] in pending.keys():
        if msg["status"]=="done":
            for item in  pending[msg["corrid"]]:
                print(item)
                if msg["type"] in item.keys():
                    done[msg["corrid"]]=pending.pop(msg["corrid"])
                    break
            else:
                pending[msg["corrid"]].append({msg["type"]:msg})
                done[msg["corrid"]]=pending.pop(msg["corrid"])
                    #print(msg)
                print("popped in else part")
              
        else:
            print("pending for {}".format(msg))
            for item in  pending[msg["corrid"]]:
                if msg["type"] in item.keys():
                    break
            else:
                pending[msg["corrid"]].append({msg["type"]:msg})
    else:
        pending[msg["corrid"]]=[]
        pending[msg["corrid"]].append({msg["type"]:msg})

def work2(msg):
    global pending
    global done
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





msg1={'corrid':'1234','type':'new_policy','msg':"New policy created","status":"pending"}

msg2={'corrid':'1234','type':'approver_policy','msg':"approver policy created","status":"pending"}

msg3={'corrid':'1235','type':'applier','msg':"New policy created","status":"pending"}

msg4={'corrid':'1234','type':'apply_result','msg':"New policy created","status":"done"}

msg5={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"pending"}

msg6={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"done"}

msg11={'corrid':'1239','type':'new_policy','msg':"New policy created","status":"pending"}

msg12={'corrid':'1238','type':'approver_policy','msg':"approver policy created","status":"pending"}

msg13={'corrid':'1238','type':'applier','msg':"New policy created","status":"pending"}

msg14={'corrid':'1236','type':'apply_result','msg':"New policy created","status":"pending"}

msg15={'corrid':'1236','type':'red_flag','msg':"New policy created","status":"done"}

msg16={'corrid':'1237','type':'new_policy','msg':"New policy created","status":"done"}

messages=[msg1,msg2,msg3,msg4,msg5,msg6]+[msg11,msg12,msg13,msg14,msg15,msg16]

print(messages)
for m in messages:
  # print("working on {}".format(m))
   work2(m)

print ("*********** pending *****************")
pprint(pending)


print ("*************** done *****************")
pprint(done)






