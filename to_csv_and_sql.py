
# coding: utf-8

# In[ ]:

def get_element(osm_file, tags):
    context = ET.iterparse(osm_file, events=('start',))
    _, root = next(context)
    for event, elem in context:
        if elem.tag in tags:
            yield elem
            root.clear()


# In[ ]:

def get_node(element):
    node_attribs = {}
    node_attribs['id']=element.attrib['id']
    node_attribs['user']=element.attrib['user']
    node_attribs['uid']=element.attrib['uid']
    node_attribs['version']=element.attrib['version']
    node_attribs['timestamp']=element.attrib['timestamp']
    node_attribs['changeset']=element.attrib['changeset']
    node_attribs['lat']=element.attrib['lat']
    node_attribs['lon']=element.attrib['lon']
    return node_attribs
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')  
import csv
with open ('node.csv','wb') as node_file:
    for element in get_element('brooklyn_new-york.osm',('node')):
        node_writer=csv.DictWriter(node_file,fieldnames=['id','user','uid','version','timestamp','changeset','lat','lon'])
        node_attribs=get_node(element)
        node_writer.writerow(node_attribs)


# In[ ]:

import sqlite3
db = sqlite3.connect("map")
c = db.cursor()
c.execute(('''CREATE TABLE IF NOT EXISTS node(
                id integer, user text, 
                uid interger,  version integer,
                timestamp text,  changeset integer,
                lat real,lon real
                )'''))
for e in get_element('brooklyn_new-york.osm',('node')):
    n=get_node(e)
    node_list=[n['id'],n['user'],n['uid'],n['version'],n['timestamp'],n['changeset'],n['lat'],n['lon']]
    c.execute("insert into node values(?,?,?,?,?,?,?,?)",node_list)
db.commit()
db.close()


# In[ ]:

def get_node_tag(element):
    tags=[]
    for tag in element.iter("tag"):
        if tag.attrib['k'].find(':')==-1:
            key=tag.attrib['k']
            types='regular'
        else:
            i=tag.attrib['k'].find(':')
            key=tag.attrib['k'][i+1:]
            types=tag.attrib['k'][:i]
        value=tag.attrib['v']
        if key=='phone':
            value=update_telephone_form(value)
        if key=='street':
            value=update_name(tag.attrib['v'], mapping)
        tags.append({'id':element.attrib['id'],'key':key,'value':value,'type':types})
    return tags

with open ('node_tag.csv','wb') as node_file:
    for element in get_element('brooklyn_new-york.osm',('node')):
        tags=get_node_tag(element)
        for e in tags:
            node_writer=csv.DictWriter(node_file,fieldnames=['id','type','key','value'])
            node_writer.writerow(e)


# In[ ]:

import sqlite3
node_tag = sqlite3.connect("map")
c = node_tag.cursor()
c.execute(('''CREATE TABLE IF NOT EXISTS node_tag(
                id integer, key text, 
                value text, type text
                )'''))
for e in get_element('brooklyn_new-york.osm',('node')):
    n=get_node_tag(e)
    for element in n:
        node_list=[element['id'],element['key'],element['value'],element['type']]
        c.execute("insert into node_tag values(?,?,?,?)",node_list)
node_tag.commit()
node_tag.close()


# In[ ]:

def get_way(element):
    way_attribs = {}
    way_attribs['id']=element.attrib['id']
    way_attribs['user']=element.attrib['user']
    way_attribs['version']=element.attrib['version']
    way_attribs['timestamp']=element.attrib['timestamp']
    way_attribs['uid']=element.attrib['uid']
    way_attribs['changeset']=element.attrib['changeset']
    return  way_attribs


# In[ ]:

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')  
with open ('way.csv','wb') as node_file:
    for element in get_element('brooklyn_new-york.osm',('way')):
        node_writer=csv.DictWriter(node_file,fieldnames=['id','user','uid','version','timestamp','changeset'])
        node_attribs=get_way(element)
        node_writer.writerow(node_attribs)


# In[ ]:

import sqlite3
db = sqlite3.connect("map")
c = db.cursor()
c.execute(('''CREATE TABLE IF NOT EXISTS way(
                id integer, user text, 
                uid interger,  version integer,
                timestamp text,  changeset integer)'''))
for e in get_element('brooklyn_new-york.osm',('way')):
    n=get_way(e)
    node_list=[n['id'],n['user'],n['uid'],n['version'],n['timestamp'],n['changeset']]
    c.execute("insert into way values(?,?,?,?,?,?)",node_list)
db.commit()
db.close()


# In[ ]:

def get_way_node(element):
    way_nodes=[]
    i=0
    for nd_tag in element.iter("nd"):
        i+=1
        way_nodes.append({'id':element.attrib['id'],'node_id':nd_tag.attrib['ref'],'position':i})
    return way_nodes


# In[ ]:

with open ('way_node.csv','wb') as node_file:
    for element in get_element('brooklyn_new-york.osm',('way')):
        tags=get_way_node(element)
        for e in tags:
            node_writer=csv.DictWriter(node_file,fieldnames=['id','node_id','position'])
            node_writer.writerow(e)


# In[ ]:

import sqlite3
node_tag = sqlite3.connect("map")
c = node_tag.cursor()
c.execute(('''CREATE TABLE IF NOT EXISTS way_node(
                id integer, node_id integer, 
                position integer
                )'''))
for e in get_element('brooklyn_new-york.osm',('way')):
    n=get_way_node(e)
    for element in n:
        node_list=[element['id'],element['node_id'],element['position']]
        c.execute("insert into way_node values(?,?,?)",node_list)
node_tag.commit()
node_tag.close()


# In[ ]:

def get_way_tag(element):
    tags=[]
    for way_tag in element.iter("tag"):
        if way_tag.attrib['k'].find(':')==-1:
            key=way_tag.attrib['k']
            types='regular'
        else:
            i=way_tag.attrib['k'].find(':')
            key=way_tag.attrib['k'][i+1:]
            types=way_tag.attrib['k'][:i]
        tags.append({'id':element.attrib['id'],'key':key,'value':way_tag.attrib['v'],'type':types})
    return  tags


# In[ ]:

with open ('way_tag.csv','wb') as node_file:
    for element in get_element('brooklyn_new-york.osm',('way')):
        tags=get_way_tag(element)
        for e in tags:
            node_writer=csv.DictWriter(node_file,fieldnames=['id','key','value','type'])
            node_writer.writerow(e)


# In[ ]:

import sqlite3
node_tag = sqlite3.connect("map")
c = node_tag.cursor()
c.execute(('''CREATE TABLE IF NOT EXISTS way_tags(
                id integer, key text, 
                value text, type text
                )'''))
for e in get_element('brooklyn_new-york.osm',('way')):
    n=get_way_tag(e)
    for element in n:
        node_list=[element['id'],element['key'],element['value'],element['type']]
        c.execute("insert into way_tags values(?,?,?,?)",node_list)
node_tag.commit()
node_tag.close()

