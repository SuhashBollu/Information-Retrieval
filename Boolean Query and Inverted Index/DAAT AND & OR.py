import sys
import collections
from collections import OrderedDict
def BuildIndex():
    f = open(sys.argv[1], "r")
    ii_dict = dict()
    for line in f:
        flg = True
        ii_dic = line.split()
        for l in ii_dic:
            if(flg==True):
                flg = False
            else:
                if l not in ii_dict.keys():
                    ii_dict[l] = list()
    f.close()
    for l in ii_dict.keys():
        f1 = open(sys.argv[1], "r")
        for line in f1:
            if l in line.split():
                ii_dict[l].append(int(line.split()[0]))
        ii_dict[l] = sorted(ii_dict[l])
        f1.close()
    return ii_dict

def PhraseDict():
    pdict =dict()
    f1 = open(sys.argv[1],"r")
    for line in f1:
        flg = True
        psplit = line.split()
        stri = ""
        for l in psplit:
            if flg == True:
                stri = l
                pdict[l] = list()
                flg = False
            else:
                pdict[stri].append(l)
    f1.close()
    return pdict

def termFrequencyIndex():
    tf_dict = dict()
    iindex = BuildIndex()
    pdict = PhraseDict()
    for l in iindex.keys():
        tpair = dict()
        tf_dict[l]=list()
        for ls in iindex[l]:
            tpair[ls]=pdict[str(ls)].count(l)
        tf_dict[l] = tpair
    return tf_dict
            


def GetPostings(str):
    dic = BuildIndex()
    lis = dic.get(str)
    return lis

def intersectDaatAnd(lis):
    dic = dict()
    for i in lis:
        dic[i] = len(GetPostings(i))
    liste = OrderedDict(sorted(dic.items(), key=lambda x: x[1]))
    lis = list(liste.keys())
    temp  = list()
    temp=GetPostings(lis[0])
    compCount=0
    for l in range(1,len(lis)):
        l1 = len(temp)
        curray = GetPostings(lis[l])
        l2 = len(curray)
        arrm = []
        i,j=0,0
        while i<l1 and j<l2:
            compCount=compCount+1
            if temp[i] < curray[j]:
                i+=1
            elif temp[i] > curray[j]:
                j+=1
            else:
                arrm.append(curray[j])
                j+=1
                i+=1
        temp = arrm
    temp=sorted(temp)
    return temp,compCount




def unionDaatOr(lis):
    temp  = list()
    temp=GetPostings(lis[0])
    compCount=0
    for l in range(1,len(lis)):
        l1 = len(temp)
        curray = GetPostings(lis[l])
        l2 = len(curray)
        arrm = [None]*(l1+l2)
        i,j,k=0,0,0
        while i<l1 and j<l2:
            compCount=compCount+1
            if temp[i] < curray[j]:
                arrm[k] = temp[i]
                i+=1
                k+=1
            elif temp[i] > curray[j]:
                arrm[k] = curray[j]
                j+=1
                k+=1
            else:
                arrm[k] = curray[j]
                k+=1
                j+=1
                i+=1
        while i<l1:
            arrm[k] = temp[i]
            k+=1
            i+=1

        while j<l2:
            arrm[k] = curray[j]
            k +=1
            j+=1

        temp = [x for x in arrm if x is not None]
    temp = sorted(temp)
    return temp,compCount
    


def tfidf(andList, orList, termList):
    iindex = BuildIndex()
    pdict = PhraseDict()
    total_no_docs = len(PhraseDict().keys())
    tfdict = termFrequencyIndex()
    sorted_andList = list()
    sorted_orList = list()
    if(len(andList)>1):
        ascd = dict()
        for l in andList:
            tfidf = 0.00
            for term in termList:
                docid =  tfdict[str(term)]
                tf = float(docid[l]/len(pdict[str(l)]))
                idf = float(total_no_docs/len(iindex[term]))
                tfidf += tf*idf
            ascd[l] = tfidf
            sorted_d = OrderedDict(sorted(ascd.items(), key=lambda tfidf: tfidf[1], reverse = True))
        sorted_andList =  sorted_d.keys()
    else:
        sorted_andList =  andList

    if(len(orList)>1):
        oscd=dict()
        for l in orList:
            tfidf = 0.00
            for term in termList:
                docid =  tfdict[str(term)]
                if l in docid.keys():
                    tf = float(docid[l]/len(pdict[str(l)]))
                    idf = float(total_no_docs/len(iindex[term]))
                    tfidf += tf*idf
            oscd[l] = tfidf
            sorted_d = OrderedDict(sorted(oscd.items(), key=lambda tfidf: tfidf[1], reverse = True))
        sorted_orList =  sorted_d.keys()
    else:
        sorted_orList = orList

    return sorted_andList, sorted_orList





def main():
    
    f0 = open(sys.argv[3],"r")
    f2 = open(sys.argv[2],"w+")
    counter = 0
    linecount = sum(1 for line in f0)
    f0.close()
    f1 = open(sys.argv[3],"r")
    for line in f1:
        counter +=1
        linecf = line
        lst = linecf.split()
        for l in lst:
            ls = GetPostings(l)
            f2.write("GetPostings\n")
            f2.write(l)
            f2.write('\n')
            f2.write("Postings list: ")
            if(len(ls)!=0):
                for l in ls:
                    f2.write(str(l))
                    f2.write(" ")
            else:
                f2.write("empty")
            f2.write('\n')
        dal, ac = intersectDaatAnd(lst)
        f2.write("DaatAnd\n")
        f2.write(line.rstrip())
        f2.write("\nResults: ")
        if(len(dal)!=0):
            for l in dal:
                f2.write(str(l))
                f2.write(" ")
        else:
            f2.write("empty")
        f2.write("\n")
        f2.write("Number of documents in results: ")
        f2.write(str(len(dal)))
        f2.write("\n")
        f2.write("Number of comparisons: ")
        f2.write(str(ac))
        f2.write("\n")
        dol, oc = unionDaatOr(lst)
        alist, olist = tfidf(dal, dol, lst)
        f2.write("TF-IDF\n")
        f2.write("Results: ")
        if(len(alist)!=0):
            for l in alist:
                f2.write(str(l))
                f2.write(" ")
        else:
            f2.write("empty")
        f2.write("\nDaatOr\n")
        f2.write(line.rstrip())
        f2.write("\nResults: ")
        if(len(dol)!=0):
            for l in dol:
                f2.write(str(l))
                f2.write(" ")
        else:
            f2.write("empty")
        f2.write("\n")
        f2.write("Number of documents in results: ")
        f2.write(str(len(dol)))
        f2.write("\n")
        f2.write("Number of comparisons: ")
        f2.write(str(oc))
        f2.write("\n")
        f2.write("TF-IDF\n")
        f2.write("Results: ")
        if(len(olist)!=0):
            for l in olist:
                f2.write(str(l))
                f2.write(" ")
        else:
            f2.write("empty")
        if counter !=  linecount:
            f2.write("\n")
            f2.write("\n")
    f1.close()
    f2.close()

    

if __name__ == "__main__":
    main()