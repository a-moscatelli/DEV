#!/usr/bin/env python
# coding: utf-8

# In[1]:


NOC=6
NOH=4
NOC**NOH


# In[2]:


# can also use the online service: https://datalog.db.in.tum.de/
# or the desktop GUI: java -jar AbcDatalog-0.6.0.jar


# In[3]:


assert NOC**NOH == 1296


# In[4]:


import http.client
import urllib.parse
import json
import requests


# In[5]:


datalog='''


isa(h0,ho).
isa(h1,ho).
isa(h2,ho).
isa(h3,ho).

isa(c0,co).
isa(c1,co).
isa(c2,co).
isa(c3,co).
isa(c4,co).
isa(c5,co).

isa(b0,fbb).
isa(b1,fbb).
isa(b2,fbb).
isa(b3,fbb).
isa(b4,fbb).

isa(w0,fbw).
isa(w1,fbw).
isa(w2,fbw).
isa(w3,fbw).
isa(w4,fbw).

follows(h1,h0).
follows(h2,h1).
follows(h3,h2).

greater_than(HH,LL) :- follows(HH,MID), greater_than(MID,LL).
greater_than(HH,LL) :- follows(HH,LL).


itertools_product_co(CH0,CH1,CH2,CH3) :- isa(CH0,co), isa(CH1,co), isa(CH2,co), isa(CH3,co).    % sz = 1296 = NOC**NOH
possibilesecrets(CH0,CH1,CH2,CH3) :- itertools_product_co(CH0,CH1,CH2,CH3).

% reconciliations with python itertools are mentioned below.

itertools_combinations_ho(H0,H1) :- isa(H0,ho), isa(H1,ho), greater_than(H1,H0).            % = itertools.combinations(range(4), r=2) %%% sz = 6
itertools_combinations_ho(H0,H1,H2) :- itertools_combinations_ho(H0,H1), itertools_combinations_ho(H0,H2), itertools_combinations_ho(H1,H2).    % = itertools.combinations(range(4), r=3) %%% sz = 4
itertools_combinations_ho(H0,H1,H2,H3) :- itertools_combinations_ho(H0,H1,H2), itertools_combinations_ho(H0,H1,H3), itertools_combinations_ho(H0,H2,H3), itertools_combinations_ho(H1,H2,H3).  % = itertools.combinations(range(4), r=4) %%% sz = 1

itertools_permutations_co(CH0,CH1) :- isa(CH0,co), isa(CH1,co), CH0 != CH1. % itertools.permutations(range(6), r=2) %%% sz = 30
itertools_permutations_co(CH0,CH1,CH2) :- itertools_permutations_co(CH0,CH1), itertools_permutations_co(CH0,CH2), itertools_permutations_co(CH1,CH2). % = itertools.permutations(range(6), r=3) %%% sz = 120
itertools_permutations_co(CH0,CH1,CH2,CH3) :- itertools_permutations_co(CH0,CH1,CH2), itertools_permutations_co(CH0,CH1,CH3), itertools_permutations_co(CH0,CH2,CH3), itertools_permutations_co(CH1,CH2,CH3). % = itertools.permutations(range(6), r=4) %%% sz = 360
permutations(CH0,CH1,CH2,CH3) :- itertools_permutations_co(CH0,CH1,CH2,CH3).

%%%%%%%%%%%

secret(c1,c3,c1,c4).
guessnfeedback(c1,c0,c2,c2,b1,w0).
guessnfeedback(c2,c3,c1,c4,b3,w0).

%%%%%%%%%%%

% now show the subset of possibilesecrets(CH0,CH1,CH2,CH3) that have all the combinations of blacks in common with all the feedbacks I have got.

% from now on: untested and TBC

postg_product_b1(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 = CH0, GCH1 != CH1, GCH2 != CH2, GCH3 != CH3, BB=b1.
postg_product_b1(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 != CH0, GCH1 = CH1, GCH2 != CH2, GCH3 != CH3, BB=b1.
postg_product_b1(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 != CH0, GCH1 != CH1, GCH2 = CH2, GCH3 != CH3, BB=b1.
postg_product_b1(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 != CH0, GCH1 != CH1, GCH2 != CH2, GCH3 = CH3, BB=b1.

postg_product_b3w0(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 != CH0, GCH1 = CH1, GCH2 = CH2, GCH3 = CH3, BB=b3,WW=w0.
postg_product_b3w0(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 = CH0, GCH1 != CH1, GCH2 = CH2, GCH3 = CH3, BB=b3,WW=w0.
postg_product_b3w0(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 = CH0, GCH1 = CH1, GCH2 != CH2, GCH3 = CH3, BB=b3,WW=w0.
postg_product_b3w0(CH0,CH1,CH2,CH3) :- possibilesecrets(CH0,CH1,CH2,CH3), guessnfeedback(GCH0,GCH1,GCH2,GCH3,BB,WW), GCH0 = CH0, GCH1 = CH1, GCH2 = CH2, GCH3 != CH3, BB=b3,WW=w0.


'''


# In[6]:


def submitkb(datalogtext):
    headers = {'Content-type': 'application/json'}
    connection = http.client.HTTPConnection('localhost', 8080, timeout=30)
    payload_s = json.dumps({"uc":"learn","kb":datalogtext})
    rpost = requests.post('http://localhost:8080/HelloWorldu', headers = headers, data = payload_s)
    connection.close()
    print(rpost, rpost.text, rpost.ok, rpost.status_code)
    return rpost.status_code


# In[7]:


def getkbstat():
    connection = http.client.HTTPConnection('localhost', 8080, timeout=30)
    connection.request("GET", "/HelloWorldu?uc=kb")
    response = connection.getresponse()
    jjtext = response.read().decode()
    connection.close()
    print("query submitted. Status: {} and reason: {}".format(response.status, response.reason))
    try:
        qdict = json.loads(jjtext)
    except json.decoder.JSONDecodeError:
        print('invalid JSON:'+jjtext)
        qdict={'qs':qquery,'ans':[]}
    qdict['retcode'] = response.status
    return qdict


# In[8]:


def submitquery(query):
    assert query[-1] == '?'
    qquery = urllib.parse.quote(query)
    connection = http.client.HTTPConnection('localhost', 8080, timeout=30)
    connection.request("GET", "/HelloWorldu?uc=query&qs="+qquery)
    response = connection.getresponse()
    jjtext = response.read().decode()
    connection.close()
    print("query submitted. Status: {} and reason: {}".format(response.status, response.reason))
    assert response.status != 400
    try:
        qdict = json.loads(jjtext)
    except json.decoder.JSONDecodeError:
        print('invalid JSON:'+jjtext)
        qdict={'qs':qquery,'ans':[]}
    qdict['retcode'] = response.status
    return qdict


# In[9]:


status_code = submitkb(datalog)


# In[10]:


assert status_code==201


# In[11]:


ansdict = getkbstat()
print(ansdict)


# In[12]:


assert ansdict['retcode']==200


# In[13]:


query = "product(CH0,CH1,CH2,CH3)?"


# In[14]:


ans = submitquery(query)
alen = len(ans['ans'])
print('len(ans):',alen)


# In[15]:


assert ansdict['retcode']==200 or ansdict['retcode']==204


# In[16]:


assert alen == 1296


# In[17]:


query = "permut(CH0,CH1,CH2,CH3)?"


# In[18]:


ans_dict = submitquery(query)
alen = len(ans_dict['ans'])
print('len(ans):',alen)


# In[19]:


assert alen == 360


# In[20]:


from itertools import combinations, combinations_with_replacement, product, permutations


# In[21]:


pp = permutations([0,1,2,3,4,5], r=4)
ppls = list(pp)
print(len(ppls))


# In[22]:


print('first 10','permutations',ppls[0:10])


# In[23]:


pp = combinations([0,1,2,3,4,5], r=4)
ppls = list(pp)
print(len(ppls))


# In[24]:


print('first 10','combinations',ppls[0:10])


# In[25]:


pp = permutations([0,1,2], r=2)
ppls = list(pp)
print(len(ppls))


# In[26]:


print('first 10','permutations',ppls[0:10])


# In[27]:


pp = combinations([0,1,2], r=2)
ppls = list(pp)
print(len(ppls))


# In[28]:


print('first 10','combinations',ppls[0:10])


# In[29]:


query = "postg_product(CH0,CH1,CH2,CH3)?"
ans_dict = submitquery(query)
alen = len(ans_dict['ans'])
print('len(ans):',alen)


# In[37]:


pp = combinations(range(3), r=2) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[38]:


pp = combinations(range(4), r=2) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[42]:


pp = combinations(range(4), r=3) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[43]:


pp = combinations(range(4), r=4) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[40]:


pp = combinations(range(3), r=3) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[50]:


# from itertools import combinations, combinations_with_replacement, product, permutations
pp = permutations(range(6), r=2) # blacks
ppls = list(pp)
print(len(ppls))
print(ppls)


# In[ ]:




