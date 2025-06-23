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
                    "valor_refeicao": "8,00",
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
