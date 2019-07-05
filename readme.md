data for the project
====================
Is contained in the *data* subfolder, where each textfile describes a fragment of a poem (story). a story is described by a title, and can have one or more fragments. These are indicated by the suffix of the data files, e.g *Beatrijs_1.txt , Beatrijs_2.txt.* These textfiles contain the syllables of the poem in the form of python lists, where every row is a list of lists, containing words and syllables. The first row of the textfile conatins a title for the fragment, which will appear in the scansessions. As an example *Beatrijs_1.txt*
 ```
 Beatrijs
[['si'], ['sei', 'de'], ['ma', 'ri', 'a'], ['die'], ['go', 'de'], ['so', 'ghe', 'de']]
[['fon', 'tey', 'ne'], ['bo', 'ven'], ['al', 'le'], ['wi', 'ven']]
[['laet'], ['mi'], ['in', 'der'], ['noet'], ['niet'], ['bli', 'ven']]
[['vrou', 'we'], ['ic'], ['ne', 'me'], ['u'], ['tor', 'con', 'den']]
[['dat'], ['mi'], ['rou', 'wen'], ['mi', 'ne'], ['son', 'den']]
[['en', 'de'], ['sijn'], ['mi'], ['her', 'de'], ['leet']]
```

database for mavahmine
======================
all tables are defined in *models.py*, 
 * user : contains all user information. 
 * story : titles and description
 * fragment : contains reference to a story and the fragment number, which is the postfix of the filename, in the example above the fragment number is 1.
 * syllable : with indication of line, word and syllable number, we can contain all information from the data textfiles. 
 * annotation: which syllables were (un)stressed by the user
 * fragmentdone: which scans a user has finished
Database is *sqlite3*, and is stored in *app.db*. All data and database definitions can be queried by using the command line tool *sqlite3*.
```
#sqlite3 app.db
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
sqlite>
```
To get all tables in the database
```
sqlite> .tables
annotation    fragmentdone  syllable    
fragment      story         user        
```
and to get a schema of 1 table (definition of the table)
```
sqlite> .schema syllable
CREATE TABLE syllable (
        id INTEGER NOT NULL, 
        frag_id INTEGER NOT NULL, 
        line_nbr SMALLINT NOT NULL, 
        word_nbr SMALLINT NOT NULL, 
        syll_nbr SMALLINT NOT NULL, 
        syllable VARCHAR(30) NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(frag_id) REFERENCES fragment (id)
);
CREATE INDEX ix_syllable_frag_id ON syllable (frag_id);
sqlite
```

database creation/initialisation
===============================


This database can be initalised from scratch as follows
```
#ls app.db
app.db
#rm app.db
#ls app.db
ls: cannot access 'app.db': No such file or directory
#python3 db\_create.py
#ls app.db
app.db
#python3 import_txt.py

