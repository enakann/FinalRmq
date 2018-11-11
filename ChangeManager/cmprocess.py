from Pickling import Pickling
from time import time
import traceback
import json
from multiprocessing import current_process
from threading import Lock,current_thread

lock=Lock()

class CmProcess:
    def __init__(self,msg):
        self.msg=msg
        self.pending={}
        self.done={}
        self.final={}
        self.p = Pickling("mp_picling_db")
    def process(self):
        print("cmprocessing is called")
        print(current_process)
        print(current_thread)
        try:
           (pending,done)=self.pre_process()
        except Exception:
            raise
        setattr(self,'pending',pending)
        setattr(self,'done',done)

        if self.msg['status']=='done':
            self.out=self.done_process()
        if self.msg['status']=='pending':
            self.out=self.pending_process()
    def write(self):
        lock.acquire()
        print(current_process().name)
        self.final['pending']=self.pending
        self.final['done']=self.done
        self.p.write(self.final)
        lock.release()
    def pending_process(self):
        if self.msg["corrid"] in self.pending.keys():
            for item in self.pending[self.msg["corrid"]]:
                if self.msg["type"] in item.keys():
                    break
            else:
                self.pending[self.msg["corrid"]].append({self.msg["type"]: self.msg})
        else:
            self.pending[self.msg["corrid"]] = []
            self.pending[self.msg["corrid"]].append({self.msg["type"]: self.msg})
        self.write()

    def done_process(self):
        if self.msg["corrid"] in self.pending.keys():
            self.pending[self.msg["corrid"]].append({self.msg["type"]:self.msg})
            self.done[self.msg["corrid"]] = self.pending.pop(self.msg["corrid"])
        else:
            self.done[self.msg["corrid"]] = []
            self.done[self.msg["corrid"]].append({self.msg["type"]: self.msg})
        self.write()

    def pre_process(self):
        try:
            data = self.p.read()
            if data['pending']:
                pending = data['pending']
            else:
                pending={}
            if data['done']:
                done = data['done']
            else:
                done={}
        except Exception as e:
            print("Exception has occured during Pickling {}".format(e))
            raise
            self.p.write({'pending':{},'done':{}})
            self.process(self.msg)
        return (pending,done)

if __name__ == '__main__':
     msg={'username': u'navi', 'status': u'pending', 'ticket-num': u'srno1', 'type': u'test3', u'Payload': {u'source': u'10.10.10.1', u'destination': u'10.172.2.1', u'protocol': u'tcp', u'port': 22, u'input-row-id': 1}, 'corrid': u'10'}


     cm=CmProcess(msg)
     cm.process()
