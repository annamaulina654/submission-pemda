import pandas as pd
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

class TestLoad(TestCase):

    def setUp(self):
        self.dummy_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
        self.test_csv_file = "test_output_for_unittest.csv"

    def tearDown(self):
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_load_to_csv_success(self):
        load_to_csv(self.dummy_df, self.test_csv_file)
        
        self.assertTrue(os.path.exists(self.test_csv_file))
        read_df = pd.read_csv(self.test_csv_file)
        pd.testing.assert_frame_equal(read_df, self.dummy_df)

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv_permission_error(self, mock_to_csv):
        mock_to_csv.side_effect = PermissionError("Mocked Permission Error")
        load_to_csv(self.dummy_df, self.test_csv_file)
        self.assertFalse(os.path.exists(self.test_csv_file))

    @patch('utils.load.Credentials')
    @patch('utils.load.build')
    @patch('utils.load.os.path.exists')
    def test_load_to_google_sheets_success(self, mock_exists, mock_build, mock_credentials):
        mock_exists.return_value = True 
        
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        load_to_google_sheets(self.dummy_df, "DUMMY_ID", "dummy_path.json")

        mock_credentials.from_service_account_file.assert_called_once()
        mock_build.assert_called_once()
        mock_service.spreadsheets().values().clear().execute.assert_called_once()
        mock_service.spreadsheets().values().update().execute.assert_called_once()

    @patch('utils.load.os.path.exists')
    def test_load_to_google_sheets_no_creds(self, mock_exists):
        mock_exists.return_value = False 
        load_to_google_sheets(self.dummy_df, "DUMMY_ID", "dummy_path.json")

    @patch('pandas.DataFrame.to_sql')
    @patch('utils.load.create_engine')
    def test_load_to_postgresql_success(self, mock_create_engine, mock_to_sql):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        load_to_postgresql(self.dummy_df, "DUMMY_DB_URL", "dummy_table")

        mock_create_engine.assert_called_with("DUMMY_DB_URL")
        mock_to_sql.assert_called_with(
            "dummy_table", 
            mock_engine, 
            if_exists='replace', 
            index=False
        )

    @patch('utils.load.create_engine')
    def test_load_to_postgresql_exception(self, mock_create_engine):
        mock_create_engine.side_effect = Exception("Mocked DB Connection Error")
        load_to_postgresql(self.dummy_df, "DUMMY_DB_URL", "dummy_table")