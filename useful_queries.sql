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