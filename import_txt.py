import os, re, glob
import sqlite3 as lite

#
# check the path for txt files
# these fiels contain fragments of a
# story ,and are ordered as lists of lists
# where each word is a list, containing zero or more syllables
#
# this script populates the 'story' table as well as
# the 'syllable' table.
# remark : doesn't work on updates yet!!!!!!!
#
def import_txt_files(path, cur):
    # all data files are in the subdir data
    files = glob.glob(path + '*.txt')
    if len(files) > 0:
        print(" files found ", len(files))
        for file in files:
            print("-------> processing file ", file)
            header = True
            alist = []
            line_nbr = 0 # because of the header :-)
            word_nbr = 1
            syl_nbr = 1
            with open(file, 'r') as f:
                m = re.match(r'.*\/(\w+)_(\d+)\.txt', file)
                if m:
                    story = m.group(1)
                    fragment_nbr = m.group(2)
                else:
                    print("filename does not match")
                for line in f:
                    line_wnl = line.rstrip()
                    if header:
                        print("story -> ", story)
                        print("descr -> ", line_wnl)
                        header = False
                        cur.execute("select * from story where title = ? ", (story, ))
                        st = cur.fetchone()
                        if st is None:
                            print("no story found with title %s, inserting a new one" % story)
                            cur.execute("insert into story (title, description) values( ?, ?)",
                                        (story, line_wnl))
                            story_id = cur.lastrowid
                        else:
                            story_id = st[0]
                        #we have a new fragment
                        cur.execute("insert into fragment (story_id, frag_nbr) values ( ?, ? )",
                                    (story_id, fragment_nbr))
                        frag_id = cur.lastrowid
                        print("frag_id -> %d", frag_id)
                    else:
                        print("line -> ", line_wnl)
                        llist = eval(line_wnl)
                        # llist is a list of lists
                        for alist in llist:
                            for syl in alist:
                                print("frag_id %s, syllable_nr %s, word_nbr %s, line_nbr %s, %s"  \
                                      % (frag_id, syl_nbr, word_nbr, line_nbr, syl))
                                cur.execute("insert into syllable (frag_id, line_nbr, word_nbr, syll_nbr, \
                                syllable ) values ( ?, ?, ? ,? , ? )", \
                                            (frag_id, line_nbr, word_nbr, syl_nbr, syl))
                                syl_nbr += 1
                            syl_nbr = 1
                            word_nbr += 1
                        word_nbr = 1
                    line_nbr += 1
    else:
        print("no files found in this path %s" % (path))
                
#f __name__ == 'main':
print("ok, starting conversion txt-> db")
path = './data/'
con = lite.connect('app.db')
cur = con.cursor()
import_txt_files(path, cur)
con.commit()
con.close()
