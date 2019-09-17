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
sqlite>
```
sqlite3>
All sql commands can be executed from the sqlite3 prompt, like this one (mind the semicolon at the end!)
```
select * from story;
1|Haghe|Lantsloot vander Haghedochte
2|Lutgart|Het Leven van Sinte Lutgart
3|HerenPassie|Ons Heren Passie
4|Beatrijs|Beatrijs
5|RijmSpr|Rijmspreuken
6|Reynaert|Van den vos Reyanerde
7|GrimOorlog|De Grimbergse Oorlog
8|FloBla|Floris ende Blancefloer
9|Heelal|Natuurkunde van het Geheelal
10|Limb_Aiol|De Limburgse Aiol
11|BY5|Brabantsche Yeesten, Vijfde Boek
12|Walewein|Walewein
13|Karel|Karel ende Elegast
14|BY7|Brabantsche Yeesten, Zevende Boek
15|Brandaen|De Reis van Sente Brandane
16|BY1|Brabantsche Yeetsen, Eerste Boek
17|Woeringen|De Slag bij Woeringen
```

database creation/initialisation
===============================

This database can be initalised from scratch as follows:
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
-------> processing file  ./data/Heelal_2.txt
story ->  Heelal
descr ->  Natuurkunde van het Geheelal
frag_id -> %d 68
line ->  [['wil', 'tu'], ['we', 'ten'], ['die'], ['hoec', 'heyt'], ['des']]
frag_id 68, syllable_nr 1, word_nbr 1, line_nbr 1, wil
frag_id 68, syllable_nr 2, word_nbr 1, line_nbr 1, tu
frag_id 68, syllable_nr 1, word_nbr 2, line_nbr 1, we
frag_id 68, syllable_nr 2, word_nbr 2, line_nbr 1, ten
frag_id 68, syllable_nr 1, word_nbr 3, line_nbr 1, die
frag_id 68, syllable_nr 1, word_nbr 4, line_nbr 1, hoec
frag_id 68, syllable_nr 2, word_nbr 4, line_nbr 1, heyt
frag_id 68, syllable_nr 1, word_nbr 5, line_nbr 1, des
line ->  [['die'], ['to', 'ten'], ['fir', 'ma', 'men', 'ten'], ['es']]
frag_id 68, syllable_nr 1, word_nbr 1, line_nbr 2, die
frag_id 68, syllable_nr 1, word_nbr 2, line_nbr 2, to
frag_id 68, syllable_nr 2, word_nbr 2, line_nbr 2, ten
frag_id 68, syllable_nr 1, word_nbr 3, line_nbr 2, fir
frag_id 68, syllable_nr 2, word_nbr 3, line_nbr 2, ma
frag_id 68, syllable_nr 3, word_nbr 3, line_nbr 2, men
frag_id 68, syllable_nr 4, word_nbr 3, line_nbr 2, ten
frag_id 68, syllable_nr 1, word_nbr 4, line_nbr 2, es
line ->  [['daer'], ['die'], ['ster', 'ren'], ['al', 'le'], ['in'], ['staen']]
frag_id 68, syllable_nr 1, word_nbr 1, line_nbr 3, daer
frag_id 68, syllable_nr 1, word_nbr 2, line_nbr 3, die
frag_id 68, syllable_nr 1, word_nbr 3, line_nbr 3, ster
frag_id 68, syllable_nr 2, word_nbr 3, line_nbr 3, ren
frag_id 68, syllable_nr 1, word_nbr 4, line_nbr 3, al
frag_id 68, syllable_nr 2, word_nbr 4, line_nbr 3, le
frag_id 68, syllable_nr 1, word_nbr 5, line_nbr 3, in
frag_id 68, syllable_nr 1, word_nbr 6, line_nbr 3, staen
line ->  [['nu'], ['hoert'], ['hier'], ['ic'], ['seg', 'di'], ['saen']]
frag_id 68, syllable_nr 1, word_nbr 1, line_nbr 4, nu
frag_id 68, syllable_nr 1, word_nbr 2, line_nbr 4, hoert
frag_id 68, syllable_nr 1, word_nbr 3, line_nbr 4, hier
frag_id 68, syllable_nr 1, word_nbr 4, line_nbr 4, ic
frag_id 68, syllable_nr 1, word_nbr 5, line_nbr 4, seg
frag_id 68, syllable_nr 2, word_nbr 5, line_nbr 4, di
frag_id 68, syllable_nr 1, word_nbr 6, line_nbr 4, saen
```
reporting
=========
To easy the creation of reports, a Report class has been defined in *models.py*. Most methods are staticly defined, and do not require initialisation of the class. The report methods can be accessed easily via the *flask* shell prompt. Best is to define an environment variable on the command line, prior to start using the flask shell:
```
#export FLASK_APP=scanblog.py
```
 * get\_syl\_frag(frag_id)
 Puts all syllables of a fragment in a dictionary, initalising the key 'stress' to False and 'cnt' to 0
 ```
 >>> Report.get_syl_frag(1)
{1: {'syl': 're', 'stress': False, 'cnt': 0}, 2: {'syl': 'de', 'stress': False, 'cnt': 0}, 3: {'syl': 'ne', 'stress': False, 'cnt': 0}, 4: {'syl': 'had', 'stress': False, 'cnt': 0}, 5: {'syl': 'de', 'stress': False, 'cnt': 0}, 6: {'syl': 'recht', 'stress': False, 'cnt': 0}, 7: {'syl': 'die', 'stress': False, 'cnt': 0}, 8: {'syl': 'mi', 'stress': False, 'cnt': 0}, 9: {'syl': 'bla', 'stress': False, 'cnt': 0}, 10: {'syl': 'meer', 'stress': False, 'cnt': 0}, 11: {'syl': 'de', 'stress': False, 'cnt': 0}, 12: {'syl': 'dat', 'stress': False, 'cnt': 0}, 13: {'syl': 'ic', 'stress': False, 'cnt': 0}, 14: {'syl': 'mi', 'stress': False, 'cnt': 0}, 15: {'syl': 'noit', 'stress': False, 'cnt': 0}, 16: {'syl': 'ter', 'stress': False, 'cnt': 0}, 17: {'syl': 'min', 'stress': False, 'cnt': 0}, 18: {'syl': 'nen', 'stress': False, 'cnt': 0}, 19: {'syl': 'keer', 'stress': False, 'cnt': 0}, 20: {'syl': 'de', 'stress': False, 'cnt': 0}, 21: {'syl': 'mi', 'stress': False, 'cnt': 0}, 22: {'syl': 'ne', 'stress': False, 'cnt': 0}, 23: {'syl': 'pi', 'stress': False, 'cnt': 0}, 24: {'syl': 'ne', 'stress': False, 'cnt': 0}, 25: {'syl': 'es', 'stress': False, 'cnt': 0}, 26: {'syl': 'swaer', 'stress': False, 'cnt': 0}, 27: {'syl': 'die', 'stress': False, 'cnt': 0}, 28: {'syl': 'ic', 'stress': False, 'cnt': 0}, 29: {'syl': 'do', 'stress': False, 'cnt': 0}, 30: {'syl': 'gen', 'stress': False, 'cnt': 0}, 31: {'syl': 'moet', 'stress': False, 'cnt': 0}, 32: {'syl': 'ic', 'stress': False, 'cnt': 0}, 33: {'syl': 'wil', 'stress': False, 'cnt': 0}, 34: {'syl': 'se', 'stress': False, 'cnt': 0}, 35: {'syl': 'la', 'stress': False, 'cnt': 0}, 36: {'syl': 'ten', 'stress': False, 'cnt': 0}, 37: {'syl': 'het', 'stress': False, 'cnt': 0}, 38: {'syl': 'es', 'stress': False, 'cnt': 0}, 39: {'syl': 'mi', 'stress': False, 'cnt': 0}, 40: {'syl': 'goet', 'stress': False, 'cnt': 0}}
>>> 
```

 * get\_freq\_stressed\_frag(frag\_id)
 Counts all the syllables that were stressed by all the users in a fragment. These are updated in the previous structured, so that the result is a complete dictionary of 1 fragment, with all stressed and non-stressed syllables. So the output looks the same as above, with the syllables that were stressed indicated with 'True' and with 'cnt' the number of times it was stressed.
 
 * get\_syl\_story(story_id)
 Same as above, but for a complete story. The stories title (original filename) and fragment number, will be included as a key element in the result. In the next example we use the *pprint* module, so before using it, just do *import pprint*
 ```
 >>> pprint.pprint(Report.get_syl_story(1))         
1
63
{'BrRose_1': {2874: {'cnt': 0, 'stress': False, 'syl': 'al'},
              2875: {'cnt': 0, 'stress': False, 'syl': 'se'},
              2876: {'cnt': 0, 'stress': False, 'syl': 'oft'},
              2877: {'cnt': 0, 'stress': False, 'syl': 'wa'},
              2878: {'cnt': 0, 'stress': False, 'syl': 'ren'},
              2879: {'cnt': 0, 'stress': False, 'syl': 'nu'},
              2880: {'cnt': 0, 'stress': False, 'syl': 'we'},
              2881: {'cnt': 0, 'stress': False, 'syl': 'ro'},
              2882: {'cnt': 0, 'stress': False, 'syl': 'sen'},
              2883: {'cnt': 0, 'stress': False, 'syl': 'vrou'},
              2884: {'cnt': 0, 'stress': False, 'syl': 'we'},
              2885: {'cnt': 0, 'stress': False, 'syl': 'bli'},
              2886: {'cnt': 0, 'stress': False, 'syl': 'scap'},
              2887: {'cnt': 0, 'stress': False, 'syl': 'was'},
              2888: {'cnt': 0, 'stress': False, 'syl': 'so'},
              2889: {'cnt': 0, 'stress': False, 'syl': 'o'},
              2890: {'cnt': 0, 'stress': False, 'syl': 'ver'},
              2891: {'cnt': 0, 'stress': False, 'syl': 'sco'},
              2892: {'cnt': 0, 'stress': False, 'syl': 'ne'},
              2893: {'cnt': 0, 'stress': False, 'syl': 'dat'},
              2894: {'cnt': 0, 'stress': False, 'syl': 'sceen'},
              2895: {'cnt': 0, 'stress': False, 'syl': 'e'},
              2896: {'cnt': 0, 'stress': False, 'syl': 'ne'},
              2897: {'cnt': 0, 'stress': False, 'syl': 'god'},
              2898: {'cnt': 0, 'stress': False, 'syl': 'din'},
              2899: {'cnt': 0, 'stress': False, 'syl': 'ne'},
              2900: {'cnt': 0, 'stress': False, 'syl': 'u'},
              2901: {'cnt': 0, 'stress': False, 'syl': 'ten'},
              2902: {'cnt': 0, 'stress': False, 'syl': 'tro'},
              2903: {'cnt': 0, 'stress': False, 'syl': 'ne'},
              2904: {'cnt': 0, 'stress': False, 'syl': 'so'},
              2905: {'cnt': 0, 'stress': False, 'syl': 'ver'},
              2906: {'cnt': 0, 'stress': False, 'syl': 'lich'},
              2907: {'cnt': 0, 'stress': False, 'syl': 'tes'},
              2908: {'cnt': 0, 'stress': False, 'syl': 'se'},
              2909: {'cnt': 0, 'stress': False, 'syl': 'daer'},
              2910: {'cnt': 0, 'stress': False, 'syl': 'se'},
              2911: {'cnt': 0, 'stress': False, 'syl': 'ginc'},
              2912: {'cnt': 0, 'stress': False, 'syl': 'ne'},
              2913: {'cnt': 0, 'stress': False, 'syl': 'ven'},
              2914: {'cnt': 0, 'stress': False, 'syl': 'de'},
              2915: {'cnt': 0, 'stress': False, 'syl': 'du'},
              2916: {'cnt': 0, 'stress': False, 'syl': 'te'},
              2917: {'cnt': 0, 'stress': False, 'syl': 'den'},
              2918: {'cnt': 0, 'stress': False, 'syl': 'jon'},
              2919: {'cnt': 0, 'stress': False, 'syl': 'ge'},
              2920: {'cnt': 0, 'stress': False, 'syl': 'linc'}},
```
 * get\_syl\_all()
 Gets the same result as above, but for all the stories defined in the story table.
 * res\_to\_csv(fname, res)
 Puts the result of the methods above (dictionaries) into a csv file, enhanced with the description of the stories.
 ```
 >>> res=Report.get_syl_story(1)
1
63
>>> Report.res_to_csv('test4.csv', res)
```
The file *test4.csv* will be created in the directory were the flask shell was started.
```
#cat test4.csv
cat test4.csv
title,syl,cnt,stress
BrRose_2,,,
,re,0,False
,de,0,False
,ne,0,False
,had,0,False
,de,0,False
,recht,0,False
,die,0,False
,mi,0,False
,bla,0,False
,meer,0,False
,de,0,False
,dat,0,False
,ic,0,False
,mi,0,False
,noit,0,False
,ter,0,False
,min,0,False
,nen,0,False
,keer,0,False
,de,0,False
,mi,0,False
,ne,0,False
,pi,0,False
,ne,0,False
,es,0,False
,swaer,0,False
,die,0,False
,ic,0,False
,do,0,False
,gen,0,False
,moet,0,False
,ic,0,False
,wil,0,False
,se,0,False
,la,0,False
,ten,0,False
,het,0,False
,es,0,False
,mi,0,False
,goet,0,False
BrRose_1,,,
,al,0,False
,se,0,False
,oft,0,False
,wa,0,False
,ren,0,False
,nu,0,False
,we,0,False
,ro,0,False
,sen,0,False
,vrou,0,False
,we,0,False
,bli,0,False
,scap,0,False
,was,0,False
,so,0,False
,o,0,False
,ver,0,False
,sco,0,False
,ne,0,False
,dat,0,False
,sceen,0,False
,e,0,False
,ne,0,False
,god,0,False
,din,0,False
,ne,0,False
,u,0,False
,ten,0,False
,tro,0,False
,ne,0,False
,so,0,False
,ver,0,False
,lich,0,False
,tes,0,False
,se,0,False
,daer,0,False
,se,0,False
,ginc,0,False
,ne,0,False
,ven,0,False
,de,0,False
,du,0,False
,te,0,False
,den,0,False
,jon,0,False
,ge,0,False
,linc,0,False
```
 * get\_scans\_user(user\_id)
 Gets all the scans of all the fragments of a specified user (user\_id). The result is placed in a dictionary, with key elements the *stories title* '\_' *fragments number*. The dictionaries structure is the same as the one documented above, but the value of 'cnt' will never be higher than 1 (0 for the not stressd syllables).
 ```
 >>> pprint.pprint(Report.get_scans_user(1))
{'Brandaen_2': {2921: {'cnt': 1, 'stress': True, 'syl': 'daer'},
                2922: {'cnt': 0, 'stress': False, 'syl': 'was'},
                2923: {'cnt': 1, 'stress': True, 'syl': 'hem'},
                2924: {'cnt': 0, 'stress': False, 'syl': 'si'},
                2925: {'cnt': 0, 'stress': False, 'syl': 'ne'},
                2926: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2927: {'cnt': 1, 'stress': True, 'syl': 'we'},
                2928: {'cnt': 0, 'stress': False, 'syl': 'van'},
                2929: {'cnt': 0, 'stress': False, 'syl': 'ee'},
                2930: {'cnt': 1, 'stress': True, 'syl': 're'},
                2931: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2932: {'cnt': 1, 'stress': True, 'syl': 'wan'},
                2933: {'cnt': 0, 'stress': False, 'syl': 'del'},
                2934: {'cnt': 0, 'stress': False, 'syl': 'de'},
                2935: {'cnt': 0, 'stress': False, 'syl': 'al'},
                2936: {'cnt': 0, 'stress': False, 'syl': 'so'},
                2937: {'cnt': 1, 'stress': True, 'syl': 'see'},
                2938: {'cnt': 0, 'stress': False, 'syl': 're'},
                2939: {'cnt': 1, 'stress': True, 'syl': 'dat'},
                2940: {'cnt': 0, 'stress': False, 'syl': 'si'},
                2941: {'cnt': 0, 'stress': False, 'syl': 'ne'},
                2942: {'cnt': 0, 'stress': False, 'syl': 'cu'},
                2943: {'cnt': 1, 'stress': True, 'syl': 'me'},
                2944: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2945: {'cnt': 0, 'stress': False, 'syl': 'kan'},
                2946: {'cnt': 1, 'stress': True, 'syl': 'den'},
                2947: {'cnt': 1, 'stress': True, 'syl': 'pec'},
                2948: {'cnt': 0, 'stress': False, 'syl': 'had'},
                2949: {'cnt': 0, 'stress': False, 'syl': 'den'},
                2950: {'cnt': 1, 'stress': True, 'syl': 'hem'},
                2951: {'cnt': 0, 'stress': False, 'syl': 'die'},
                2952: {'cnt': 0, 'stress': False, 'syl': 'hel'},
                2953: {'cnt': 1, 'stress': True, 'syl': 'sche'},
                2954: {'cnt': 0, 'stress': False, 'syl': 'vi'},
                2955: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2956: {'cnt': 1, 'stress': True, 'syl': 'den'},
                2957: {'cnt': 0, 'stress': False, 'syl': 'ghe'},
                2958: {'cnt': 0, 'stress': False, 'syl': 'wre'},
                2959: {'cnt': 1, 'stress': True, 'syl': 'ven'},
                2960: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2961: {'cnt': 0, 'stress': False, 'syl': 'lijf'},
                2962: {'cnt': 1, 'stress': True, 'syl': 'en'},
                2963: {'cnt': 0, 'stress': False, 'syl': 'de'},
                2964: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2965: {'cnt': 1, 'stress': True, 'syl': 'baert'}},
 
```
 * To save the result in a file, we just pickle it, but there is a method in the class Report, called **user\_scans\_to\_file(user\_id, filename). This will call the previous method (get\_scnas\_user), and then save the dictionary to a file.
```
>>> Report.user_scans_to_file(1, 'test2.pickle')
user scans for id 1 have been written to test2.pickle
```
 * to get the data in the file back into a dictionary, use the following function *file\_scnas\_to\_dict(filename)
```
>>> scans_dict=Report.file_scans_to_dict('test2.pickle')
>>> pprint.pprint(scans_dict)
{'Brandaen_2': {2921: {'cnt': 1, 'stress': True, 'syl': 'daer'},
                2922: {'cnt': 0, 'stress': False, 'syl': 'was'},
                2923: {'cnt': 1, 'stress': True, 'syl': 'hem'},
                2924: {'cnt': 0, 'stress': False, 'syl': 'si'},
                2925: {'cnt': 0, 'stress': False, 'syl': 'ne'},
                2926: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2927: {'cnt': 1, 'stress': True, 'syl': 'we'},
                2928: {'cnt': 0, 'stress': False, 'syl': 'van'},
                2929: {'cnt': 0, 'stress': False, 'syl': 'ee'},
                2930: {'cnt': 1, 'stress': True, 'syl': 're'},
                2931: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2932: {'cnt': 1, 'stress': True, 'syl': 'wan'},
                2933: {'cnt': 0, 'stress': False, 'syl': 'del'},
                2934: {'cnt': 0, 'stress': False, 'syl': 'de'},
                2935: {'cnt': 0, 'stress': False, 'syl': 'al'},
                2936: {'cnt': 0, 'stress': False, 'syl': 'so'},
                2937: {'cnt': 1, 'stress': True, 'syl': 'see'},
                2938: {'cnt': 0, 'stress': False, 'syl': 're'},
                2939: {'cnt': 1, 'stress': True, 'syl': 'dat'},
                2940: {'cnt': 0, 'stress': False, 'syl': 'si'},
                2941: {'cnt': 0, 'stress': False, 'syl': 'ne'},
                2942: {'cnt': 0, 'stress': False, 'syl': 'cu'},
                2943: {'cnt': 1, 'stress': True, 'syl': 'me'},
                2944: {'cnt': 0, 'stress': False, 'syl': 'ver'},
                2945: {'cnt': 0, 'stress': False, 'syl': 'kan'},
                2946: {'cnt': 1, 'stress': True, 'syl': 'den'},
                2947: {'cnt': 1, 'stress': True, 'syl': 'pec'},
                2948: {'cnt': 0, 'stress': False, 'syl': 'had'},
                2949: {'cnt': 0, 'stress': False, 'syl': 'den'},
                2950: {'cnt': 1, 'stress': True, 'syl': 'hem'},
                2951: {'cnt': 0, 'stress': False, 'syl': 'die'},
                2952: {'cnt': 0, 'stress': False, 'syl': 'hel'},
                2953: {'cnt': 1, 'stress': True, 'syl': 'sche'},
                2954: {'cnt': 0, 'stress': False, 'syl': 'vi'},
                2955: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2956: {'cnt': 1, 'stress': True, 'syl': 'den'},
                2957: {'cnt': 0, 'stress': False, 'syl': 'ghe'},
                2958: {'cnt': 0, 'stress': False, 'syl': 'wre'},
                2959: {'cnt': 1, 'stress': True, 'syl': 'ven'},
                2960: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2961: {'cnt': 0, 'stress': False, 'syl': 'lijf'},
                2962: {'cnt': 1, 'stress': True, 'syl': 'en'},
                2963: {'cnt': 0, 'stress': False, 'syl': 'de'},
                2964: {'cnt': 0, 'stress': False, 'syl': 'an'},
                2965: {'cnt': 1, 'stress': True, 'syl': 'baert'}},
 'Ferg_1': {1030: {'cnt': 0, 'stress': False, 'syl': 'die'},
            1031: {'cnt': 0, 'stress': False, 'syl': 'co'},
            1032: {'cnt': 1, 'stress': True, 'syl': 'ninc'},
```
reporting2
==========
Modified the reporting a bit, so it will reflect the verses in lists of lists,
which is better, because a list maintains order, and dictionaries do not (until Phyton 3.7)

 * get\_syl\_frag(frag_id)
 Retrieves all the syllables in a fragment. Each verse is a list of words, where the words contain one or more syllables. Best is to look at an example. We use the *pprint** function to output the result.
 ```
 >>> pprint.pprint(Report2.get_syl_frag(2))
[[[0, 0], [0], [0], [0], [0], [0, 0]],
 [[0], [0], [0], [0, 0], [0], [0, 0]],
 [[0, 0], [0, 0], [0, 0], [0], [0], [0], [0, 0]],
 [[0, 0], [0, 0], [0, 0], [0], [0, 0, 0]],
 [[0], [0, 0], [0], [0], [0], [0, 0, 0]],
 [[0], [0], [0, 0], [0], [0, 0, 0], [0, 0, 0]]]
```
The values in the lists indicate if a syllable has been stressed (1) or not (0). They are all initialised to zero's.
 * get\_scans\_frag(frag_id, use\r_id)
 Retrieves all scans for a user on a specific fragment. In the database, only the stressed scans are retained. So this function will set the correct syllables to a one value in the previous list of lists.
 
 ```
 >>> pprint.pprint(Report2.get_scans_frag(2,1))
[[[0, 1], [1], [0], [1], [0], [1, 0]],
 [[1], [0], [0], [0, 1], [0], [1, 0]],
 [[1, 0], [1, 0], [1, 0], [1], [0], [0], [1, 0]],
 [[0, 0], [1, 0], [1, 0], [0], [1, 0, 0]],
 [[0], [1, 0], [1], [0], [1], [0, 1, 0]],
 [[1], [0], [1, 0], [0], [0, 1, 0], [0, 1, 0]]]
```
 * get\_scans\_user(user_id)
 Retrieves all the scans of a specific user. This will place all the lists in a dictionary, with a key named to the fragment. In the next example, we only show 2 fragments for the specified user, the real list is much longer.
 
 ```
 >>> pprint.pprint(Report2.get_scans_user(1)) 
{u'BY1_1': [[[0, 0], [1, 0, 1, 0], [1], [0, 1, 0]],
            [[1], [0], [1, 0], [1], [0], [1, 0]],
            [[1], [0], [1], [0, 0], [1], [0], [1, 0]],
            [[0], [0, 1, 0], [1, 0], [1, 0]],
            [[1, 0], [0], [1, 0], [0], [0, 1, 0]],
            [[1, 0], [1, 0, 0], [1], [0, 1, 0]],
            [[1, 0], [0], [1], [0], [1], [0, 1, 0]],
            [[0], [1, 0], [1, 0], [1, 0], [1], [0], [1, 0]],
            [[0], [1, 0], [1], [0], [1]],
            [[0], [1, 0], [1], [0, 1, 0], [1]]],
 u'Beatrijs_1': [[[0], [1, 0], [0, 1, 0], [0], [1, 0], [1, 0, 0]],
                 [[0, 1, 0], [1, 0], [1, 0], [1, 0]],
                 [[1], [0], [1, 0], [1], [0], [1, 0]],
                 [[1, 0], [0], [1, 0], [1], [0, 1, 0]],
                 [[1], [0], [1, 0], [1, 0], [1, 0]],
                 [[1, 0], [1], [0], [1, 0], [1]]],
 u'BrRose_1': [[[1, 0], [0], [1, 0], [1, 0], [1, 0]],
               [[1, 0], [1, 0], [1], [0], [1, 0, 1, 0]],
               [[0], [1], [0, 0], [0, 1, 0], [1, 0], [1, 0]],
               [[1], [0, 1, 0, 0], [1, 0], [1]],
               [[1, 0], [0, 1, 0], [0], [1, 0, 1]]],
 u'Busk_2': [[[0], [1, 0], [1, 0], [0], [1], [0], [0, 1]],
             [[0], [1], [0], [1, 0], [1, 0], [1]],
             [[0, 0], [1, 0], [1, 0], [0], [1], [1, 0]],
             [[0, 1, 0], [1], [0], [1, 0], [1, 0]]],
```

 * all\_users\_scans()
 Retrieves all the scans of all users registered for the website. In the next example, we will only show a part of the output. The username will be the key in a dictionary, which contains the structure mentioned above.
 
 ```
  u'rkmwbhp': {u'ADoet_1': [[[1, 0], [1, 0, 0], [1], [0], [1, 0]],
                           [[1], [0], [1, 0, 0], [0], [1, 0], [1, 0]],
                           [[0], [1], [1], [1, 0, 0], [0], [1, 0]],
                           [[0], [1], [0], [1], [0], [1, 0, 1, 0]]],
              u'BY5_1': [[[0, 0], [0], [1, 0], [1], [1]],
                         [[1], [0], [0], [1, 0], [0], [0], [1]],
                         [[0, 0], [1, 0], [0], [0], [1, 0], [1, 0]],
                         [[1], [0], [1, 0], [1, 0], [1, 0]],
                         [[0], [1, 0, 0], [0], [1, 0, 0]]],
```

 * all\_users\_scans\_to\_file(filename)
 The complete dictionary will be dumped in a json structure in a file, with the specified filename.
 
