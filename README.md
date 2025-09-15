# Chess Game Analytics

All chess players have their own style, preferences, and preparation. This preparation can range from a beginner who knows the first two or three moves, all the way up to a grandmaster who memorizes up to 20 moves. Knowing various openings with as much depth as possible is extremely beneficial, as even minor inaccuracies in the opening can compound into debilitating disadvantages.

Given the importance of the start of any chess game, it's my goal to figure out my strongest, and weakest, openings in an effort to take a more insightful approach to my chess studies. And although the goal is to analyze my own games for strengths or weaknesses in my openings, there are a multitude of additional uses to extract, organize, and visualize chess game data by user. One key application is for those at the higher level who participate in tournaments. While preparing for a match, players will be able to extract analytics/habits on their opponent to develop an optimal strategy for their playstyle.

## Step 1: Install packages
We will need three packages:
1) berserk - To connect to lichess API and extract data
2) python-chess - To parse PGN data into a usable format
3) mysql-connector-python - To connect and automatically execute queries on MySQL database
4) io - To assist parsing the PGN strings

```
pip install berserk
pip install python-chess
pip install mysql-connector-python
```

## Step 2(, 3 and 4): Extract, Transform, & Load the data
First, the provided python file "extract_data_into_sql.py" needs to be downloaded and edited. We simply insert the username of the player whose games are to be analyzed, paste in our API token, and then populate the MySQL database connection information and run the script. A separate file "extract_data_into_csv.py" has also been provided for those who prefer spreadsheets :)
*Note: I used the SQLTools extension on VSCode, but there are plenty of ways to set up a MySQL database*
### Extract
We call on the lichess API to **extract** the game data filtered to only the specified user (date, game type, etc. also an option). The data is then formatted into a PGN file.
```
    # data is an iterable of PGN strings
    data = client.games.export_by_player(
        user, True, start_date, end_date, max, None, None, perf_type, None,
        None, False, False, True, False, False, True, False, True, None, None, None
    )
```
### Transform
Next, we **transform** and clean up the data to make it more usable and cover up those edge cases.
```
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
```
### Load
Then, we take the parsed pgn data and **load** it into the previously connected MySQL database. It gets a bit bulky, but it's mostly just the SQL table values.
```
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
```

### Step 3: Analyze & Visualize
[Sheet 1.pdf](https://github.com/user-attachments/files/22348684/Sheet.1.pdf)

**I plan to analyze my results and publish them using Tableau**
**Include some useful SQL queries**
**Summarize results**
