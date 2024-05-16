import mysql.connector
from datetime import datetime

def average_rating(username):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Prepare the SELECT statement
        average_rating_query = """
            SELECT AVG(rating) AS average_rating
            FROM MatchSessions
            WHERE assigned_jury_username = %s
        """

        # Execute the SELECT statement
        cursor.execute(average_rating_query, (username,))
        average_rating = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if average_rating is not None:
            return average_rating[0]
        else:
            return 0
        
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    
def number_of_ratings(username):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Prepare the SELECT statement
        count_query = "SELECT COUNT(*) AS rated_matches_count FROM MatchSessions WHERE assigned_jury_username = %s"
        
        # Execute the SELECT statement
        cursor.execute(count_query, (username,))
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the count of rated matches
        if result is not None:
            return result[0]
        else:
            return 0
        
    except mysql.connector.Error as err:
        print("Error:", err)
        return None  # Return None in case of any error
    
def rate_session(session_id, jury_username, rating):
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Check if the session has already been rated
        if is_already_rated(session_id, jury_username):
            print("Session has already been rated by this jury.")
            return False

        # Check if the session has already occurred
        if not session_played(session_id):
            print("Session has not yet occurred. Cannot rate.")
            return False

        

        # Update the rating for the session
        cursor.execute("UPDATE MatchSessions SET rating = %s WHERE session_id = %s AND assigned_jury_username = %s", (rating, session_id, jury_username))

        # Commit the changes
        conn.commit()

        # Close the cursor and connection

        cursor.close()
        conn.close()

        print("Session rated successfully.")
        return True

    except mysql.connector.Error as err:
        print("Error:", err)
        return False



def is_already_rated(session_id, jury_username):
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Check if the session is already rated by the jury
        cursor.execute("SELECT rating FROM MatchSessions WHERE session_id = %s AND assigned_jury_username = %s", (session_id, jury_username))
        rating = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if rating is not None:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print("Error:", err)
        return False



def session_played(session_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Get the date of the specific match session
        cursor.execute("SELECT date FROM MatchSessions WHERE session_id = %s", (session_id,))
        session_date = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if session_date:
            session_date = session_date[0]
            current_date = datetime.now().date()
            return current_date > session_date
        else:
            return False

    except mysql.connector.Error as err:
        print("Error:", err)
        return False

