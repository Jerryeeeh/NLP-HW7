
import streamlit as st
import re, collections
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))


def known(words): 
    return set(w for w in words if w in WORDS)

def P(word): 
    N = sum(WORDS.values())
    return WORDS[word] / N


def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits  for c in letters if R] 
    inserts    = [L + c + R               for L, R in splits for c in letters]
    self_      = [word]
   
    return set(deletes + transposes + replaces + inserts + self_ )

def doubles(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    double_    = [L + R[0] + R[:]         for L, R in splits if R      ]
    return set(double_)

def doubles2(word):
    return (d2 for d1 in doubles(word) for d2 in doubles(d1))


def edits0(word): 
    return [word]

def edits1_(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    replaces   = [L + c + R[1:]           for L, R in splits  for c in letters if R] 
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(replaces + inserts  )

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def insert(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])             for i in range(len(word) + 1)]
    insert_    = [L + c + R          for L, R in splits for c in letters]
    return (insert_)

def candidates(word): 
    return   known(insert(word)) or known(doubles2(word))|known(doubles(word))  or known(edits1(word)) or known(edits0(word)) or known(edits1(word))|known(edits2(word))  or [word] or known(edits0(word))

def correction(word): 
    return max(candidates(word), key = P )



st.title("Spell Checker DEMO")
sow = st.sidebar.checkbox("show original word")
select = st.selectbox('choose a word or ..',('','apple','mouse','elephat' ))
type = st.text_input('type your word')

if type:
    sp = type
else:
    sp = select

if  sow :
    st.text('original word:'+ sp)

if sp:
    if  sp == correction(sp):
        st.success(sp +' is the correct spelling!')
    else:
        st.error('Correction: '+correction(sp))