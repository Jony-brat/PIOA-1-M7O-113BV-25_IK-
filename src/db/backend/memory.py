from .errors import DuplicateIDError, InvalidAgeError

type Student_Rec = tuple[int, str, str, int, str]

class bd_of_student:
    def __init__(self) -> None:
        self._student: list[Student_Rec] = []

    def create_rec(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> Student_Rec:

        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if any(record[0] == student_id for record in self._student):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record: Student_Rec = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self._student.append(new_record)
        return new_record

    def select_rec(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[Student_Rec]:

        if (
            student_id is None
            and first_name is None
            and second_name is None
            and age is None
            and sex is None
        ):
            return self._student.copy()

        result: list[Student_Rec] = []

        for record in self._student:
            if student_id is not None and record[0] != student_id:
                continue

            if first_name is not None and record[1] != first_name:
                continue

            if second_name is not None and record[2] != second_name:
                continue

            if age is not None and record[3] != age:
                continue

            if sex is not None and record[4] != sex:
                continue

            result.append(record)

        return result

    def update_rec(
        self,
        record_index: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> None:
        if record_index >= len(self._student):
            raise IndexError(f"Запись с индексом {record_index} не существует.")
        old_record = self._student[record_index]
        new_record = (
            old_record[0],
            first_name.strip() if first_name is not None else old_record[1],
            second_name.strip() if second_name is not None else old_record[2],
            age if age is not None else old_record[3],
            sex.strip() if sex is not None else old_record[4],
        )
        self._student[record_index] = new_record

    def delete_rec(self, record_index: int) -> None:
        if record_index >= len(self._student):
            raise IndexError(f"Запись с индексом {record_index} не существует.")

        self._student.pop(record_index)

    def sort_rec(self, field: str, reverse: bool = False) -> list[Student_Rec]:
        field_map = {"id": 0, "first_name": 1, "second_name": 2, "age": 3, "sex": 4}

        if field not in field_map:
            raise ValueError(f"Некорректное поле для сортировки: {field}")

        return sorted(self._student, key=lambda x: x[field_map[field]], reverse=reverse)

    def get_all_rec(self) -> list[Student_Rec]:
        return self._student.copy()

    def __len__(self) -> int:
        return len(self._student)
