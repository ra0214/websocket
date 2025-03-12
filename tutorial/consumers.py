import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from .models import Carrera

class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("carreras_group", self.channel_name)
        await self.send_carrera_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("carreras_group", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                data = json.loads(text_data)
                
                if data.get('type') == 'crear_carrera':
                    carrera = await self.guardar_carrera(
                        data.get('nombre'),
                        data.get('descripcion')
                    )
                    if carrera:
                        await self.channel_layer.group_send(
                            "carreras_group",
                            {
                                "type": "carrera_actualizada",
                                "message": "Nueva carrera creada"
                            }
                        )
                
                elif data.get('type') == 'editar_carrera':
                    carrera = await self.editar_carrera(
                        data.get('id'),
                        data.get('nombre'),
                        data.get('descripcion')
                    )
                    if carrera:
                        await self.channel_layer.group_send(
                            "carreras_group",
                            {
                                "type": "carrera_actualizada",
                                "message": "Carrera actualizada"
                            }
                        )
                
                elif data.get('type') == 'eliminar_carrera':
                    deleted = await self.eliminar_carrera(data.get('id'))
                    if deleted:
                        await self.channel_layer.group_send(
                            "carreras_group",
                            {
                                "type": "carrera_actualizada",
                                "message": "Carrera eliminada"
                            }
                        )
                
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))

    async def carrera_actualizada(self, event):
        await self.send_carrera_list()

    async def send_carrera_list(self):
        carreras = await self.get_carreras()
        await self.send(text_data=json.dumps({
            'type': 'carrera_list',
            'message': carreras
        }))

    @database_sync_to_async
    def guardar_carrera(self, name, description):
        try:
            return Carrera.objects.create(
                name=name,
                description=description
            )
        except Exception as e:
            print(f"Error al guardar carrera: {e}")
            return None

    @database_sync_to_async
    def editar_carrera(self, id, name, description):
        try:
            carrera = Carrera.objects.get(id=id)
            carrera.name = name
            carrera.description = description
            carrera.save()
            return carrera
        except Carrera.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error al editar carrera: {e}")
            return None

    @database_sync_to_async
    def eliminar_carrera(self, id):
        try:
            carrera = Carrera.objects.get(id=id)
            carrera.delete()
            return True
        except Carrera.DoesNotExist:
            return False
        except Exception as e:
            print(f"Error al eliminar carrera: {e}")
            return False

    @database_sync_to_async
    def get_carreras(self):
        carreras = Carrera.objects.all()
        return [{'id': c.id, 'nombre': c.name, 'descripcion': c.description} for c in carreras]