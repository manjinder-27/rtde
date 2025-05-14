import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Document
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


async def save_doc(doc):
    await sync_to_async(doc.save)()

async def del_doc(doc):
    await sync_to_async(doc.delete)()

@database_sync_to_async
def get_doc(id):
    return Document.objects.get(uniqID=id)

@database_sync_to_async
def assignID(doc):
    return doc.assignUniqID()

async def assign_doc_id(doc):
    await assignID(doc)


class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data_rec = json.loads(text_data)
        msg = data_rec['msg']
        if msg == "sv" or msg == "clsv":
            docID = data_rec['docID']
            doc = await get_doc(docID)
            doc.content = data_rec['data']
            await save_doc(doc)
            if msg == "clsv":
                await assign_doc_id(doc)
                await save_doc(doc)
                await self.channel_layer.group_send(self.room_group_name,{"type":"close.redirect","msg":"close_redirect","user":data_rec["user"]})
            else:
                await self.channel_layer.group_send(self.room_group_name,{"type":"file.saved","msg": "saved","user":data_rec["user"]})
        elif msg == "dlt":
            doc = await get_doc(data_rec['docID'])
            await del_doc(doc)
            await self.channel_layer.group_send(self.room_group_name,{"type":"del.redirect","msg":"del_redirect","user":data_rec["user"]})
        elif msg == "cpos":
            data = {
                "type":"setCursorPos",
                "msg":data_rec["msg"],
                "pos":data_rec["pos"],
                "username":data_rec["username"]
            }
            await self.channel_layer.group_send(self.room_group_name,data)
        elif msg == "content":
            data = {
                "type":"updateContent",
                "msg":data_rec["msg"],
                "data":data_rec["data"]
            }
            await self.channel_layer.group_send(self.room_group_name,data)
        elif msg == "connected":
            data = {
                "type":"connected",
                "msg":"connected",
                "user":data_rec["username"]
            }
            await self.channel_layer.group_send(self.room_group_name,data)
        else:
            print(">> Something Else")
    

    async def setCursorPos(self,event):
        await self.send(text_data=json.dumps({
            'msg':event['msg'],
            'pos':event['pos'],
            'username':event['username']
        }))
    
    async def updateContent(self,event):
        await self.send(text_data=json.dumps({
            "msg":event["msg"],
            "data":event["data"]
        }))
    
    async def connected(self,event):
        await self.send(text_data=json.dumps({
            "msg":"connected",
            "user":event["user"]
        }))
    
    async def close_redirect(self,event):
        await self.send(text_data=json.dumps({
            "msg":event["msg"],
            "user":event["user"]
        }))

    async def del_redirect(self,event):
        await self.send(text_data=json.dumps({
            "msg":event["msg"],
            "user":event["user"]
        }))

    async def file_saved(self,event):
        await self.send(text_data=json.dumps({
            "msg":event["msg"],
            "user":event["user"]
        }))