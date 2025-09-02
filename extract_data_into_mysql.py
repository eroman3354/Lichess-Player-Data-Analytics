import berserk
import mysql.connector
import chess.pgn

# Initialize Lichess API client
client = berserk.Client()

# Provide Lichess username
user = "eroman5"
# Optional: provide a date range
start_date = None
end_date = None
# Type of game format ("Standard" includes all games)
perf_type = "Standard"
# Max num of games
max = None

# Establish connection to MySQL database and populate table
def update_mysql_database(pgn_data):
    try:
        cnx = mysql.connector.connect(
            host="localhost",   # Or the IP address/domain of your MySQL server
            user="root",    # your username
            password="drunkenELAN22!",  # your password
            database="lichess_user_games"   # your database name
        )
        print("Connection established successfully!")
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    if 'cnx' in locals() and cnx.is_connected():
        cursor = cnx.cursor()
    
    if 'cursor' in locals():
        # Execute queries to populate table here
        # Create new table "games" in database if not already executed
        # Create table (adjust columns based on your schema)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                event VARCHAR(255),
                site VARCHAR(255),
                date VARCHAR(255),
                white VARCHAR(255),
                black VARCHAR(255),
                result VARCHAR(255),
                gameid VARCHAR(255) NOT NULL PRIMARY KEY,
                utcdate VARCHAR(255),
                utctime VARCHAR(255),
                whiteelo INT,
                blackelo INT,
                whiteratingdiff INT,
                blackratingdiff INT,
                variant VARCHAR(255),
                timecontrol VARCHAR(255),
                eco VARCHAR(255),
                opening VARCHAR(255),
                termination VARCHAR(255)
            );
        """)

        # Insert data
        for game_info in pgn_data:
            headers = game_info["headers"]
            # Manipulate the "Opening" field to only include broad opening names
            opening = headers.get("Opening", '')
            index = opening.find(":")
            opening = opening[:index] if index != -1 else opening
            # Get gameid
            gameid = headers.get("GameId", '')
            cursor.execute('''
                INSERT IGNORE INTO games (event, site, date, white, black, result, gameid, utcdate, utctime, 
                           whiteelo, blackelo, whiteratingdiff, blackratingdiff, variant, timecontrol, eco, opening, termination)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (
                headers.get("Event", ''),
                headers.get("Site", ''),
                headers.get("Date", ''),
                headers.get("White", ''),
                headers.get("Black", ''),
                headers.get("Result", ''),
                gameid,
                headers.get("UTCDate", ''),
                headers.get("UTCTime", ''),
                int(headers.get("WhiteElo", 0)), # Convert to integer
                int(headers.get("BlackElo", 0)), # Convert to integer
                int(headers.get("WhiteRatingDiff", 0)),
                int(headers.get("BlackRatingDiff", 0)),
                headers.get("Variant", ''),
                headers.get("TimeControl", ''),
                headers.get("ECO", ''),
                opening, # Use the manipulated opening value
                headers.get("Termination", ''),
            ))

        cnx.commit()
        cursor.close()
        cnx.close()
        print("Connection closed.")

def parse_pgn_file(filepath):
    games_data = []
    with open(filepath, encoding="utf-8") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            
            # Extract header information
            headers = game.headers
            
            games_data.append({
                "headers": headers,
            })
    return games_data

def main():
    data = client.games.export_by_player(user, True, start_date, end_date, max, None, None, perf_type, None
                                 , None, False, False, True, False, False, True, False, True, None, None, None)

    filename1 = f"{user}_games.pgn"

    with open(filename1, 'w') as f:
        for game in data:
            f.write(game)
            f.write("\n\n")
        f.close()

    game_data = parse_pgn_file(f"{user}_games.pgn")
    update_mysql_database(game_data)

if __name__ == "__main__":
    main()