from modules.database import get_connection


connection = get_connection()
cursor = connection.cursor()


# Count students
cursor.execute("SELECT COUNT(*) FROM students")
students = cursor.fetchone()[0]

print("Total Students:", students)


# Count buildings
cursor.execute("SELECT COUNT(*) FROM buildings")
buildings = cursor.fetchone()[0]

print("Total Buildings:", buildings)


# Count exits
cursor.execute("SELECT COUNT(*) FROM exits")
exits = cursor.fetchone()[0]

print("Total Exits:", exits)


# Count assembly points
cursor.execute("SELECT COUNT(*) FROM assembly_points")
assembly_points = cursor.fetchone()[0]

print("Total Assembly Points:", assembly_points)


# Count sensors
cursor.execute("SELECT COUNT(*) FROM sensors")
sensors = cursor.fetchone()[0]

print("Total Sensors:", sensors)


connection.close()