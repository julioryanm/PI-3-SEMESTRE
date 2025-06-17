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
