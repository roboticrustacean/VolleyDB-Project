import mysql.connector

def view_former_teammates(username):
    try:
        # Get the list of session IDs where the player has played
        played_squads = find_played_squads(username)
        if not played_squads:
            return []

        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Query to find distinct usernames with the same session IDs
        teammate_query = """
            SELECT DISTINCT player_username
            FROM SessionSquads
            WHERE session_id IN ({})
            AND player_username != %s
        """.format(",".join(["%s"] * len(played_squads)))

        cursor.execute(teammate_query, tuple(played_squads) + (username,))
        teammates = [row[0] for row in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return teammates

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def find_played_squads(username):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Query to find all SessionSquads where the player has played
        played_squads_query = """
            SELECT session_id
            FROM SessionSquads
            WHERE player_username = %s
        """
        cursor.execute(played_squads_query, (username,))
        played_squads = [row[0] for row in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return played_squads

    except mysql.connector.Error as err:
        print("Error:", err)
        return None


def most_played_with_height(username):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="yondu",
            database="volleydb"
        )
        cursor = conn.cursor()

        # Query to find the most played with players' average height
        query = """
            SELECT AVG(subquery.average_height) AS overall_average_height
            FROM (
                SELECT
                    COUNT(ss.session_id) AS sessions_played,
                    AVG(p.height) AS average_height
                FROM
                    SessionSquads ss
                JOIN
                    Player p ON ss.player_username = p.username
                WHERE
                    ss.session_id IN (SELECT session_id FROM SessionSquads WHERE player_username = %s)
                    AND ss.player_username != %s
                GROUP BY
                    ss.player_username
                HAVING
                    sessions_played = (
                        SELECT MAX(session_count)
                        FROM (
                            SELECT COUNT(session_id) AS session_count
                            FROM SessionSquads
                            WHERE player_username = %s
                            GROUP BY player_username
                        ) AS session_counts
                    )
            ) AS subquery
        """

        cursor.execute(query, (username, username, username))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0]  # Return the overall average height
        else:
            return None  # No result found

    except mysql.connector.Error as err:
        print("Error:", err)
        return None  # Return None in case of any error

