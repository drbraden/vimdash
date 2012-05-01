#!/usr/local/bin/python

import os, sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('vim.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()

cur.execute('DROP TABLE searchIndex;')
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')

docpath = 'vim.docset/Contents/Resources/Documents'

for fn in os.listdir(docpath):
    if os.path.splitext(fn)[1] == '.html':

        page = open(os.path.join(docpath,fn)).read()
        soup = BeautifulSoup(page)
    
        for a in soup.find_all('a'):
            #if 'name' in a.attrs.keys():
            #    name = a.attrs['name']
            #    cur.execute('INSERT INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'func', fn))
            #    print 'name: %s, path: %s' % (name, fn)

            if 'href' in a.attrs.keys():
                name = a.text
                anchor = a.attrs['href']
                if '#' in anchor: path = anchor
                else: path = fn
                cur.execute('DELETE FROM searchIndex WHERE name = ? AND type = ? AND path = ?', (name, 'func', path)) # Last-in-wins dedup
                cur.execute('INSERT INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'func', path))
                print 'name: %s, path: %s' % (name, path)

conn.commit()
conn.close()