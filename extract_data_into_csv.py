import berserk
from converter.pgn_data import PGNData

session = berserk.TokenSession("lip_2MyZJjtsZKYrR19jCumw")
client = berserk.Client(session=session)

# Provide Lichess username
user = "eroman5"
# Optional: provide a date range
start_date = None
end_date = None
# Type of game format
perf_type = "rapid"
# Max num of games
max = None

def main():
    data = client.games.export_by_player(user, True, start_date, end_date, max, None, None, perf_type, None
                                 , None, False, False, True, False, False, True, False, True, None, None, None)

    filename1 = f"{user}_games.pgn"

    with open(filename1, 'w') as f:
        for game in data:
            f.write(game)
            f.write("\n\n")

    pgn_data = PGNData(filename1)
    res = pgn_data.export()

    if res.is_complete:
        print("PGN data successfully exported to CSV.")
    else:
        print("Export failed or encountered issues.")

if __name__ == "__main__":
    main()