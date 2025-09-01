Player Game Analytics

Whether your goal is to analyze your own games for strengths or weaknesses in your openings, or to analyze an upcoming opponent to develop an optimal strategy,
the aim of this project is to extract all of a user's game data to decipher performance and winrates based on the opening used at the start of the game.

To utilize this repo, follow these steps:
1) Generate an API token with Lichess
2) Download the python file "extract_data_into_***.py"
3) Insert the username of the player being analyzed, your API token, and adjust perf_type to the game format of your choosing
4) Optional: Connect your SQL database and run the script (csv file is available if preferred)

*** I plan to analyze my results and publish them using Power BI ***

REQUIRED LIBRARIES:
1) berserk - this is the lichess api to access game data
2) mysql-connector-python - used to connect to MySQL database
3) python-chess - Used to parse PGN data
