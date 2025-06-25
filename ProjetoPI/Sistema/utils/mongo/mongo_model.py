from bson import ObjectId
from Sistema.utils.mongo.mongo_connection import get_mongo_client
from datetime import datetime
from Sistema.models import Colaborador

class ControleRefeicoes:
    def __init__(self):
        self.db = get_mongo_client()
        self.collection = self.db["controle_diario"]  # nova coleção

    def registrar_refeicoes(self, data, colaboradores_ids, usuario):
        registros = []
        data_formatada = datetime.strptime(data, "%Y-%m-%d")

        for colaborador_id in colaboradores_ids:
            try:
                colaborador = Colaborador.objects.get(id=colaborador_id)
                registro = {
                    "colaborador_id": colaborador.id,
                    "colaborador_nome": colaborador.nome,
                    "obra_id": colaborador.obra.id,
                    "obra_nome": colaborador.obra.nome,
                    "data_refeicao": data_formatada,
                    "valor_refeicao": 8.00,
                    "registrado_em": datetime.now(),
                    "registrado_por_id": usuario.id,
                    "registrado_por_nome": usuario.username,
                }
                registros.append(registro)
            except Colaborador.DoesNotExist:
                continue  # ignora se colaborador não encontrado

        if registros:
            self.collection.insert_many(registros)

    def listar_registros(self):
        registros = list(self.collection.find())
        for r in registros:
            r["id"] = str(r["_id"])
           # r["data_refeicao"] = r["data_refeicao"].strftime("%Y-%m-%d")
        return registros

    def buscar_registro(self, registro_id):
        return self.collection.find_one({"_id": ObjectId(registro_id)})

    def atualizar_data_refeicao(self, registro_id, nova_data):
        data_formatada = datetime.strptime(nova_data, "%Y-%m-%d")
        return self.collection.update_one(
            {"_id": ObjectId(registro_id)},
            {"$set": {"data_refeicao": data_formatada}}
        )

    def excluir_registro(self, registro_id):
        return self.collection.delete_one({"_id": ObjectId(registro_id)})

    def _construir_query(self, filtros):
        query = {}
        if filtros.get("data_inicio"):
            query["data_refeicao"] = {"$gte": datetime.strptime(filtros["data_inicio"], "%Y-%m-%d")}
        if filtros.get("data_fim"):
            if "data_refeicao" not in query:
                query["data_refeicao"] = {}
            query["data_refeicao"]["$lte"] = datetime.strptime(filtros["data_fim"], "%Y-%m-%d")
        if filtros.get("obra_id"):
            query["obra_id"] = int(filtros["obra_id"])
        if filtros.get("colaborador_id"):
            query["colaborador_id"] = int(filtros["colaborador_id"])
        return query

    def total_refeicoes(self, filtros):
        query = self._construir_query(filtros)
        return self.collection.count_documents(query)

    def total_colaboradores_unicos(self, filtros):
        query = self._construir_query(filtros)
        return len(self.collection.distinct("colaborador_id", query))

    def refeicoes_por_dia(self, filtros):
        query = self._construir_query(filtros)
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$data_refeicao", "total": {"$sum": 1}, "soma_valor_refeicao": {"$sum": "$valor_refeicao"}}},
            {"$sort": {"_id": 1}}
        ]
        resultado = list(self.collection.aggregate(pipeline))

        # Formatar data no backend
        for r in resultado:
            r["data_formatada"] = r["_id"].strftime("%d/%m/%y")
        return resultado
    
    def somar_valor_refeicoes(self, filtros):
        query = self._construir_query(filtros)
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "soma_valor_refeicao": {"$sum": "$valor_refeicao"}}}
        ]
        resultado = list(self.collection.aggregate(pipeline))
        return resultado[0]["soma_valor_refeicao"] if resultado else 0

    def listar_obras_unicas(self):
        return self.collection.aggregate([
            {"$group": {
                "_id": {"obra_id": "$obra_id", "obra_nome": "$obra_nome"}
            }},
            {"$project": {
                "obra_id": "$_id.obra_id",
                "obra_nome": "$_id.obra_nome",
                "_id": 0
            }},
            {"$sort": {"obra_nome": 1}}
        ])

    def listar_colaboradores_unicos(self):
        return self.collection.aggregate([
            {"$group": {
                "_id": {"colaborador_id": "$colaborador_id", "colaborador_nome": "$colaborador_nome"}
            }},
            {"$project": {
                "colaborador_id": "$_id.colaborador_id",
                "colaborador_nome": "$_id.colaborador_nome",
                "_id": 0
            }},
            {"$sort": {"colaborador_nome": 1}}
        ])