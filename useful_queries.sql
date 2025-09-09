/* Directory of useful queries */

-- Select specific user's games, excluding weird variants (like Chess960, King of the Hill, etc.)
SELECT * FROM games
WHERE (white = "eroman5" OR black = "eroman5")
AND opening IS NOT NULL
ORDER BY utcdate DESC, utctime DESC;

-- Count of specific user's games, excluding weird variants
SELECT COUNT(*) AS total_count FROM games
WHERE (white = "eroman5" OR black = "eroman5")
AND opening IS NOT NULL;

-- Count of wins for specific user grouped by opening
SELECT COUNT(*) AS win_count
FROM games
WHERE ((white = 'eroman5' AND result = '1-0')
    OR (black = 'eroman5' AND result = '0-1'))
    AND opening IS NOT NULL
GROUP BY opening;

-- Opening win rates for specific user (minimum 5 games played)
SELECT
    opening,
    AVG(CASE WHEN white = 'eroman5' AND result = '1-0' THEN 1
        WHEN black = 'eroman5' AND result = '0-1' THEN 1
        WHEN result = '1/2-1/2' THEN 0.5
        ELSE 0 END) AS win_rate,
    COUNT(opening) AS games_played
FROM games
WHERE (white = 'eroman5' OR black = 'eroman5')
    AND (opening IS NOT NULL AND opening != '?')
GROUP BY opening
HAVING COUNT(opening) >= 5;