
--- Fastest laps
SELECT l.activityId, l.timestamp, l.total_elapsed_time, r.activityType
FROM swim_laps l
LEFT JOIN all_activities r ON l.activityId = r.activityId
WHERE l.total_elapsed_time > 30
ORDER BY l.total_elapsed_time
LIMIT 30

--- Fastest 100m swims
SELECT l.activityId, l.total_distance, l.timestamp, l.total_elapsed_time, r.activityType
FROM swim_lengths l
LEFT JOIN all_activities r ON l.activityId = r.activityId
WHERE l.total_elapsed_time > 70 AND l.total_distance == 100
ORDER BY l.total_elapsed_time
LIMIT 10

--- Fastest 100m each month, time order
SELECT strftime("%Y-%m", r.startTimeLocal), min(l.total_elapsed_time)
FROM swim_lengths l 
LEFT JOIN all_activities r ON l.activityId = r.activityId
WHERE l.total_elapsed_time > 73 AND l.total_elapsed_time < 180 AND l.total_distance == 100
GROUP BY strftime("%Y-%m", r.startTimeLocal)
ORDER BY r.startTimeLocal


--- Fastest 200m each month, time order
SELECT strftime("%Y-%m", r.startTimeLocal), min(l.total_elapsed_time)
FROM swim_lengths l 
LEFT JOIN all_activities r ON l.activityId = r.activityId
WHERE l.total_elapsed_time > 150 AND l.total_elapsed_time < 360 AND l.total_distance == 200
GROUP BY strftime("%Y-%m", r.startTimeLocal)
ORDER BY r.startTimeLocal


--- Longest session each month, time order
???

--- "Fastest" session (distance / total time) per month, time order
???

--- "Fastest" session (average swimming speed) per month, time order
???


----------- all_activities ----------
        activityId TEXT      activityName TEXT    startTimeLocal TEXT      activityType TEXT
             5129419239             Simbassäng    2020-06-22 20:23:27           lap_swimming
             5117664387             Simbassäng    2020-06-20 14:22:40           lap_swimming
             5105060041             Simbassäng    2020-06-17 20:22:39           lap_swimming
             5094851020             Simbassäng    2020-06-15 20:26:46           lap_swimming
             5083417722             Simbassäng    2020-06-13 10:03:54           lap_swimming
             5083417317             Simbassäng    2020-06-13 09:55:20           lap_swimming

----------- swim_lengths ----------
       avg_cadence REAL    total_distance REALtotal_elapsed_time REAL         timestamp TEXT        activityId TEXT
                   22.0                  100.0                110.307    2020-06-22 18:25:18             5129419239
                    0.0                    0.0                 29.989    2020-06-22 18:25:48             5129419239
                    0.0                  100.0                176.808    2020-06-22 18:28:49             5129419239
                    0.0                    0.0                 44.597    2020-06-22 18:29:29             5129419239
                   24.0                  200.0                220.902    2020-06-22 18:33:10             5129419239
 
----------- swim_laps ----------
avg_swimming_cadence REAL     total_strokes REALtotal_elapsed_time REAL         timestamp TEXT        activityId TEXT
                   22.0                   21.0                 57.312    2020-06-22 18:25:18             5129419239
                   23.0                   20.0                 52.995    2020-06-22 18:25:18             5129419239
                   None                   None                 29.989    2020-06-22 18:25:48             5129419239
                    0.0                    0.0                 88.404    2020-06-22 18:28:49             5129419239
                    0.0                    0.0                 88.404    2020-06-22 18:28:49             5129419239
                   None                   None                 44.597    2020-06-22 18:29:29             5129419239
                   22.0                   21.0                 56.375    2020-06-22 18:33:10             5129419239
