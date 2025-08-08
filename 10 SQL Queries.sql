# Creating 10 SQL Queries
 
# 1)  Total Matches Played by Format
SELECT 'T20' AS match_type, COUNT(*) AS matches FROM t20_matches 
UNION ALL
SELECT 'ODI', COUNT(*) FROM odi_matches
UNION ALL
SELECT 'TEST', COUNT(*) FROM test_matches
UNION ALL
SELECT 'IPL', COUNT(*) FROM ipl_matches;

# 2)  Top 5 Teams by Total Win (All Format)
SELECT winner, COUNT(*) AS total_wins
FROM(
	SELECT winner FROM t20_matches
    UNION ALL
    SELECT winner FROM odi_matches
    UNION ALL 
    SELECT winner FROM test_matches
    UNION ALL  
    SELECT winner FROM ipl_matches
) AS all_matches
WHERE winner != 'No Result'
GROUP BY winner
ORDER BY total_wins DESC		
LIMIT 5;

# 3)  Popular Match Venues (All Format)
SELECT venue, COUNT(*) AS match_count
FROM (
    SELECT venue FROM t20_matches
    UNION ALL
    SELECT venue FROM odi_matches
    UNION ALL
    SELECT venue FROM test_matches
    UNION ALL
    SELECT venue FROM ipl_matches
) AS all_venues
GROUP BY venue
ORDER BY match_count DESC
LIMIT 10;

# 4)  IPL Matches are Hosted in Cities
SELECT city, COUNT(*) AS matches
FROM ipl_matches
WHERE city IS NOT NULL AND city != ''
GROUP BY city
ORDER BY matches DESC;

# 5)  Total Unique Teams in Each Format
SELECT 'T20' AS format, COUNT(DISTINCT teams) AS unique_team_combos FROM t20_matches
UNION ALL
SELECT 'ODI', COUNT(DISTINCT teams) FROM odi_matches
UNION ALL
SELECT 'Test', COUNT(DISTINCT teams) FROM test_matches
UNION ALL
SELECT 'IPL', COUNT(DISTINCT teams) FROM ipl_matches;

# 6)  Number of Matches That Resulted in No Result (Per Format)
SELECT 'T20' AS format, COUNT(*) FROM t20_matches WHERE winner = 'No Result'
UNION ALL
SELECT 'ODI', COUNT(*) FROM odi_matches WHERE winner = 'No Result'
UNION ALL
SELECT 'Test', COUNT(*) FROM test_matches WHERE winner = 'No Result'
UNION ALL
SELECT 'IPL', COUNT(*) FROM ipl_matches WHERE winner = 'No Result';

# 7 IPL Matches Played Each Year
SELECT YEAR(date) AS year, COUNT(*) AS matches
FROM ipl_matches
GROUP BY year
ORDER BY year;

# 8) Most Frequent Match Types (Across All Formats)
SELECT match_type, COUNT(*) AS count
FROM (
    SELECT match_type FROM t20_matches
    UNION ALL
    SELECT match_type FROM odi_matches
    UNION ALL
    SELECT match_type FROM test_matches
    UNION ALL
    SELECT match_type FROM ipl_matches
) AS all_types
GROUP BY match_type
ORDER BY count DESC;

# 9) Number of Matches Played Per Gender
SELECT gender, COUNT(*) AS match_count
FROM (
    SELECT gender FROM t20_matches
    UNION ALL
    SELECT gender FROM odi_matches
    UNION ALL
    SELECT gender FROM test_matches
    UNION ALL
    SELECT gender FROM ipl_matches
) AS genders
GROUP BY gender;

# 10) Count of Matches Played by Each Team (Only T20)
SELECT team, COUNT(*) AS matches_played
FROM (
    SELECT SUBSTRING_INDEX(teams, ',', 1) AS team FROM t20_matches
    UNION ALL
    SELECT TRIM(SUBSTRING_INDEX(teams, ',', -1)) AS team FROM t20_matches
) AS all_teams
GROUP BY team
ORDER BY matches_played DESC;







