import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from bson import ObjectId

from Sistema.utils.mongo.mongo_model import ControleRefeicoes
from Sistema.models import Colaborador

class TestControleRefeicoes(unittest.TestCase):

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    @patch("Sistema.models.Colaborador.objects.get")
    def test_registrar_refeicoes(self, mock_get_colaborador, mock_get_client):
        mock_colaborador = MagicMock()
        mock_colaborador.id = 13
        mock_colaborador.nome = "Carlos Mendes"
        mock_colaborador.obra.id = 1
        mock_colaborador.obra.nome = "aeroporto"
        mock_get_colaborador.return_value = mock_colaborador

        mock_collection = MagicMock()
        mock_db = {"controle_diario": mock_collection}
        mock_get_client.return_value = mock_db

        controle = ControleRefeicoes()
        usuario_mock = MagicMock()
        usuario_mock.id = 6
        usuario_mock.username = "joao"

        controle.registrar_refeicoes("2025-06-25", [13], usuario_mock)

        self.assertTrue(mock_collection.insert_many.called)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    @patch("Sistema.models.Colaborador.objects.get")
    def test_registrar_refeicao_colaborador_nao_encontrado(self, mock_get_colaborador, mock_get_client):
        mock_get_colaborador.side_effect = Colaborador.DoesNotExist
        mock_collection = MagicMock()
        mock_db = {"controle_diario": mock_collection}
        mock_get_client.return_value = mock_db

        controle = ControleRefeicoes()
        usuario_mock = MagicMock()
        usuario_mock.id = 99
        usuario_mock.username = "joao"

        controle.registrar_refeicoes("2025-06-25", [999], usuario_mock)
        mock_collection.insert_many.assert_not_called()

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_listar_registros(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.find.return_value = [{"_id": ObjectId(), "colaborador_nome": "Carlos"}]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        registros = controle.listar_registros()
        self.assertGreater(len(registros), 0)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_buscar_registro(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {"colaborador_nome": "Carlos"}
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        result = controle.buscar_registro(ObjectId())
        self.assertEqual(result["colaborador_nome"], "Carlos")

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_atualizar_data_refeicao(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.update_one.return_value.modified_count = 1
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        result = controle.atualizar_data_refeicao(ObjectId(), "2025-06-25")
        self.assertEqual(result.modified_count, 1)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_excluir_registro(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.delete_one.return_value.deleted_count = 1
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        result = controle.excluir_registro(ObjectId())
        self.assertEqual(result.deleted_count, 1)

    def test_construir_query_completa(self):
        controle = ControleRefeicoes()
        filtros = {
            "data_inicio": "2025-06-01",
            "data_fim": "2025-06-10",
            "obra_id": "1",
            "colaborador_id": "13"
        }
        query = controle._construir_query(filtros)
        self.assertIn("data_refeicao", query)
        self.assertIn("$gte", query["data_refeicao"])
        self.assertIn("$lte", query["data_refeicao"])
        self.assertEqual(query["obra_id"], 1)
        self.assertEqual(query["colaborador_id"], 13)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_total_refeicoes(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.count_documents.return_value = 5
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        total = controle.total_refeicoes({})
        self.assertEqual(total, 5)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_total_colaboradores_unicos(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.distinct.return_value = [13, 7, 8]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        self.assertEqual(controle.total_colaboradores_unicos({}), 3)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_refeicoes_por_dia(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [{"_id": datetime(2025, 6, 25), "total": 2, "soma_valor_refeicao": 16.0}]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        resultado = controle.refeicoes_por_dia({})
        self.assertEqual(resultado[0]["data_formatada"], "25/06/25")

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_somar_valor_refeicoes(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [{"soma_valor_refeicao": 80.0}]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        self.assertEqual(controle.somar_valor_refeicoes({}), 80.0)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_somar_valor_refeicoes_vazio(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = []
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        self.assertEqual(controle.somar_valor_refeicoes({}), 0)

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_listar_obras_unicas(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [{"obra_id": 1, "obra_nome": "aeroporto"}]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        resultado = list(controle.listar_obras_unicas())
        self.assertEqual(resultado[0]["obra_nome"], "aeroporto")

    @patch("Sistema.utils.mongo.mongo_model.get_mongo_client")
    def test_listar_colaboradores_unicos(self, mock_get_client):
        mock_collection = MagicMock()
        mock_collection.aggregate.return_value = [
            {"colaborador_id": 13, "colaborador_nome": "Carlos Mendes"},
            {"colaborador_id": 7, "colaborador_nome": "Carlos Mendes"},
            {"colaborador_id": 8, "colaborador_nome": "Ana Souza"},
        ]
        mock_get_client.return_value = {"controle_diario": mock_collection}

        controle = ControleRefeicoes()
        resultado = list(controle.listar_colaboradores_unicos())
        self.assertEqual(len(resultado), 3)

if __name__ == '__main__':
    unittest.main()
