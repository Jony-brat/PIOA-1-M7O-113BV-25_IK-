import unittest
from src.db.backend.memory import bd_of_student
from src.db.backend.errors import InvalidAgeError, DuplicateIDError


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.student_table = bd_of_student()
        self.assertIsInstance(self.student_table, bd_of_student)

    def test_student_table_allocation(self):
        student_table = bd_of_student()
        self.assertIsInstance(student_table, bd_of_student)

    def test_create_record(self):
        cases = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
            (3, "Екатерина", "Сидорова", 19, "F"),
            (4, "Дмитрий", "Кузнецов", 21, "M"),
            (5, "Сергей", "Смирнов", 18, "M"),
            (6, "Анна", "Васильева", 23, "F"),
        ]

        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.student_table.create_rec(*test_data)
                self.assertEqual(record, test_data)

    def test_create_record_negative_age(self):
        cases = [
            (1, "Алексей", "Иванов", -1, "M"),
            (2, "Мария", "Петрова", -5, "F"),
            (3, "Екатерина", "Сидорова", -10, "F"),
        ]
        error_message = "Поле age не может быть отрицательным."

        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidAgeError) as context:
                    self.student_table.create_rec(*test_data)
                self.assertEqual(str(context.exception), error_message)

    def test_create_record_duplicate_id(self):
        test_data_1 = (1, "Алексей", "Иванов", 20, "M")
        test_data_2 = (1, "Мария", "Петрова", 22, "F")
        error_message = "Запись с id=1 уже существует."

        self.student_table.create_rec(*test_data_1)

        with self.assertRaises(DuplicateIDError) as context:
            self.student_table.create_rec(*test_data_2)

        self.assertEqual(str(context.exception), error_message)

    def test_select_record_no_filters(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        records = self.student_table.select_rec()
        self.assertEqual(records, test_datas)

    def test_select_record_by_id(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
            (3, "Екатерина", "Сидорова", 19, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        records = self.student_table.select_rec(student_id=2)
        self.assertEqual(records, [test_datas[1]])

    def test_select_record_by_name(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
            (3, "Алексей", "Смирнов", 19, "M"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        records = self.student_table.select_rec(first_name="Алексей")
        self.assertEqual(records, [test_datas[0], test_datas[2]])

    def test_select_record_by_age(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 20, "F"),
            (3, "Екатерина", "Сидорова", 19, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        records = self.student_table.select_rec(age=20)
        self.assertEqual(records, [test_datas[0], test_datas[1]])

    def test_select_record_combined_filters(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Алексей", "Петров", 20, "M"),
            (3, "Екатерина", "Иванова", 20, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        records = self.student_table.select_rec(first_name="Алексей", second_name="Иванов")
        self.assertEqual(records, [test_datas[0]])

    def test_update_record(self):
        self.student_table.create_rec(1, "Алексей", "Иванов", 20, "M")

        self.student_table.update_rec(0, first_name="Александр", age=21)

        records = self.student_table.select_rec()
        self.assertEqual(records[0][1], "Александр")
        self.assertEqual(records[0][3], 21)
        self.assertEqual(records[0][0], 1)

    def test_update_record_invalid_index(self):
        with self.assertRaises(IndexError):
            self.student_table.update_rec(0, first_name="Алексей")

    def test_delete_record(self):
        self.student_table.create_rec(1, "Алексей", "Иванов", 20, "M")
        self.student_table.create_rec(2, "Мария", "Петрова", 22, "F")

        self.student_table.delete_rec(0)

        self.assertEqual(len(self.student_table), 1)
        records = self.student_table.select_rec()
        self.assertEqual(records[0][0], 2)

    def test_delete_record_invalid_index(self):
        with self.assertRaises(IndexError):
            self.student_table.delete_rec(0)

    def test_sort_records_by_id(self):
        test_datas = [
            (3, "Екатерина", "Сидорова", 19, "F"),
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        sorted_records = self.student_table.sort_rec("id")
        self.assertEqual(sorted_records[0][0], 1)
        self.assertEqual(sorted_records[1][0], 2)
        self.assertEqual(sorted_records[2][0], 3)

    def test_sort_records_by_age_descending(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
            (3, "Екатерина", "Сидорова", 19, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        sorted_records = self.student_table.sort_rec("age", reverse=True)
        self.assertEqual(sorted_records[0][3], 22)
        self.assertEqual(sorted_records[1][3], 20)
        self.assertEqual(sorted_records[2][3], 19)

    def test_sort_records_by_name(self):
        test_datas = [
            (1, "Дмитрий", "Кузнецов", 18, "M"),
            (2, "Анна", "Васильева", 19, "F"),
            (3, "Борис", "Соколов", 20, "M"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        sorted_records = self.student_table.sort_rec("first_name")
        self.assertEqual(sorted_records[0][1], "Анна")
        self.assertEqual(sorted_records[1][1], "Борис")
        self.assertEqual(sorted_records[2][1], "Дмитрий")

    def test_sort_records_invalid_field(self):
        with self.assertRaises(ValueError):
            self.student_table.sort_rec("invalid_field")

    def test_len_method(self):
        self.assertEqual(len(self.student_table), 0)

        self.student_table.create_rec(1, "Алексей", "Иванов", 20, "M")
        self.assertEqual(len(self.student_table), 1)

        self.student_table.create_rec(2, "Мария", "Петрова", 22, "F")
        self.assertEqual(len(self.student_table), 2)

    def test_get_all_records(self):
        test_datas = [
            (1, "Алексей", "Иванов", 20, "M"),
            (2, "Мария", "Петрова", 22, "F"),
        ]

        for test_data in test_datas:
            self.student_table.create_rec(*test_data)

        all_records = self.student_table.get_all_rec()
        self.assertEqual(all_records, test_datas)

        # Проверка что возвращается копия
        all_records.append((3, "Екатерина", "Сидорова", 19, "F"))
        self.assertEqual(len(self.student_table), 2)

    def test_update_record_invalid_index_message(self):
        with self.assertRaises(IndexError) as context:
            self.student_table.update_rec(0, first_name="Алексей")
        self.assertIn("не существует", str(context.exception))

    def test_delete_record_invalid_index_message(self):
        with self.assertRaises(IndexError) as context:
            self.student_table.delete_rec(0)
        self.assertIn("не существует", str(context.exception))


if __name__ == "__main__":
    unittest.main()