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
            pending[msg["corrid"]].append({msg["type"]:msg})
    else:
        pending[msg["corrid"]]=[]
        pending[msg["corrid"]].append({msg["type"]:msg})






msg1={'corrid':'1234','type':'new_policy','msg':"New policy created","status":"pending"}

msg2={'corrid':'1234','type':'approver_policy','msg':"approver policy created","status":"pending"}

msg3={'corrid':'1235','type':'applier','msg':"New policy created","status":"pending"}

msg4={'corrid':'1234','type':'apply_result','msg':"New policy created","status":"done"}

msg5={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"pending"}


msg6={'corrid':'1235','type':'new_policy','msg':"New policy created","status":"pending"}

messages=[msg1,msg2,msg3,msg4,msg5,msg6]

print(messages)
for m in messages:
  # print("working on {}".format(m))
   work(m)

print ("*********** pending *****************")
pprint(pending)


print ("*************** done *****************")
pprint(done)






