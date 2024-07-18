import json
from typing import Dict, List, Union

# Определение типов
Book = Dict[str, Union[int, str]]
BooksList = List[Book]


class Library:
    """Класс для управления книгами в библиотеке"""

    def __init__(self, db_path="library_data.json"):
        self.db_path = db_path
        self.data = self.load_data()

    def load_data(self):
        """Функция для загрузки данных из файла JSON"""
        try:
            with open(self.db_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save_data(self):
        """Функция для сохранения данных в файл JSON"""
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int):
        """Функция для добавления книги"""
        book: Book = {
            "id": len(self.data) + 1,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии",
        }
        self.data.append(book)
        self.save_data()
        print("Книга успешно добавлена.")

    def delete_book(self, book_id: int):
        """Функция для удаления книги по id"""
        for book in self.data[:]:
            if book["id"] == book_id:
                self.data.remove(book)
                self.save_data()
                print("Книга успешно удалена.")
                return
        print("Книга с указанным id не найдена.")

    def search_book(self, criteria: str) -> BooksList:
        """
        Функция для поиска книги по различным критериям (title, author, year)
        """
        found_books: BooksList = []
        for book in self.data:
            if (
                criteria.lower() in book["title"].lower()
                or criteria.lower() in book["author"].lower()
                or criteria == str(book["year"])
            ):
                found_books.append(book)
        return found_books

    def display_all_books(self):
        """Функция для отображения всех книг"""
        for book in self.data:
            print(
                f"ID: {book['id']} | Название: {book['title']} | "
                f"Автор: {book['author']} | Год: {book['year']} | "
                f"Статус: {book['status']}"
            )

    def change_status(self, book_id: int, new_status: str):
        """Функция для изменения статуса книги по id"""
        for book in self.data:
            if book["id"] == book_id:
                book["status"] = new_status
                self.save_data()
                print("Статус книги успешно изменен.")
                return
        print("Книга с указанным id не найдена.")


library = Library()

if __name__ == "__main__":
    while True:
        print(
            "\nМеню:"
            "\n1. Добавить книгу"
            "\n2. Удалить книгу"
            "\n3. Найти книгу"
            "\n4. Показать все книги"
            "\n5. Изменить статус книги"
            "\n6. Выход"
        )

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)

        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("Введите корректный ID книги.")

        elif choice == "3":
            criteria = input("Введите название, автора или год издания: ")
            found_books = library.search_book(criteria)
            if found_books:
                for book in found_books:
                    print(
                        f"Найденная книга: {book['title']} | {book['author']}"
                        f" | {book['year']} | {book['status']}"
                    )
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_all_books()

        elif choice == "5":
            try:
                book_id = int(
                    input("Введите ID книги для изменения статуса: ")
                )
                new_status = input("Введите новый статус (в наличии/выдана): ")
                if (
                    new_status.lower() == "в наличии"
                    or new_status.lower() == "выдана"
                ):
                    library.change_status(book_id, new_status)
                else:
                    print("Статус должен быть 'в наличии' или 'выдана'.")
            except ValueError:
                print("Введите корректный ID книги и статус.")

        elif choice == "6":
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")
