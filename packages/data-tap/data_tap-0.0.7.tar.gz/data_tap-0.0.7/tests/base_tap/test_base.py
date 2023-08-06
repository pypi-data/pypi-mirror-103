import unittest

from data_tap.base_tap import BaseTap


class TestBaseTap(unittest.TestCase):

    def test_return_json(self):
        base_tap = BaseTap(
            creds_file='tests/fixtures/mock_file.json',
            config_file='tests/fixtures/mock_file.json'
        )

        self.assertEqual(base_tap.creds, {'id_secret': '12345', 'id_key': '!1abc0'})
        self.assertEqual(base_tap.config, {'id_secret': '12345', 'id_key': '!1abc0'})

    def test_return_csv(self):
        base_tap = BaseTap(
            creds_file='tests/fixtures/mock_file.csv',
            config_file='tests/fixtures/mock_file.csv'
        )

        self.assertEqual(base_tap.creds, {'id_secret': 12345, 'id_key': '!1abc0'})
        self.assertEqual(base_tap.config, {'id_secret': 12345, 'id_key': '!1abc0'})

    def test_return_yaml(self):
        base_tap = BaseTap(
            creds_file='tests/fixtures/mock_file.yaml',
            config_file='tests/fixtures/mock_file.yaml'
        )

        self.assertEqual(base_tap.creds, {'id_secret': '12345', 'id_key': '!1abc0'})
        self.assertEqual(base_tap.config, {'id_secret': '12345', 'id_key': '!1abc0'})

    def test_return_yml(self):
        base_tap = BaseTap(
            creds_file='tests/fixtures/mock_file.yml',
            config_file='tests/fixtures/mock_file.yml'
        )

        self.assertEqual(base_tap.creds, {'id_secret': '12345', 'id_key': '!1abc0'})
        self.assertEqual(base_tap.config, {'id_secret': '12345', 'id_key': '!1abc0'})


if __name__ == '__main__':
    unittest.main()
