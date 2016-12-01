#-*-coding:utf-8-*-
from near_synonym.models import GRDS
from json import dumps
from collections import OrderedDict

grds={} #g_rds[governor]={relation:{dependent:sentences}}

def append_to_grds(governor,relation,dependent,sentence,grds):
    if governor not in grds:grds[governor]={relation:{dependent:[sentence]}}
    elif relation not in grds[governor]:grds[governor][relation]={dependent:[sentence]}
    elif dependent not in grds[governor][relation]:grds[governor][relation][dependent]=[sentence]
    elif sentence not in grds[governor][relation][dependent]:
        grds[governor][relation][dependent].append(sentence)

def attach_ch_rel(REL):
    en_ch={'nsubj':'主語','dobj':'謂語'}
    if REL not in en_ch:return REL
    return '%s(%s)' % (REL,en_ch[REL])

FORM_HEAD_DEPREL=[('ROOT',0,'root')] #[{FORM,HEAD,DEPREL},...]
words=[]
for line in open('parsed'):
    if line=='\n':
        for FORM,HEAD,DEPREL in FORM_HEAD_DEPREL:
            governor=FORM_HEAD_DEPREL[HEAD][0]
            append_to_grds(governor,attach_ch_rel(DEPREL),FORM,' '.join(words),grds)
        FORM_HEAD_DEPREL=[('ROOT',0,'root')] #[{FORM,HEAD,DEPREL},...]
        words=[]
        continue
    ID,FORM,LEMMA,UPOSTAG,XPOSTAG,FEATS,HEAD,DEPREL,DEPS,MISC=line.split()
      #dependent                       #governor
    FORM_HEAD_DEPREL.append((FORM,int(HEAD),DEPREL))
    words.append(FORM)

for governor,rds in grds.items():
    print(governor)
    rds=OrderedDict(sorted(rds.items(),key=lambda r_ds:sum([len(r_ds[1][d]) for d in r_ds[1]]),reverse=True))
    for r,ds in rds.items():
        rds[r]=OrderedDict(sorted(ds.items(),key=lambda d_s:len(d_s[1]),reverse=True))
    GRDS(governor=governor,rds=dumps(rds,ensure_ascii=False)).save()

