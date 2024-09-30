import pdfplumber
import pandas as pd

def excel():
    with pdfplumber.open("pdf/omg.pdf") as pdf:
        tables = []
        n = 1
        for page in pdf.pages:
            print("Page", n, "out of 28")
            n += 1

            table = page.extract_table()

            # if the table does not contain "Fermata" in the first row, add it to the previous table
            if table and "FERMATE" in table[0]:
                tables.append(table)
            elif tables:
                # add an empty col to table starting from col 1
                for row in table:
                    row.insert(1, "")
                tables[-1].extend(table)
        
        with pd.ExcelWriter("output.xlsx") as writer:
            for i, table in enumerate(tables):
                # Convert the table to a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                
                # if the table has "N° Corsa" in the headers, remove second col and third and fourth row
                if "N° Corsa" in df.columns:
                    df = df.drop(columns=df.columns[1])
                    # write "Periodo" in the second row of the first column
                    df.iloc[0, 0] = "Periodo"
                    # drop row 2 and 3
                    df = df.drop([1, 2])
                    #df = df.drop([2, 3])

                # if any cell contains "00:00", check if the cell below contains an earlier hour, if it does then make the current cell empty
                for col in df.columns:
                    for k in range(1, len(df[col]) - 1):  # Ensure we don't go out of bounds
                        if df.iloc[k][col] == "00:00":
                            if df.iloc[k + 1][col] > df.iloc[k][col]:
                                df.iloc[k][col] = "-"
                
                # Save each DataFrame as a separate sheet
                df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)

def database():
    # create the database
    import sqlite3
    conn = sqlite3.connect("output.db")
    c = conn.cursor()

    # create the tables
    c.execute("""
    CREATE TABLE point (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE stop (
        id INTEGER PRIMARY KEY,
        point_id INTEGER,
        time TEXT,
        route_id INTEGER,
        FOREIGN KEY (point_id) REFERENCES point(id),
        FOREIGN KEY (route_id) REFERENCES route(id)
    )
    """)

    c.execute("""
    CREATE TABLE route (
        id INTEGER PRIMARY KEY,
        number INTEGER,
        period TEXT
    )
    """)

    # read the excel file
    df = pd.read_excel("output.xlsx", sheet_name=None, engine='openpyxl')

    # insert the data into the tables
    for sheet_name, data in df.items():
        if "N° Corsa" in data.columns:
            for _, row in data.iterrows():
                # Insert into route table
                c.execute("INSERT INTO route (number, period) VALUES (?, ?)", (row["N° Corsa"], row["Periodo"]))
                route_id = c.lastrowid

                # Insert into point and stop tables
                for i in range(2, len(row), 2):
                    point_name = row.index[i]
                    stop_time = row[i]

                    # Insert into point table
                    c.execute("INSERT INTO point (name) VALUES (?)", (point_name,))
                    point_id = c.lastrowid

                    # Insert into stop table
                    c.execute("INSERT INTO stop (point_id, time, route_id) VALUES (?, ?, ?)", (point_id, stop_time, route_id))

    # commit the changes
    conn.commit()

    # close the connection
    conn.close()

if __name__ == "__main__":
    excel()