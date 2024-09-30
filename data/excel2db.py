import pandas as pd

def excel_to_sql(file_path, output_file):
    # Read the Excel file
    excel_data = pd.ExcelFile(file_path)
    
    points = []
    stops = []
    routes = []
    unique_points = []  # To keep track of unique points

    # SQL structure creation
    sql_structure = """
CREATE TABLE point (
    _id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE route (
    number INTEGER PRIMARY KEY,
    period TEXT NOT NULL CHECK (period IN ('Univ', 'Univ*', 'Fest*', 'Est', 'Scol')),
    terminus VARCHAR(255) NOT NULL,
    FOREIGN KEY (terminus) REFERENCES point(name)
);

CREATE TABLE stop (
    _id INTEGER PRIMARY KEY,
    point_id INT NOT NULL,
    time TIME,
    route_id INT NOT NULL,
    FOREIGN KEY (point_id) REFERENCES point(_id),
    FOREIGN KEY (route_id) REFERENCES route(_id)
);
"""

    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name, header=None)

        # Extracting points, routes, and periods
        points_list = df.iloc[2:, 0].tolist()
        routes_list = df.iloc[0, 1:].tolist()
        periods_list = df.iloc[1, 1:].tolist()

        # Create points SQL
        for point in points_list:
            if point in unique_points:
                print(f"Point '{point}' already exists in the database. Skipping...")
                continue
            print(f"Adding point '{point}' to the database...")
            unique_points.append(point)
            points.append(f"INSERT INTO point (name) VALUES ('{point}');")

        # Create routes and stops SQL
        for col in range(1, len(routes_list) + 1):
            route_number = routes_list[col - 1]
            period = periods_list[col - 1]
            
            # Find non-null times for each point in this route
            for row in range(2, df.shape[0]):
                time_slot = df.iat[row, col]
                if pd.notna(time_slot) and isinstance(time_slot, str) and ':' in time_slot:
                    point_name = points_list[row - 2]
                    # Find corresponding point_id (assuming order corresponds)
                    point_id = unique_points.index(point_name) + 1
                    print(f"point_id: {point_id} of point_name: {point_name}")
                    # Create stops SQL
                    stops.append(f"INSERT INTO stop (point_id, time, route_id) VALUES ({point_id}, '{time_slot}', {route_number});")
                if row == df.shape[0] - 1:
                    routes.append(f"INSERT INTO route (number, period, terminus) VALUES ('{route_number}', '{period}', '{point_name}');")

    # Combine all SQL statements
    sql_statements = sql_structure + '\n' + '\n'.join(points + stops + routes)

    # Save the SQL statements to a text file
    with open(output_file, 'w') as f:
        f.write(sql_statements)

if __name__ == "__main__":
    excel_to_sql('output.xlsx', 'output.sql')