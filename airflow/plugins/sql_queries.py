class SqlQueries:
    songplay_table_insert = ("""
                           INSERT INTO songplays (start_time, user_id, level, song_id, artist_id,session_id, location, user_agent)
                           SELECT DISTINCT '1970-01-01':: DATE + (se.ts/1000) * interval '1 second' AS start_time,
                                    se.userId   ,
                                    se.level    ,  
                                    ss.song_id  ,
                                    ss.artist_id,
                                    se.sessionId,
                                    se.location ,
                                    se.userAgent
                           FROM staging_events AS se JOIN staging_songs AS ss ON (ss.title=se.song AND
                           ss.artist_name=se.artist)  
                           WHERE se.page = 'NextSong';""")

    user_table_insert =("""
                        INSERT INTO users
                        SELECT DISTINCT userId,
                                        firstName,
                                        lastName,
                                        gender,
                                        level
                       FROM staging_events
                       WHERE userId IS NOT NULL;""")


    song_table_insert = ("""
                       INSERT INTO songs
                       SELECT DISTINCT song_id,
                                       title,
                                       artist_id,
                                       year,
                                       duration
                       FROM staging_songs""")

    artist_table_insert =("""
                       INSERT INTO artists 
                       SELECT DISTINCT artist_id,
                                       artist_name,
                                       artist_location,
                                       artist_latitude,
                                       artist_longitude
                       FROM staging_songs;""")

    time_table_insert = ("""
                       INSERT INTO time 
                       SELECT        TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time,
                                     EXTRACT ( hour    FROM start_time),
                                     EXTRACT ( day     FROM start_time),
                                     EXTRACT ( week    FROM start_time),
                                     EXTRACT ( month   FROM start_time),
                                     EXTRACT ( year    FROM start_time),
                                     EXTRACT ( weekday FROM start_time)
                       FROM staging_events """)
    
    


    
    # DROP TABLES if they already exist
    staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
    staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs"
    songplay_table_drop       = "DROP TABLE IF EXISTS songplays ;"
    user_table_drop           = "DROP TABLE IF EXISTS users; "
    song_table_drop           = "DROP TABLE IF EXISTS songs; "
    artist_table_drop         = "DROP TABLE IF EXISTS artists; "
    time_table_drop           = "DROP TABLE IF EXISTS time; "

