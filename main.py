import os.path
import csv

class Library:
    def __init__(self):
        self.biblioteka_header = ['ID', 'Tytul', 'Autor', 'Rok wydania', 'Status']
        self.historia_header = ['ID', 'Numer czytacza', 'Czy udana', 'Data wypozyczenia', 'Data oddania']
        self.czytacze_header = ['Numer czytacza', 'Imie', 'Nazwisko', 'Ilosc ksiazek']

        self.biblioteka = self.load_csv_file('biblioteka.csv', self.biblioteka_header)
        self.historia = self.load_csv_file('historia.csv', self.historia_header)
        self.czytacze = self.load_csv_file('czytacze.csv', self.czytacze_header)

    def load_csv_file(self, file_name, header):
        data = []
        try:
            if not os.path.isfile(file_name):
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(header)
            with open(file_name, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                data = [row for row in reader]
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania pliku {file_name}: {e}")
        return data
        #W razie gdyby brakowało jakiegoś pliku oraz nie było permisji lub błędne znaki sie wkradły (zapis i odczyt CSV)

    def save_csv_file(self, file_name, data):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(data)
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania pliku {file_name}: {e}")

    def remove_polish_characters(self, text):
        polish_to_ascii = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        return ''.join(polish_to_ascii.get(char, char) for char in text)

    def find_book_by_title_or_id(self, books, search):
        for book in books:
            if len(book) >= 2 and (book[0] == search or book[1].lower() == search.lower()):
                return book
        return None

    def find_reader_by_id_or_name(self, readers, id, first_name, last_name):
        for reader in readers:
            if reader[0] == id or (reader[1].lower() == first_name.lower() and reader[2].lower() == last_name.lower()):
                return reader
        return None

    def add_book(self):
        title = self.remove_polish_characters(input("Podaj tytuł książki: "))
        author = self.remove_polish_characters(input("Podaj autora książki: "))
        year = input("Podaj rok wydania książki: ")

        if len(self.biblioteka) > 1:
            id = max(int(book[0]) for book in self.biblioteka[1:]) + 1
        else:
            id = 1

        new_book = [id, title, author, year, "W bibliotece"]
        self.biblioteka.append(new_book)
        self.save_csv_file('biblioteka.csv', self.biblioteka)

        print("Książka dodana do biblioteki.")
    #W razie gdyby jakies dane nie pasujace do formatu byly podane (liczba - litera)
    def borrow_book(self):
        try:
            search = self.remove_polish_characters(input("Podaj tytuł lub numer indeksu książki: "))
            book = self.find_book_by_title_or_id(self.biblioteka[1:], search)
            reader_id = input("Podaj numer czytacza: ")
            first_name = self.remove_polish_characters(input("Podaj imię: "))
            last_name = self.remove_polish_characters(input("Podaj nazwisko: "))
            if book and book[4] == "W bibliotece":


                date = input("Podaj datę wypożyczenia (dd/mm/yyyy): ")

                reader = self.find_reader_by_id_or_name(self.czytacze[1:], reader_id, first_name, last_name)
                if not reader:
                    new_reader = [reader_id, first_name, last_name, '0']
                    self.czytacze.append(new_reader)
                    self.save_csv_file('czytacze.csv', self.czytacze)
                    reader = new_reader
                    print("Nowy czytacz zapisany w bazie danych.")

                book[4] = "Nie w bibliotece"
                self.save_csv_file('biblioteka.csv', self.biblioteka)

                reader[3] = str(int(reader[3]) + 1)
                self.save_csv_file('czytacze.csv', self.czytacze)

                transaction = [book[0], reader[0], "Tak", date, ""]
                self.historia.append(transaction)
                self.save_csv_file('historia.csv', self.historia)

                print("Książka wypożyczona.")
            else:
                if book:
                    new_reader = [reader_id, first_name, last_name, '0']
                    self.czytacze.append(new_reader)
                    self.save_csv_file('czytacze.csv', self.czytacze)
                    reader = new_reader
                    reader[3] = str(int(reader[3]))
                    self.save_csv_file('czytacze.csv', self.czytacze)
                    print("Nowy czytacz zapisany w bazie danych.")
                    print("Książka jest niedostępna.")
                else:
                    print("Nie znaleziono książki.")

                transaction = [book[0] if book else "", reader_id, "Nie", "", ""]
                self.historia.append(transaction)
                self.save_csv_file('historia.csv', self.historia)

        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def view_book_history(self):
        try:
            search = self.remove_polish_characters(input("Podaj tytuł lub numer indeksu książki: "))
            book = self.find_book_by_title_or_id(self.biblioteka[1:], search)

            if book:
                print("Historia książki:")
                for transaction in self.historia[1:]:
                    if transaction[0] == book[0]:
                        print(
                            f"Numer czytacza: {transaction[1]}, Czy udana: {transaction[2]}, Data wypożyczenia: {transaction[3]}, Data oddania: {transaction[4]}")
            else:
                print("Nie znaleziono książki.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def return_book(self):
        try:
            search = self.remove_polish_characters(input("Podaj tytuł lub numer indeksu książki: "))
            book = self.find_book_by_title_or_id(self.biblioteka[1:], search)
            reader_id = input("Podaj numer czytacza: ")
            first_name = self.remove_polish_characters(input("Podaj imię: "))
            last_name = self.remove_polish_characters(input("Podaj nazwisko: "))
            return_date = input("Podaj datę oddania (dd/mm/yyyy): ")
            reader = self.find_reader_by_id_or_name(self.czytacze[1:], reader_id, first_name, last_name)

            if book and book[4] == "Nie w bibliotece":


                if reader:
                    book[4] = "W bibliotece"
                    self.save_csv_file('biblioteka.csv', self.biblioteka)

                    reader[3] = str(int(reader[3]) - 1)
                    self.save_csv_file('czytacze.csv', self.czytacze)

                    for transaction in self.historia[1:]:
                        if transaction[0] == book[0] and transaction[1] == reader[0] and transaction[4] == "":
                            transaction[4] = return_date
                            self.save_csv_file('historia.csv', self.historia)
                            break

                    print("Książka zwrócona.")
                else:
                    print("Nie znaleziono czytacza.")
            else:
                print("Nie znaleziono książki lub jest dostępna w bibliotece.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")


def main():
    library = Library()
    while True:
        print("Co chcesz zrobić?")
        print("1. Dodaj książkę")
        print("2. Wypożycz książkę")
        print("3. Zobacz historię książki")
        print("4. Zwróć książkę")
        print("5. Wyjdź")

        option = input("Wybierz opcję (1-5): ")

        if option == "1":
            library.add_book()
        elif option == "2":
            library.borrow_book()
        elif option == "3":
            library.view_book_history()
        elif option == "4":
            library.return_book()
        elif option == "5":
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
