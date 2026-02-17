import asyncio
import websockets
import json
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.clients = {}
        self.messages = []
        self.max_messages = 100
    
    async def register(self, websocket):
        client_id = str(id(websocket))
        self.clients[client_id] = {
            'ws': websocket,
            'name': None,
            'joined': datetime.now()
        }
        return client_id
    
    async def unregister(self, client_id):
        if client_id in self.clients:
            del self.clients[client_id]
    
    async def broadcast(self, message, exclude_id=None):
        for cid, client in self.clients.items():
            if cid != exclude_id and client['ws'].open:
                try:
                    await client['ws'].send(json.dumps(message))
                except:
                    pass
    
    async def handle_client(self, websocket, path):
        client_id = await self.register(websocket)
        
        try:
            # Отправляем историю
            for msg in self.messages[-10:]:
                await websocket.send(json.dumps(msg))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    if data['type'] == 'set_name':
                        self.clients[client_id]['name'] = data['name']
                        
                        # Приветствие
                        await websocket.send(json.dumps({
                            'type': 'system',
                            'message': f'Добро пожаловать, {data["name"]}!'
                        }))
                        
                        # Уведомляем всех
                        await self.broadcast({
                            'type': 'user_joined',
                            'username': data['name']
                        }, exclude_id=client_id)
                        
                        # Отправляем количество онлайн
                        await self.broadcast({
                            'type': 'users_online',
                            'count': len([c for c in self.clients.values() if c['name']])
                        })
                        
                    elif data['type'] == 'message':
                        user_name = self.clients[client_id]['name']
                        if user_name:
                            msg_data = {
                                'type': 'message',
                                'user': user_name,
                                'text': data['text'],
                                'timestamp': datetime.now().isoformat()
                            }
                            
                            self.messages.append(msg_data)
                            if len(self.messages) > self.max_messages:
                                self.messages = self.messages[-self.max_messages:]
                            
                            await self.broadcast(msg_data)
                    
                    elif data['type'] == 'typing':
                        user_name = self.clients[client_id]['name']
                        if user_name:
                            await self.broadcast({
                                'type': 'typing',
                                'username': user_name,
                                'isTyping': data['isTyping']
                            }, exclude_id=client_id)
                            
                except json.JSONDecodeError:
                    pass
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            user_name = self.clients.get(client_id, {}).get('name')
            await self.unregister(client_id)
            
            if user_name:
                await self.broadcast({
                    'type': 'user_left',
                    'username': user_name
                })
                
                await self.broadcast({
                    'type': 'users_online',
                    'count': len([c for c in self.clients.values() if c['name']])
                })

async def main():
    chat_server = ChatServer()
    
    server = await websockets.serve(
        chat_server.handle_client,
        "0.0.0.0",
        5002,
        ping_interval=20,
        ping_timeout=40
    )
    
    print("🚀 YAPPUP Messenger Server запущен - server.py:122")
    print("🌐 WebSocket: ws://localhost:5002 - server.py:123")
    print("📁 Откройте index.html в браузере - server.py:124")
    
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
