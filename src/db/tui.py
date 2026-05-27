from .backend.memory import bd_of_student
from .backend.errors import InvalidAgeError, DuplicateIDError


class StudentUI:

    def __init__(self):
        self.table = bd_of_student()

    def _print_menu(self) -> None:
        print("\n[ СИСТЕМА УПРАВЛЕНИЯ СТУДЕНТАМИ ]")
        print("1 - Внести новую запись")
        print("2 - Вывести все записи")
        print("3 - Поиск записей по критериям")
        print("4 - Редактировать запись")
        print("5 - Удалить запись")
        print("6 - Упорядочить записи")
        print("0 - Завершить работу")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Неверный ввод: требуется целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Неверный ввод: требуется целое число или пустая строка.")

    def _read_optional_str(self, prompt: str) -> str | None:
        raw = input(prompt).strip()
        return raw if raw else None

    def _print_records(self, records: list[tuple]) -> None:
        if not records:
            print("Список пуст. Ничего не найдено.")
            return

        for i, record in enumerate(records):
            print(f"[{i}] {record}")

    def _add_record(self) -> None:
        print("\n--- Добавление новой записи ---")

        student_id = self._read_int("Идентификатор: ")
        first_name = input("Имя: ").strip()
        second_name = input("Фамилия: ").strip()
        age = self._read_int("Возраст: ")
        sex = input("Пол: ").strip()

        try:
            record = self.table.create_rec(
                student_id, first_name, second_name, age, sex
            )
            print(f"Успешно добавлено: {record}")
        except (InvalidAgeError, DuplicateIDError) as exc:
            print(f"Операция прервана: {exc}")

    def _show_all(self) -> None:
        print("\n--- Все записи в базе ---")
        records = self.table.get_all_rec()
        self._print_records(records)

    def _find_records(self) -> None:
        print("\n--- Поиск по атрибутам ---")
        print("(Нажмите Enter чтобы пропустить условие)")

        student_id = self._read_optional_int("ID: ")
        first_name = self._read_optional_str("Имя: ")
        second_name = self._read_optional_str("Фамилия: ")
        age = self._read_optional_int("Возраст: ")
        sex = self._read_optional_str("Пол: ")

        records = self.table.select_rec(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            sex=sex,
        )

        print(f"\nРезультатов по заданным критериям: {len(records)}")
        self._print_records(records)
        return records

    def _update_record(self) -> None:
        print("\n--- Редактирование существующей записи ---")

        all_records = self.table.get_all_rec()
        if not all_records:
            print("База данных пуста. Нечего редактировать.")
            return

        self._print_records(all_records)
        index = self._read_int("Укажите номер записи для изменения: ")

        if index >= len(all_records):
            print("Ошибка: запись под указанным номером отсутствует.")
            return

        print("\nВведите новые данные (оставьте поле пустым чтобы не менять):")
        first_name = self._read_optional_str(
            f"Имя (сейчас: {all_records[index][1]}): "
        )
        second_name = self._read_optional_str(
            f"Фамилия (сейчас: {all_records[index][2]}): "
        )
        age = self._read_optional_int(f"Возраст (сейчас: {all_records[index][3]}): ")
        sex = self._read_optional_str(f"Пол (сейчас: {all_records[index][4]}): ")

        try:
            self.table.update_rec(index, first_name, second_name, age, sex)
            print("Изменения успешно применены.")
        except IndexError as exc:
            print(f"Не удалось обновить: {exc}")

    def _delete_record(self) -> None:
        print("\n--- Удаление записи ---")

        all_records = self.table.get_all_rec()
        if not all_records:
            print("В базе нет записей для удаления.")
            return

        self._print_records(all_records)
        index = self._read_int("Введите номер записи которую хотите удалить: ")

        if index >= len(all_records):
            print("Ошибка: указанная запись не существует.")
            return

        confirm = input("Подтвердите удаление (y/n): ").strip().lower()
        if confirm == "y":
            try:
                self.table.delete_rec(index)
                print("Запись была удалена из базы.")
            except IndexError as exc:
                print(f"Не удалось удалить: {exc}")
        else:
            print("Операция удаления отменена пользователем.")

    def _sort_records(self) -> None:
        print("\n--- Упорядочивание записей ---")
        print("Поля для сортировки: id, first_name, second_name, age, sex")

        field = input("Укажите поле для сортировки: ").strip().lower()
        reverse_input = input("Сортировать в обратном порядке? (y/n): ").strip().lower()
        reverse = reverse_input == "y"

        try:
            sorted_records = self.table.sort_rec(field, reverse)
            direction = "убыванию" if reverse else "возрастанию"
            print(f"\nОтсортированные данные (поле: '{field}', направление: {direction}):")
            self._print_records(sorted_records)
        except ValueError as exc:
            print(f"Ошибка при сортировке: {exc}")

    def run(self) -> None:
        while True:
            self._print_menu()
            action = input("Ваш выбор: ").strip()

            if action == "1":
                self._add_record()
            elif action == "2":
                self._show_all()
            elif action == "3":
                self._find_records()
            elif action == "4":
                self._update_record()
            elif action == "5":
                self._delete_record()
            elif action == "6":
                self._sort_records()
            elif action == "0":
                print("Работа завершена. До свидания.")
                break
            else:
                print("Неизвестная команда. Пожалуйста, выберите пункт из меню.")


def run() -> None:
    app = StudentUI()
    app.run()


if __name__ == "__main__":
    run()