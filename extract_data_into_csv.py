import berserk
from converter.pgn_data import PGNData

session = berserk.TokenSession("""Insert personal API token""")
client = berserk.Client(session=session)

# establish which user's games
user = "eroman5"
# How are dates formatted ???
start_date = None
end_date = None
# type of game format
perf_type = "rapid"
# max num of games
max = 5000

def main():
    data = client.games.export_by_player(user, True, start_date, end_date, max, None, None, perf_type, None
                                 , None, False, False, True, False, False, True, False, True, None, None, None)

    filename1 = f"{user}_games.pgn"
    #filename2 = f"{user}_games.csv"

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