import mysql.connector
from datetime import datetime
# get_current_team(username) returns the current team of the coach with the given username
def get_current_team(username):
    current_date = datetime.now().date()
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()
        query = "SELECT team_id FROM Team WHERE coach_username = %s AND contract_finish >= %s"
        cursor.execute(query, (username, current_date))
        current_team = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if current_team is not None:
            return current_team[0]

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def delete_match_session(session_id):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Prepare the DELETE statement
        delete_match_session_query = ("DELETE FROM MatchSessions WHERE session_id = %s")

        # Execute the DELETE statement
        cursor.execute(delete_match_session_query, (session_id,))

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True  # Return True if match session is deleted successfully
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return False  # Return False if an error occurs
    
def add_match_session(session_id, team_id, stadium_id, time_slot, date, jury_name, jury_surname):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Get jury username from name and surname
        get_jury_username_query = ("SELECT username FROM Jury WHERE name = %s AND surname = %s")
        cursor.execute(get_jury_username_query, (jury_name, jury_surname))
        assigned_jury_username = cursor.fetchone()

        # Check if jury exists
        if assigned_jury_username is not None:
            assigned_jury_username = assigned_jury_username[0]  # Extracting username from the tuple
        else:
            # Jury not found, return False
            return None
        # Prepare the INSERT statement
        add_match_session_query = ("INSERT INTO MatchSessions "
                                    "(session_id, team_id, stadium_id, time_slot, date, assigned_jury_username, rating) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, NULL)")
        

        # Execute the INSERT statement
        cursor.execute(add_match_session_query, (session_id, team_id, stadium_id, time_slot, date, assigned_jury_username))

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return session_id  # Return the session ID if match session is added successfully
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return None  # Return False if an error occurs
    

def create_session_squad(session_id, team_id, players):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # get the last squad_id
        get_last_squad_id_query = "SELECT MAX(squad_id) FROM SessionSquads"
        cursor.execute(get_last_squad_id_query)
        last_squad_id = cursor.fetchone()[0]
        
        # If no squad exists yet, set squad_id to 1, otherwise increment by 1
        squad_id = 1 if last_squad_id is None else last_squad_id + 1

        for i, (player_name, player_surname, position_id) in enumerate(players, start=1):
            player_username = get_player_username(player_name, player_surname)
            if player_username and player_belongs_to_team(player_username, team_id):
                # Prepare the INSERT statement
                add_player_to_squad_query = ("INSERT INTO SessionSquads "
                                             "(squad_id, session_id, player_username, position_id) "
                                             "VALUES (%s, %s, %s, %s)")

                # Execute the INSERT statement
                cursor.execute(add_player_to_squad_query, (squad_id, session_id, player_username, position_id))

                squad_id += 1

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

    
def get_player_username(name, surname):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Prepare the SELECT statement
        get_player_username_query = ("SELECT username FROM Player WHERE name = %s AND surname = %s")

        # Execute the SELECT statement
        cursor.execute(get_player_username_query, (name, surname))
        player_username = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if player_username is not None:
            return player_username[0]
        
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    
def player_belongs_to_team(player_username, team_id):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Query to check if the player belongs to the specified team
        check_player_team_query = ("SELECT COUNT(*) FROM PlayerTeams "
                                   "WHERE username = %s AND team = %s")
        
        # Execute the query
        cursor.execute(check_player_team_query, (player_username, team_id))

        # Fetch the result
        count = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return count > 0
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

def list_all_stadiums():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Prepare the SELECT statement
        list_all_stadiums_query = "SELECT stadium_name, stadium_country FROM Stadium"

        # Execute the SELECT statement
        cursor.execute(list_all_stadiums_query)
        stadiums = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return stadiums
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return None