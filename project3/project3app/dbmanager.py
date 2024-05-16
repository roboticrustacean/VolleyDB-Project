import mysql.connector

def add_player(username, password, name, surname, date_of_birth, height, weight):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()
        # Prepare the INSERT statement
        add_player_query = ("INSERT INTO Player "
                            "(username, password, name, surname, date_of_birth, height, weight) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        # Execute the INSERT statement
        player_data = (username, password, name, surname, date_of_birth, height, weight)
        cursor.execute(add_player_query, player_data)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True  # Return True if player is added successfully

    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False if an error occurs

def add_coach(username, password, name, surname, nationality):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()
        # Prepare the INSERT statement
        add_coach_query = ("INSERT INTO Coach "
                            "(username, password, name, surname, nationality) "
                            "VALUES (%s, %s, %s, %s, %s)")

        # Execute the INSERT statement
        coach_data = (username, password, name, surname, nationality)
        cursor.execute(add_coach_query, coach_data)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True  # Return True if player is added successfully

    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False if an error occurs

def add_jury(username, password, name, surname, nationality):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()
        # Prepare the INSERT statement
        add_jury_query = ("INSERT INTO Jury "
                            "(username, password, name, surname, nationality) "
                            "VALUES (%s, %s, %s, %s, %s)")

        # Execute the INSERT statement
        jury_data = (username, password, name, surname, nationality)
        cursor.execute(add_jury_query, jury_data)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True  # Return True if player is added successfully

    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False if an error occurs

def update_stadium_name(stadium_id, new_name):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()
        # Prepare the UPDATE statement
        update_stadium_query = ("UPDATE stadium "
                                "SET stadium_name = %s "
                                "WHERE stadium_id = %s")
        
        # Execute the UPDATE statement
        stadium_data = (new_name, stadium_id)
        cursor.execute(update_stadium_query, stadium_data)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True  # Return True if stadium name is updated successfully
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False if an error occurs