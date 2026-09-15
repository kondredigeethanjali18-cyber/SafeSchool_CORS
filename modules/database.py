import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "school.db"

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def create_tables():
    """
    Create all required database tables.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            building TEXT NOT NULL,
            status TEXT DEFAULT 'safe'
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buildings (
            building_id INTEGER PRIMARY KEY,
            building_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exits (
            exit_id INTEGER PRIMARY KEY,
            exit_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT DEFAULT 'open'
        )
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assembly_points (
            assembly_id INTEGER PRIMARY KEY,
            assembly_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            capacity INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id INTEGER PRIMARY KEY,
            sensor_type TEXT NOT NULL,
            sensor_name TEXT NOT NULL,
            building TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            status TEXT DEFAULT 'normal'
        )
    """)

    connection.commit()
    connection.close()


def add_sample_data():
    """
    Insert sample school data for our prototype.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]

    if student_count == 0:

        student_id = 1

        buildings = {
            "Block A": ["8-A", "8-B", "9-A"],
            "Block B": ["9-B", "10-A", "10-B"],
            "Block C": ["7-A", "7-B"]
        }

        for building, classes in buildings.items():

            for class_name in classes:
                for number in range(1, 21):

                    student_name = f"Student {student_id}"

                    cursor.execute("""
                        INSERT INTO students
                        (student_id, student_name, class_name, building, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        student_id,
                        student_name,
                        class_name,
                        building,
                        "safe"
                    ))

                    student_id += 1

    cursor.execute("SELECT COUNT(*) FROM buildings")

    if cursor.fetchone()[0] == 0:

        buildings_data = [
            (1, "Block A", 17.3850, 78.4867),
            (2, "Block B", 17.3855, 78.4872),
            (3, "Block C", 17.3847, 78.4875)
        ]

        cursor.executemany("""
            INSERT INTO buildings
            (building_id, building_name, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, buildings_data)

    cursor.execute("SELECT COUNT(*) FROM exits")

    if cursor.fetchone()[0] == 0:

        exits_data = [
            (1, "Exit A", 17.3858, 78.4864, "open"),
            (2, "Exit B", 17.3845, 78.4862, "open"),
            (3, "Exit C", 17.3843, 78.4878, "open")
        ]

        cursor.executemany("""
            INSERT INTO exits
            (exit_id, exit_name, latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?)
        """, exits_data)

    cursor.execute("SELECT COUNT(*) FROM assembly_points")

    if cursor.fetchone()[0] == 0:

        assembly_data = [
            (1, "Assembly Point A", 17.3862, 78.4865, 150),
            (2, "Assembly Point B", 17.3840, 78.4868, 150),
            (3, "Assembly Point C", 17.3841, 78.4882, 100)
        ]

        cursor.executemany("""
            INSERT INTO assembly_points
            (assembly_id, assembly_name, latitude, longitude, capacity)
            VALUES (?, ?, ?, ?, ?)
        """, assembly_data)

    cursor.execute("SELECT COUNT(*) FROM sensors")

    if cursor.fetchone()[0] == 0:

        sensors_data = [
            (
                1,
                "fire",
                "Fire Sensor A1",
                "Block A",
                17.3851,
                78.4868,
                "normal"
            ),
            (
                2,
                "smoke",
                "Smoke Sensor B1",
                "Block B",
                17.3856,
                78.4873,
                "normal"
            ),
            (
                3,
                "water",
                "Water Sensor C1",
                "Block C",
                17.3848,
                78.4876,
                "normal"
            )
        ]

        cursor.executemany("""
            INSERT INTO sensors
            (sensor_id, sensor_type, sensor_name, building,
             latitude, longitude, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sensors_data)

    connection.commit()
    connection.close()