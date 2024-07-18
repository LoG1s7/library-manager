import os
import unittest
from unittest.mock import patch

from app.library_manager import Library


class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        """Создание тестовой базы данных"""
        self.test_db_path = "test_data.json"
        with open(self.test_db_path, "w") as f:
            f.write("[]")
        self.library = Library(db_path=self.test_db_path)

    def tearDown(self):
        """Удаление тестовой базы данных"""
        os.remove(self.test_db_path)

    @patch("library_manager.open", create=True)
    def test_add_book(self, mock_open):
        """Тест добавления книги в библиотеку"""
        mock_open.return_value.__enter__.return_value.read.return_value = "[]"
        initial_length = len(self.library.data)
        self.library.add_book("Test Book", "Test Author", 2022)
        new_length = len(self.library.data)
        self.assertEqual(new_length, initial_length + 1)

    @patch("library_manager.open", create=True)
    def test_delete_book(self, mock_open):
        """Тест удаления книги в библиотеку"""
        mock_open.return_value.__enter__.return_value.read.return_value = "[]"
        self.library.add_book("Test Book", "Test Author", 2022)
        initial_length = len(self.library.data)
        self.library.delete_book(1)
        new_length = len(self.library.data)
        self.assertEqual(new_length, initial_length - 1)

    @patch("library_manager.open", create=True)
    def test_search_book(self, mock_open):
        """Тест поиска книги в библиотеке"""
        mock_open.return_value.__enter__.return_value.read.return_value = "[]"
        self.library.add_book("Test Book", "Test Author", 2022)
        found_books = self.library.search_book("Test Author")
        self.assertEqual(len(found_books), 1)

    @patch("library_manager.open", create=True)
    def test_change_status(self, mock_open):
        """Тест изменения статуса книги в библиотеке"""
        mock_open.return_value.__enter__.return_value.read.return_value = "[]"
        self.library.add_book("Test Book", "Test Author", 2022)
        book_id = self.library.data[0]["id"]
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.data[0]["status"], "выдана")


if __name__ == "__main__":
    unittest.main()
