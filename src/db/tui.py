
from .backend.memory import (
    create_rec,
    select_rec,
    update_rec,
    delete_rec,
    create_db,
    delete_db,
    return_this_Base,
    get_temp,
)


def read_values(temp: list[str]) -> list:
    values = []
    print("\nВведите значения для полей:")
    for i in range(len(temp)):
        value = input(f"{temp[i]}: ").strip()
        values.append(value)
    return values


def reading_filters(temp: list[str]) -> list:
    print("\nВведите фильтры (Enter = пропустить поле):")
    filters = [None] * len(temp)
    for i in range(len(temp)):
        value = input(f"{temp[i]}: ").strip()
        filters[i] = value if value != "" else None
    return filters


def print_menu_for_many_bases() -> None:
    print("\n ------- Управление базами -------")
    print("1. Создать новую таблицу")
    print("2. Показать все таблицы")
    print("3. Удалить таблицу")
    print("0. Выход")


def _print_menu() -> None:
    print("\n ------- База студентов -------")
    print("1. Добавить студента")
    print("2. Показать всех студентов")
    print("3. Найти студента по фильтру")
    print("0. Выход")


def print_menu_stud() -> None:
    print("\n1. Обновить запись")
    print("2. Удалить запись")
    print("0. Выход")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:

            return int(raw)
        except ValueError:
            print("Ошибка! Введите любо целое число.")


def _add_student(number_of_base, temp) -> None:
    print("\nДобавление стуента")

    values = read_values(temp)

    try:
        
        record = create_rec(number_of_base, values)

        
        print(f"Запись добавлена: {record}")

    except ValueError as exc:
        
        print(f"Ошибка: {exc}")



def print_records(records: list[tuple], flag=True, temp=None) -> None:
    
    if not records:
        print("Студенты не найдены.")
        return

    
    if flag:
        for record in records:
            print(record)
    else:
        print("\nСписок подходящих записей")
        for i in range(len(records)):
            print(str(i) + ".", records[i])


def _show_all_students(number_of_base) -> None:
    print("\nСписок записей")
    print_records(select_rec(number_of_base))


def show_all_bases() -> None:
    print("\nСписок баз")
    Bases = return_this_Base()
    if not Bases:
        print("Записи не найдены.")
        return
    for i in range(len(Bases)):
        print(str(i) + ".", Bases[i][0], f"(колонки: {Bases[i][1]})")


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")

def find_students_by_filter(number_of_base, temp) -> list:
    print("\nПоиск по фильтру")

    filters = reading_filters(temp)

    records = select_rec(number_of_base, filters=filters)

    print_records(records, False)
    return records


def update_student(number_of_base, records, n=0, temp=None) -> None:
    print("\nОбновление информации (Enter = пропустить поле)")

    if n >= len(records):
        print("Ошибка: выбранного студента нет в списке")
        return

    old_record = records[n]
    new_values = [None] * len(temp)

    print(f"Текущая запись: {old_record}")
    print("Введите новые значения (Enter = оставить без изменений):")

    for i in range(len(temp)):
        value = input(f"{temp[i]} (текущее: {old_record[i]}): ").strip()
        new_values[i] = value if value != "" else None

    
    if all(v is None for v in new_values):
        print("Нет изменений для сохранения.")
        return

    all_records = select_rec(number_of_base)
    i = 0
    for rec in all_records:
        if rec == old_record:
            update_rec(number_of_base, i, new_values)
            break
        i += 1
    print("\nДанные успешно изменены")


def delete_this_student(number_of_base, records, n=0) -> None:
    if delete_rec(number_of_base, records, n):
        print("\nСтудент успешно удален")
    else:
        print("\nОшибка: не удалось удалить студента")


def run() -> None:
    while True:
        print_menu_for_many_bases()
        action_base = input("Выберите действие: ").strip()

        if action_base == "1":
            print("Введите название для базы")
            name = input().strip()
            print("Введите имена колонок через запятую (например: id,name,age)")
            print("Первая колонка будет использоваться как идентификатор")
            columns_input = input().strip()
            temp = [col.strip() for col in columns_input.split(",")]
            if temp:
                create_db(name, temp)
                print(f"База '{name}' создана с колонками: {temp}")
            else:
                print("Ошибка: нужно указать хотя бы одну колонку")

        elif action_base == "2":
            show_all_bases()
            Bases = return_this_Base()
            if len(Bases) > 0:
                print("Выберите базу для работы (-1 для выход в меню)")
                number_of_base = 0
                while True:
                    try:
                        number_of_base = int(input())
                    except ValueError:
                        number_of_base = "!"
                    if number_of_base == "!" or number_of_base < -1:
                        print("Ошибка повторите ввод")
                    else:
                        break
                if number_of_base != -1 and number_of_base < len(Bases):
                    temp = get_temp(number_of_base)
                    while True:
                       
                        _print_menu()

                        action = input("Выберите действие: ").strip()

                        if action == "1":
                            _add_student(number_of_base, temp)

                        elif action == "2":
                            _show_all_students(number_of_base)

                        elif action == "3":
                            result = find_students_by_filter(number_of_base, temp)
                            print_menu_stud()
                            while True:
                                subaction = input("Выберите действие: ").strip()
                                if subaction == "0":
                                    break
                                elif subaction == "1" or subaction == "2":
                                    n = 0
                                    if len(result) > 1:
                                        while True:
                                            try:
                                                n = int(
                                                    input(
                                                        "Выберите номер студента из списка выше: "
                                                    ).strip()
                                                )
                                            except ValueError:
                                                n = len(result)
                                            if n >= len(result):
                                                print(
                                                    "Такого студента нет в списке.  Повторите ввод"
                                                )
                                            else:
                                                break
                                    if subaction == "1":
                                        update_student(number_of_base, result, n, temp)
                                    else:
                                        delete_this_student(number_of_base, result, n)

                                    result = select_rec(number_of_base, filters=[])
                                    break
                                else:
                                    print("Неизвестная команда. Повторите ввод.")
                        elif action == "0":
                            print("Выход из программы.")
                            break

                        else:
                            print("Неизвестная команда. Повторите ввод.")
            else:
                print("Нет доступных баз")

        elif action_base == "3":
            show_all_bases()
            Bases = return_this_Base()
            if len(Bases) > 0:
                print("Введите номер базы для удаления")
                while True:
                    try:
                        n = int(input())
                    except ValueError:
                        n = "!"
                    if n == "!" or n >= len(Bases):
                        print("Ошибка повторите ввод")
                    else:
                        break
                delete_db(n)
            else:
                print("Баз для удаления нету")
        elif action_base == "0":
            break
        else:
            print("Неизвестная команда. Повторите ввод.")
