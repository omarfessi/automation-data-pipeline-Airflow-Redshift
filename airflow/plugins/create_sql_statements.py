
# to use in the CreateTables operator
staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events 
	(artist varchar,
	auth   varchar,
	firstName        varchar, 
    gender           varchar,
   	itemInSession    integer,
	lastName 		 varchar,
	length           float  ,
	level            varchar,
	location         varchar,
	method           varchar,
	page             varchar,
	registration     bigint ,
	sessionId        integer,
	song             varchar, 
	status           integer,
	ts               bigint , 
	userAgent        varchar,
	userId           integer)
								""")
staging_songs_table_create =  ("""CREATE TABLE IF NOT EXISTS staging_songs (
    song_id          varchar,
    num_songs        integer,
    title            varchar,
    artist_name      varchar,
    artist_latitude  float  ,
    year             integer,
    duration         float  , 
    artist_id        varchar,
    artist_longitude float  ,
    artist_location  varchar )
    						 """)
user_table_create = (""" CREATE TABLE IF NOT EXISTS users (
    user_id    integer PRIMARY KEY,
    first_name varchar,
    last_name  varchar,
    gender     varchar ,
    level      varchar ) 
    diststyle all;
    				""")
song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (
    song_id   varchar PRIMARY KEY, 
    title     varchar,
    artist_id varchar ,
    year      integer,
    duration  decimal)
    				""")
artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
    artist_id        varchar PRIMARY KEY,
    artist_name      varchar ,
    location         varchar ,
    artist_latitude  float, 
    artist_longitude float)
    					""")
time_table_create = (""" CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY,
    hour       integer,
    day        integer,
    week       integer,
    month      integer,
    year       integer,
    weekday    integer)
    				""")
songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays (
    songplay_id   bigint identity(0,1),
    start_time    timestamp REFERENCES time(start_time),
    user_id       integer   REFERENCES users (user_id),
    level         varchar   NOT NULL,
    song_id       varchar   REFERENCES songs (song_id),
    artist_id     varchar   REFERENCES artists(artist_id),
    session_id    integer   NOT NULL, 
    location      varchar   NOT NULL, 
    user_agent    varchar   NOT NULL)
    diststyle all;
   						 """)

create_all_tables_statement = [staging_events_table_create, staging_songs_table_create,\
user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
