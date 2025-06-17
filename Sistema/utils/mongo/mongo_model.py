from bson import ObjectId
from Sistema.utils.mongo.mongo_connection import get_mongo_client

class Pedido:
    def __init__(self):
        self.db = get_mongo_client()
        self.collection = self.db["pedidos"]

    def criar_pedido(self, tipo, valor):
        pedido = {"tipo": tipo, "valor": float(valor)}
        return self.collection.insert_one(pedido)

    def listar_pedidos(self):
        pedidos = list(self.collection.find())
        for pedido in pedidos:
            pedido["id"] = str(pedido["_id"])
        return pedidos

    def buscar_pedido(self, pedido_id):
        return self.collection.find_one({"_id": ObjectId(pedido_id)})

    def atualizar_pedido(self, pedido_id, tipo, valor):
        return self.collection.update_one(
            {"_id": ObjectId(pedido_id)},
            {"$set": {"tipo": tipo, "valor": float(valor)}}
        )

    def excluir_pedido(self, pedido_id):
        return self.collection.delete_one({"_id": ObjectId(pedido_id)})
