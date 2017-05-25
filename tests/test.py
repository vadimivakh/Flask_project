import unittest
from web_app import application


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        application.app.config['TESTING'] = True
        self.app = application.app.get_storage_info()

    def get_storage_info(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'simply' in response.data
        self.assertIn()

    def test_hello_world(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'Hi' in response.data
        #
        # def test_new_product(self):
        #     response = self.app.get('/products/create')
        #     self.assertEqual(response.status_code, 200)
        #     self.assertIn(b'Create new product form', response.data)
        #     self.assertIn(b'Product name', response.data)
        #     self.assertIn(b'Product price', response.data)
        #     self.assertIn(b'Product description', response.data)
        #
        #     product_info = {
        #         'product_name': b'Product 1 Brand',
        #         'product_price': b'12.34',
        #         'product_description': b'ASDF',
        #     }
        #     response = self.app.post('/products/create', data=product_info)
        #
        #     response = self.app.get('/products')
        #     self.assertEqual(response.status_code, 200)
        #     self.assertIn(product_info['product_name'], response.data)
        #     self.assertIn(product_info['product_price'], response.data)
        #     self.assertIn(product_info['product_description'], response.data)


if __name__ == '__main__':
    unittest.main()
