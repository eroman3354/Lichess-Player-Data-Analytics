import berserk
import mysql.connector
import chess.pgn
import io

# Initialize Lichess API client
client = berserk.Client()

user = "ericrosen" # Lichess username
start_date = 1748736000000 # June 1, 2025 (epoch time in milliseconds)
end_date = None
perf_type = "Standard"
max = None

def update_mysql_database_from_pgn_strings(pgn_strings):
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="PASSWORD",
            database="lichess_user_games"
        )
        print("Connection established successfully!")
    except mysql.connector.Error as err:
        print(err)
        return

    cursor = cnx.cursor()
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

    for pgn_str in pgn_strings:
        game = chess.pgn.read_game(io.StringIO(pgn_str))
        if game is None:
            continue
        headers = game.headers
        opening = headers.get("Opening", '')
        index = opening.find(":")
        opening = opening[:index] if index != -1 else opening
        gameid = headers.get("GameId", '')
        # Check if elo is numeric, else set to NULL (edge case handling)
        whiteelo = int(headers.get("WhiteElo", 0)) if headers.get("WhiteElo", '').isdigit() else None
        blackelo = int(headers.get("BlackElo", 0)) if headers.get("BlackElo", '').isdigit() else None
        whiteratingdiff = int(headers.get("WhiteRatingDiff", 0)) if headers.get("WhiteRatingDiff", '').isdigit() else None
        blackratingdiff = int(headers.get("BlackRatingDiff", 0)) if headers.get("BlackRatingDiff", '').isdigit() else None
        cursor.execute('''
            INSERT IGNORE INTO games (
                event, site, date, white, black, result, gameid, utcdate, utctime,
                whiteelo, blackelo, whiteratingdiff, blackratingdiff, variant, timecontrol, eco, opening, termination
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
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
            whiteelo,
            blackelo,
            whiteratingdiff,
            blackratingdiff,
            headers.get("Variant", ''),
            headers.get("TimeControl", ''),
            headers.get("ECO", ''),
            opening,
            headers.get("Termination", ''),
        ))

    cnx.commit()
    cursor.close()
    cnx.close()
    print("Connection closed.")

def main():
    data = client.games.export_by_player(
        user, True, start_date, end_date, max, None, None, perf_type, None,
        None, False, False, True, False, False, True, False, True, None, None, None
    )
    # data is an iterable of PGN strings
    update_mysql_database_from_pgn_strings(data)

if __name__ == "__main__":
    main()