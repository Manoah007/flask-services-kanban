import unittest
from app import app

class TestService3(unittest.TestCase):
    def setUp(self):
        # On crée un client de test virtuel pour Flask
        self.client = app.test_client()
        self.client.testing = True

    def test_route_describe_succes(self):
        # On simule une requête GET sur la route describe
        reponse = self.client.get('/db/stats/describe?serie=serie_A')
        # On vérifie que le code HTTP est bien 200 (OK)
        self.assertEqual(reponse.status_code, 200)
        # On vérifie que le mot 'moyenne' est dans la réponse
        self.assertIn(b'moyenne', reponse.data)

    def test_route_describe_erreur(self):
        # On teste avec une série qui n'existe pas
        reponse = self.client.get('/db/stats/describe?serie=serie_fantome')
        # On s'attend à une erreur 404
        self.assertEqual(reponse.status_code, 404)

    def test_route_correlation(self):
        # On simule une requête sur la corrélation
        reponse = self.client.get('/db/stats/correlation?serie_x=serie_A&serie_y=serie_B')
        self.assertEqual(reponse.status_code, 200)

if __name__ == '__main__':
    unittest.main()