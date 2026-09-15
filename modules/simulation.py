import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "school.db"


class EvacuationSimulator:

    def __init__(self):
        """
        Create a new evacuation simulator.
        """

        self.students = []
        self.elapsed_seconds = 0
        self.disaster_active = False
        self.disaster_type = None
        self.affected_building = None

        self.load_students()


    def load_students(self):
        """
        Load students from the SQLite database.
        """

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                student_name,
                class_name,
                building
            FROM students
        """)

        rows = cursor.fetchall()

        connection.close()

        self.students = []

        for row in rows:

            student = {
                "student_id": row[0],
                "student_name": row[1],
                "class_name": row[2],
                "building": row[3],
                "status": "safe"
            }

            self.students.append(student)


    def start_disaster(self, disaster_type, affected_building):
        """
        Start an evacuation simulation.
        """

        self.disaster_active = True
        self.disaster_type = disaster_type
        self.affected_building = affected_building
        self.elapsed_seconds = 0

        # Students in the affected building begin moving.
        for student in self.students:

            if student["building"] == affected_building:
                student["status"] = "moving"

            else:
                student["status"] = "safe"


    def advance(self, seconds=5):
        """
        Move the simulation forward by a given number of seconds.
        """

        if not self.disaster_active:
            return

        self.elapsed_seconds += seconds

        affected_students = [
            student
            for student in self.students
            if student["building"] == self.affected_building
        ]

        for student in affected_students:

            student_id = student["student_id"]

            if self.elapsed_seconds >= 30:
                student["status"] = "safe"

            elif self.elapsed_seconds >= 20:

                if student_id % 3 != 0:
                    student["status"] = "safe"
                else:
                    student["status"] = "moving"

            elif self.elapsed_seconds >= 10:

                if student_id % 4 == 0:
                    student["status"] = "safe"
                else:
                    student["status"] = "moving"

            else:
                student["status"] = "moving"

            if student_id % 17 == 0 and self.elapsed_seconds >= 15:
                student["status"] = "missing"

    def get_counts(self):
        """
        Return the current number of students in each state.
        """

        total = len(self.students)

        safe = sum(
            1
            for student in self.students
            if student["status"] == "safe"
        )

        moving = sum(
            1
            for student in self.students
            if student["status"] == "moving"
        )

        missing = sum(
            1
            for student in self.students
            if student["status"] == "missing"
        )

        return {
            "total": total,
            "safe": safe,
            "moving": moving,
            "missing": missing
        }

    def get_students(self):
        """
        Return the current student states.
        """

        return self.students