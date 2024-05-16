import mysql.connector

def CheckCredentials(username, password):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Check if the provided credentials are for the admin
        if (username == "bob" and password == "bob") or (username == "kevin" and password == "kevin") or (username == "sorunlubirarkadas" and password == "muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine"):
            return 1  # Admin

        # Execute a SQL query to check the credentials for players
        query = "SELECT username FROM Player WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            return 2  # Player

        # Execute a SQL query to check the credentials for coaches
        query = "SELECT username FROM Coach WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            return 3  # Coach

        # Execute a SQL query to check the credentials for jury members
        query = "SELECT username FROM Jury WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            return 4  # Jury

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # If no match is found, return 0
        return 0  # Credentials not found

    except mysql.connector.Error as error:
        print("Error:", error)
        return 0  # Error occurred