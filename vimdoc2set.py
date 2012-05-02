#!/usr/local/bin/python
import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag

docpath = 'vim.docset/Contents/Resources/Documents'
db = sqlite3.connect('vim.docset/Contents/Resources/docSet.dsidx')

cur = db.cursor()
try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

any = re.compile('.*')
for fn in os.listdir(docpath):
    if os.path.splitext(fn)[1] == '.html':
        print fn
        page = open(os.path.join(docpath,fn)).read()
        soup = BeautifulSoup(page)
    
        for tag in soup.find_all('a', {'name':any}):
            name = tag.attrs['name'].strip("'")
            
            # Vim helptag?
            try: helptag = tag.previous_sibling.strip()[-1] == '*' and tag.next_sibling.next_sibling.strip()[0] == '*'
            except: helptag = False
            # Chapter link?
            try:
                float(name)
                helptag = False
            except: pass
            # Text file link?
            try: helptag = name[-4:] != '.txt'  # File link?
            except: pass

            if helptag:
                path = '%s#%s' % (fn, name)
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'cat', path))
                print '  name: %s, path: %s' % (name, path)

db.commit()
db.close()
