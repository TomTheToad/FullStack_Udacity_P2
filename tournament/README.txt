Tournament Project 2 for Udacity's Full Stack Nanodegree.
Created by Victor Asselta
Submitted version 3.2 on May 4, 2015

This folder is contained within a parent folder for the associated Project 2 class.
I did this as to allow the vagrant config information to exist in the same local
folder as on my own machine.

Requirements:
This version has been tested with and is expected to fully function with Python 2.7
	 and a PostgreSQL database on a linux Ubuntu system. The tournament.py file 
	 requires the existence of the database tournament. The database also needs to be
	 populated with the appropriate table content.

Files Structure:
All included in a single directory:

tournament.py
	The tournament file.
DB_Handler.py
	The generic PostgreSQL handler class file
README.txt
	This read me file.
tournament.sql
	The table and view initialization file
tournament_version1
	The first version of the project for comparison purposes only.
	
Setup:
For project testing, nothing other than running the tournament_test.py file should
be necessary. 

I've included an added feature which, hopefully, should create the database and then
call the tournament.sql file to populate it.

There are several reasons why this could fail. Primarily because of differences between
system file locations. If this fails please run the following within the vagrant/tournament/
directory:

1) Create the postgresql tournament database from a command prompt:
	createdb tournament

2) Populate the new tournament database:
	Login to the postgresql tournament database
		psql tournament
	Run the configuration script
		\i tournament.sql
3) Then \q to quit postgresql
	
	
The Following is an attempt to:
1) Satisfy the basic requirements for the tournament project
2) Satisfy the extra credit requirements for the tournament project.
3) Allow the potential expansion into a mutli-tournament, points based
	system for tracking multiple player careers and allowing for points
	assignments to vary between matches or tournaments.
	
Some possible upgrades:
DB_Handler:
1) Build connection timers that reset with each query to allow for better
	connection management and efficiency.
2) Testing with multiple files needing a database connection to find more requirements
3) Allow the specification of database initialization file to be run once.

tournament.py:
1) Testing for null in bye rounds.
2) Storing frequently called query results in a local dictionary that is only updated
	when something new effects the database. Allowing, of course, that this is the only
	file which affects the database.
3) Enabling the multi-tournament feature by keeping players data.
	This was purposely disabled so as to not grow the players table to a massive
	size during repeating project 2 testing.
4) Adding logic to allow for players with bye rounds to be paired in all subsequent rounds.
5) Allowing for multiple players in a match for other kinds of competitions. This would 
	require further normalization of the match_pairings table. I chose to denormalize to allow
	for both player1 and player 2 to be included in a record.
6) I began build an associated interface with Tkinter. The problems associated with allowing a
	virtual environment to show a visual environment were easy to overcome. However, I made an
	administrative decision to not include this in the final version. I thought it would be
	annoying for a tester to have to reconfigure their own environment to support this feature.
	I don't yet fully understand the capabilities of a duplicated vagrant environment.
	



	
Notes on this version 3.1: (current version)
I decided to follow as many of the recommendations of the assessment as possible with
one notable exception. I did not combine the match_pairings and match_results tables.

The combination of these two tables would mean the loss of generating the match pairings prior
to actually running the matches. The interface allows for viewing the next round of matches
is based on the previous results. I also needed the unique match id's for match_results table
normalization.

Having pointed that out, I think that most all the other recommendation where put into place.

Everything was greatly simplified.
The DB_Handler class was completely rewritten to remove the complicated query building process.
I learned a great deal building this class and will keep developing it on my own. The idea was
to explore one possible starting point for creating ORM like functionality. It is largely
academic and is not being developed for ease of use so I removed that functionality from this
assignment.

A number of table columns were dropped due to redundancy or not being currently utilized.

Views were substituted for complex and redundant queries.

Bleach was added for a layer of security to DB_Handler. Although I'm not sure if it's really
appropriate.

The standard table query was altered significantly. Here's an example:

This is mostly straight forward query with formating:
	queryContent = "INSERT INTO tournaments (name) VALUES {}".format(tournamentName)
	
Here's an altered query for added sequrity using a string reassignment:

    t_name = "'" + str(tournamentName) + "'"
    queryContent = 'INSERT INTO tournaments (name) VALUES (%s);' % (t_name)
    
This formating was a further attempt to protect from SQL injection as requested and was
adapted from recommendations on stackoverflow.com
http://stackoverflow.com/questions/1466741/parameterized-queries-with-psycopg2-python-db-api-and-postgresql


	
Notes on version 2.1: (previous version for comparison)
This is version 2.1 of both the tournament.py file and the DB_Handler.py class.
I've decided to include my personal thoughts on this project and why I decided
to go in this direction.

I love to code but, I hated this project. This project was flawed from the beginning 
and it became a greater and greater issue for me as I worked through it. 
The initial database scheme and logic was not hard, but interesting. I also really 
like to solve problems. It’s the theme for most of my life and career. I couldn’t 
reconcile the want for simplicity but the need to solve the extra credit problems 
which seemed at odds with the initial requirements. It started with the schema. 
I don’t sleep much so I tend to watch allot of documentaries. Do you know those 
lines that can get caught in your head? Things that are passed down by great thinkers, 
comedians, or even those commercials you ache to forget? One that I hold dear is 
from Walt Disney. It’s simple and pure; “Plus it”. “I want you to plus it.”

I decided, partially because the due date was so ridiculously far out, that I needed 
to do something different, to plus it. I’m fairly new to python. Prior to this I finished 
an online CS course through udemy that included python in the course. It was an interesting 
language, but I was mostly learning Java at the time and this felt like an unwanted distraction. 
The more that I delved into python, the richer the language appeared to me. Some languages give 
you a sense for their purpose in a way. Why they were created perhaps. Possibly just what role 
they may fill in your own work. Python has always felt a bit, well academic. The more that I looked 
into it, the more that it seemed to present itself for exploration and learning. 
I chose this moment to pursue it further.

The code that is enclosed with this piece is not my favorite of my work so far. 
It’s kind of mess actually. In the past year or so, I have built some beautiful classes with Java 
and manipulated memory in C but never quite started to delve into, nor piece together the workings 
of any particular language. I have been able to explore a bit more with Python. A mess perhaps but, 
in this case at least, a mess with purpose.

I decided that I’d try to build a generic class to access the postgre database. Kind of database manager 
if you will. Something that would remove the jumbled carnage that is SQL from the tournament file. 
I originally had ideas about multiple threads and timers to close database connections but this quickly 
became too large for the space that this project resided in. It’s ironic because this class was built 
with that notion in mind.

SQL is tough I think, for coders that is. It’s too close to spoken english in a way. One of the great 
things about learning a new language, programming or spoken, is that’s it’s new, and different. 
Something that gets you thinking out of your head space and asking questions. SQL is like trying to 
speak english with an accent that is not your own, awkward. I tried to create a simple system for 
building SQL queries by using decorators and logic. I know that the next project would introduce an 
ORM and that we’d essentially lose this opportunity to explore the concepts behind building a database 
manager. So, I started to build one myself. I say started because the task became larger by the day. 
I saw too much feature creep so I decided to back off and simplify. What you see here is a beginning 
of a series of ideas that I have just begun to put into practice.

I head someone say recently that school time is the time to spend. Not said in this manner, or anything 
like this really,  but it’s what I took way from it regardless so bear with me. Work projects have usually 
been hectic. Most of the time you need to just make it work, or fix it, or figure out inner workings so 
quickly that is doesn’t really stick. It’s just the nature of deadlines created by people who don’t really 
know what it is they want anyway. It’s better to spend your time learning here than rushing through and 
trying to figure out what your doing after you get the job. Oh, and by the way, you will actually get the job. 
The fun really starts after that.

I have worked a long time in the tech field and others. I’ve always felt learning never, can never stop. 
When it does, your dead…. or you, preferably, find another career. I’ve best described it as learning most 
of what’s in one room and stepping into the next to find it much much larger. It’s a wonder that anyone ever 
becomes an “expert” at anything. Either way, this endeavor has lead to something new for me at least. I’ll 
carry it into the next room and try not to lose it in the vastness that is always there to great me.

Now’s the time to take a project, even one you hate, and make it into something more, to plus it. Thanks Walt.

