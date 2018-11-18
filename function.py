## BLACK-LAB SAS
#  19 rue du val es Dunes Caen
#  
#  Black-lab.eu
#
#  This file is owned by BLACK-LAB No portion of this document may be reproduced, 
#  copied or revised without written permission of the authors.


## @author <Hector MIKOLAJCZAK>
#  @version <1.0>

"""
liste des fonctions servant aux activités de parsing et de scoring
"""

from math import *

def ProfilRegister(FileName, FileUrl, clefbrute, cleftrate, clefvoisin, clefvecteur, Mail):
    date2 = str(datetime.now())
    profil = Profil(name= FileName,
                    url= FileUrl,
                    ClefBrute= clefbrute,
                    ClefTrate= cleftrate,
                    ClefVoisin= clefvoisin,
                    ClefVecteur= clefvecteur,
                    mail= Mail,
                    date= date2
                    )   
    profil.save()


def ReqRegister(ldes, scores, name, lobl='NONE'):
    key = secrets.token_hex(10)
    date1 = str(datetime.now())
    req = ReqReg(token= key,
                name= name,
                obl= lobl,
                desc= ldes,
                result= scores,
                date= date1,
                )       
    req.save()
    return key


def cle_swl(CV, swl=['alors','au','aucuns','aussi','autre','avant','avec','avoir','bon','car','ce','cela','ces','ceux','chaque','ci','comme','comment','dans','des','du','dedans','dehors','depuis','devrait','doit','donc','dos','début','elle','elles','en','encore','essai','est','et','eu','fait','faites','fois','font','hors','ici','il','ils','je','juste','la','le','les','leur','là','ma','maintenant','mais','mes','mine','moins','mon','mot','même','ni','nommés','notre','nous','ou','où','par','parce','pas','peut','peu','plupart','pour','pourquoi','quand','que','quel','quelle','quelles','quels','qui','sa','sans','ses','seulement','si','sien','son','sont','sous','soyez','sujet','sur','ta','tandis','tellement','tels','tes','ton','tous','tout','trop','très','tu','voient','vont','votre','vous','vu','ça','étaient','état','étions','été','être', 'de', 'des', 'et', "d'", 'la', 'en', 'du', 'and', 'les', 'à', '-', "l'", 'of', "\uf0b7", 'sur', 'the', 'pour', '—', 'un', 'to', 'in', 'au', "\uf0a7", '<', '>', '#', "\uf0d8"]):
    indice=0
    for i in range (len (CV)):
        if CV[indice] in swl :
            CV.pop(indice)
        else :
            indice+=1
    return CV


def estimer_index(Ln_alpha,mot):
    x=0
    y=len(Ln_alpha)
    indice=int(y/2)
    n=int(log2(len(Ln_alpha)))+3
    for i in range (n):
        if sorted([Ln_alpha[indice][0],mot])[0]==mot:
            y=indice
        else :
            x=indice
        indice = int((x+y)/2)
    return indice


def normcv (Ln_chrono, Ln_alpha, mot):#trouve l'equivalent normalisÈ d'un mot
    Lc=[[],[],[]]
    indice=estimer_index(Ln_alpha,mot)
    for i in range (max(0,indice-10),min(len(Ln_alpha),indice+10)):
        MAX=0
        for j in range (min(len(Ln_alpha[i][0]),len(mot))):
            if Ln_alpha[i][0][j] == mot[j] :
                MAX+=1
            else :
                break 
        Lc[0].append(MAX)
        Lc[1].append(i)
        Lc[2].append(Ln_alpha[i][0])
    L=[[],[]]
    m=max(Lc[0])
    for i in range (len(Lc[0])):
        if Lc[0][i]==m:
            L[0].append(len(Ln_alpha[Lc[1][i]][0]))
            L[1].append(Lc[1][i])
    index=L[1][L[0].index(min(L[0]))]#indice 
    MOT=Ln_alpha[index][0]
    longmax=max(len(MOT),len(mot))
    #if m/longmax>=0.5+2.7**(-longmax**2/100)*0.3:
    #print(mot,MOT)
    if m/longmax>=0.5+2.7**(-longmax**2/100)*0.3:
        Ln_alpha[index][1]+=1
        for i in range (len(Ln_chrono)):
            if Ln_chrono[i][0]==MOT:
                Ln_chrono[i][1]+=1
                break
        return [Ln_chrono,Ln_alpha,MOT]
    else :
        Ln_chrono.append([mot,1])
        Ln_alpha=sorted(Ln_alpha+[[mot,1]])
        return [Ln_chrono,Ln_alpha,mot]
    

def normCV(Ln_chrono,Ln_alpha,cv_rarete,cv_voisin,mot):#range un mot normalisÈ dans une clÈCV
    x=0
    k=normcv(Ln_chrono,Ln_alpha,mot)
    Ln_chorno,Ln_alpha,motCV=k[0],k[1],k[2]#renvoie le mot normalisÈ et la grande liste modifiÈe par le mot
    cv_voisin.append(motCV)
    for i in range (len(cv_rarete)) :
        if cv_rarete[i][0] == motCV :
            cv_rarete[i][1]+=1#modifie  cv_rarete
            return [Ln_chrono,Ln_alpha,cv_rarete,cv_voisin]
    cv_rarete.append([motCV,1])
    return [Ln_chrono,Ln_alpha,cv_rarete,cv_voisin]


def cleCV (Ln_chrono,CV):#renvoie une clÈ CV (CV est la liste de token)
    Ln_alpha=sorted(Ln_chrono)
    cle_rarete=[]
    cle_voisin=[]
    cle_vecteur=[]
    for i in CV :
        X=normCV(Ln_chrono,Ln_alpha,cle_rarete,cle_voisin,i)#modification terme par terme de la clÈ 
        Ln_chrono,Ln_alpha,cle_rarete,cle_voisin=X[0],X[1],X[2],X[3]
    for i in range (len(Ln_chrono)):
        if Ln_chrono[i][0] in cle_voisin :
            cle_vecteur.append(1)
        else :
            cle_vecteur.append(0)
    return [cle_rarete,cle_voisin,Ln_chrono,cle_vecteur]


def normrh (Ln_chrono,Ln_alpha,mot):#trouve l'equivalent normalisé d'un mot
    Lc=[[],[]]
    indice=estimer_index(Ln_alpha,mot)
    for i in range (max(0,indice-10),min(len(Ln_alpha),indice+10)):
        MAX=0
        for j in range (min(len(Ln_alpha[i][0]),len(mot))):
            if Ln_alpha[i][0][j] == mot[j] :
                MAX+=1
            else :
                break 
        Lc[0].append(MAX)
        Lc[1].append(i)
    L=[[],[]]
    m=max(Lc[0])
    for i in range (len(Lc[0])):
        if Lc[0][i]==m:
            L[0].append(len(Ln_alpha[Lc[1][i]][0]))
            L[1].append(Lc[1][i])
    index=L[1][L[0].index(min(L[0]))]#indice 
    MOT=Ln_alpha[index][0]
    longmax=max(len(MOT),len(mot))
    #(mot,MOT)
    if m/longmax>=0.5+2.7**(-longmax**2/100)*0.3:
        return MOT
    else :
        return False


def normrh1 (Ln_chrono,Ln_alpha,mot):#trouve l'equivalent normalisé d'un mot
    swl=['alors','au','aucuns','aussi','autre','avant','avec','avoir','bon','car','ce','cela','ces','ceux','chaque','ci','comme','comment','dans','des','du','dedans','dehors','depuis','devrait','doit','donc','dos','début','elle','elles','en','encore','essai','est','et','eu','fait','faites','fois','font','hors','ici','il','ils','je','juste','la','le','les','leur','là','ma','maintenant','mais','mes','mine','moins','mon','mot','même','ni','nommés','notre','nous','ou','où','par','parce','pas','peut','peu','plupart','pour','pourquoi','quand','que','quel','quelle','quelles','quels','qui','sa','sans','ses','seulement','si','sien','son','sont','sous','soyez','sujet','sur','ta','tandis','tellement','tels','tes','ton','tous','tout','trop','très','tu','voient','vont','votre','vous','vu','ça','étaient','état','étions','été','être', 'de', 'des', 'et', "d'", 'la', 'en', 'du', 'and', 'les', 'à', '-', "l'", 'of', "\uf0b7", 'sur', 'the', 'pour', '—', 'un', 'to', 'in', 'au', "\uf0a7", '<', '>', '#', "\uf0d8"]
    if mot in swl :
        return True
    Lc=[[],[]]
    indice=estimer_index(Ln_alpha,mot)
    for i in range (max(0,indice-10),min(len(Ln_alpha),indice+10)):
        MAX=0
        for j in range (min(len(Ln_alpha[i][0]),len(mot))):
            if Ln_alpha[i][0][j] == mot[j] :
                MAX+=1
            else :
                break 
        Lc[0].append(MAX)
        Lc[1].append(i)
    L=[[],[]]
    m=max(Lc[0])
    for i in range (len(Lc[0])):
        if Lc[0][i]==m:
            L[0].append(len(Ln_alpha[Lc[1][i]][0]))
            L[1].append(Lc[1][i])
    index=L[1][L[0].index(min(L[0]))]#indice 
    MOT=Ln_alpha[index][0]
    longmax=max(len(MOT),len(mot))
    #(mot,MOT)
    if m/longmax>=0.5+2.7**(-longmax**2/100)*0.3:
        return MOT
    else :
        return False


def normRH(Ln_chrono,Ln_alpha,rh_rarete,rh_voisin,mot): #range un mot normalisé dans la cléRH
    x=0
    motRH=normrh(Ln_chrono,Ln_alpha,mot)
    if motRH is False :#si le mot n'est pas dans Ln : ne modifie pas Ln
        return [rh_rarete,rh_voisin]
    rh_voisin.append(motRH)
    for i in range (len(rh_rarete)) :
        if rh_rarete[i][0] == motRH :
            rh_rarete[i][1]+=1
            return [rh_rarete,rh_voisin]
    rh_rarete.append([motRH,1])
    return [rh_rarete,rh_voisin]


def cleRH(Ln_chrono,Ln_alpha,RH):#renvoie une clé RH
    rh_rarete=[]
    rh_voisin=[]
    for i in RH :
        X=normRH(Ln_chrono,Ln_alpha,rh_rarete,rh_voisin,i)
        rh_rarete,rh_voisin=X[0],X[1]#modification terme par terme de la clé 
    return [rh_rarete,rh_voisin]


def scoring_rarete (rh_rarete , cle_rarete , Ln, n): #Ln est la BDD, requeteRH sous forme de liste de token, CV normalisé, n est le nombre de token jamais parsés dans la bdd
    score=0
    cle_rarete=sorted(cle_rarete)
    for i in rh_rarete:
        for j in range (len (cle_rarete)):
            if cle_rarete[j][0]==i[0]:
                indexLn=trouver_index(Ln,i[0])
                score+=abs(log10((Ln[indexLn][1]+1)/n))**2*cle_rarete[j][1]
                break
    return score/trouver_n(cle_rarete)


def scoring_voisin(cle_voisin,rh_voisin):
    poid=0
    cst=3
    for i in range (len(cle_voisin)):
        if cle_voisin[i] in rh_voisin :
            ref=[[],[]]
            x=rh_voisin.index(cle_voisin[i])#index du mot  dans la requete
            for j in range (max(0,x-cst ),min(len(rh_voisin),x+cst+1)) :
                if rh_voisin[j] in cle_voisin :
                    ref[0].append(rh_voisin[j])
                    ref[1].append(j)
            indexMot=ref[1][ref[0].index(cle_voisin[i])]
            for j in range (max(0,i-cst),min(len(cle_voisin),i+cst+1)):
                if cle_voisin[j] in ref[0]:
                    if cle_voisin[j]!=cle_voisin[i]:
                        poid+=1/(abs(abs(ref[1][ref[0].index(cle_voisin[j])]-indexMot)-abs(i-j))+1)
    return poid/len(cle_voisin)
    

def score (cle_rarete,cle_voisin,rh_voisin,rh_rarete,Ln):#score finale
    n=trouver_n(Ln)    
    scorev=scoring_voisin(cle_voisin,rh_voisin)
    scorer=scoring_rarete(rh_rarete,cle_rarete,Ln,n)
    print(scorer,scorev)
    return scorev*scorer


def trouver_n (Ln): #algo pas forcément utile : une bonne approximation suffit
    n=0
    for i in Ln:
        n+=i[1] 
    return n


def megascore(obj,rh_voisin,rh_rarete,nbx,n,rh_oblige=[]):
    Finale=[]
    L=[[],[],[]]#[[url],[score]]
    Ln = ClefGlobal.objects.all()
    for i in Ln:
        Ln = i.clef
    Ln = sorted(Ln)
    #print(len(Ln))
    for i in range(len(obj[0])):
        #if comparaison_liste(obj[2][i],rh_oblige) is True :
        L[0].append(obj[0][i])
        L[1].append(score(obj[1][i],obj[2][i],rh_voisin,rh_rarete,Ln))
        L[2].append(obj[2][i])
    for i in range (min(nbx,len(L[0]))):
        index=L[1].index(max(L[1]))
        Finale.append([L[0].pop(index),L[1].pop(index),correl(rh_voisin,L[2].pop(index))])
    return Finale


def megascoreSC(obj,rh_voisin,rh_rarete,nbx,n,rh_oblige=[]):
    Finale=[]
    L=[[],[],[]]#[[url],[score],[clevoisin]]
    Ln = ClefGlobal.objects.all()
    for i in Ln:
        Ln = i.clef
    Ln_alpha=sorted(Ln)
    for profil in obj :
        if rh_oblige!=[]:
            if logique_locale(rh_oblige,profil.ClefVoisin) is True :
                L[0].append(profil.url)
                L[1].append(score(profil.ClefTrate,profil.ClefVoisin,rh_voisin,rh_rarete,Ln_alpha))
                L[2].append(profil.ClefVoisin)
        else :
            L[0].append(profil.url)
            L[1].append(score(profil.ClefTrate,profil.ClefVoisin,rh_voisin,rh_rarete,Ln_alpha))
            L[2].append(profil.ClefVoisin)
    #print(len(L[0]))
    for i in range (min(nbx,len(L[0]))):
        index=L[1].index(max(L[1]))
        Finale.append([L[0].pop(index),L[1].pop(index),correl(rh_voisin,L[2].pop(index))])
    return Finale


def correl (requete,CV) :
    x=0
    for i in range (len(requete)):
        if requete[i] in CV:
            x+=1
    return x/len(requete)*100


def trouver_index(Ln,mot):
    x=0
    y=len(Ln)
    indice=int(y/2)
    while Ln[indice][0]!=mot :
        if sorted([Ln[indice][0],mot])[0]==mot:
            y=indice
        else :
            x=indice
        indice = int((x+y)/2)
    return indice


def scoring_vecteur (V1,req):
    s=0
    long1,long2=len(V1),len(req)
    if long1!=long2 :
        for i in range (long2-long1):
            V1.append(0)
    for i in range (long2):
        s+=abs(V1[i]-req[i])
    return s


def clusturing(obj,V_requete,nb=50):
    L=[[],[]]
    for vecteur in obj :
        L[0].append(vecteur.url)
        L[1].append(scoring_vecteur(vecteur.ClefVecteur,V_requete))
    Clust=[]
    for i in range (nb):
        indice=L[1].index(min(L[1]))
        L[1].pop(indice)
        Clust.append(L[0].pop(indice))
    return Clust


def vectorisation (cle_voisin,Ln):
    cle_vecteur=[]
    for i in range (len(Ln)):
        if Ln[i][0] in cle_voisin :
            cle_vecteur.append(1)
        else :
            cle_vecteur.append(0)
    return cle_vecteur


def tokenisation_CV (chaine):
    string=''
    Finale1=[]
    mail = 'NONE'
    Ref=['a','à','â','æ','á','ä','ã','å','ā','e','é','è','ê','ë','ę','ė','ē','r','z','t','y','ÿ','u','û','ù','ü','ú','ū','i','î','ï','ì','í','į','ī','o','ô','œ','ö','ò','ó','õ','ø','ō','º','p','q','s','d','f','g','h','j','k','l','m','w','x','c','ç','ć','č','v','b','n','ñ','ń','1','2','3','4','5','6','7','8','9','0','@','&','€','$','£','¥','₩','₽','-','.']
    for i in chaine:
        for j in i:
            if j in Ref:
                string+=j
            else:
                if string!='':
                    Finale1.append(string)
                string=''
        if string!='':
            Finale1.append(string)
        string=''
    final = []
    for i in Finale1 :
        if '.' in i :
            if '.' == i[-1] : 
                final.append(i[:len(i)-1])
            else :
                final.append(i)
                if '@' in i:
                    mail=i
        else:
            final.append(i)
    string=''
    Finale2=[]
    Ref=['a','à','â','æ','á','ä','ã','å','ā','e','é','è','ê','ë','ę','ė','ē','r','z','t','y','ÿ','u','û','ù','ü','ú','ū','i','î','ï','ì','í','į','ī','o','ô','œ','ö','ò','ó','õ','ø','ō','º','p','q','s','d','f','g','h','j','k','l','m','w','x','c','ç','ć','č','v','b','n','ñ','ń','1','2','3','4','5','6','7','8','9','0','@','&','€','$','£','¥','₩','₽','-']
    for i in chaine:
        for j in i:
            if j in Ref:
                string+=j
            else:
                if string!='':
                    Finale2.append(string)
                string=''
        if string!='':
            Finale2.append(string)
        string=''
    return Finale2,mail


def cle_obl (chaine,Ln_chrono,Ln_alpha):
    string=''
    i=0
    cle=[]
    groupe=[]
    Ref=['a','à','â','æ','á','ä','ã','å','ā','e','é','è','ê','ë','ę','ė','ē','r','z','t','y','ÿ','u','û','ù','ü','ú','ū','i','î','ï','ì','í','į','ī','o','ô','œ','ö','ò','ó','õ','ø','ō','º','p','q','s','d','f','g','h','j','k','l','m','w','x','c','ç','ć','č','v','b','n','ñ','ń','1','2','3','4','5','6','7','8','9','0','@','&','€','$','£','¥','₩','₽','-']
    while i<len(chaine) :
        #print(string)
        if chaine[i] in Ref :
            string+=chaine[i]
            i+=1
        elif chaine[i]==' ' and chaine[i-1] in Ref+[')',']']: 
            if string != '':
                cle.append(normrh1(Ln_chrono,Ln_alpha,string))
            i+=1
            string=''
            cle.append('{et}') 
        elif chaine[i]=='{':
            if string!='':
                cle.append(normrh1(Ln_chrono,Ln_alpha,string))
                string=''
            if cle[-1]=='{et}':
                cle[-1]='{ou}'
            else :
                if string!='':
                    cle.append(normrh1(Ln_chrono,Ln_alpha,string))
                string=''
                cle.append('{ou}')
            i+=4
        elif chaine[i]=='[':
            if string!='':
                cle.append(normrh1(Ln_chrono,Ln_alpha,string))
                cle.append('{et}')
            string=''
            i+=1
            while chaine [i]!=']':
                if chaine[i] in Ref :
                    string+=chaine[i]
                else :
                    if string!='':
                        groupe.append(normrh1(Ln_chrono,Ln_alpha,string))
                    string = ''
                i+=1
            if string!='':
                groupe.append(normrh1(Ln_chrono,Ln_alpha,string))
            cle.append(groupe)
            groupe,string=[],''
            i+=1
        elif chaine[i]=='(' or chaine[i]==')':
            if string!='':
                cle.append(normrh1(Ln_chrono,Ln_alpha,string))
            cle.append(chaine[i])
            i+=1
            string=''
        else:
            if string!='':
                cle.append(normrh1(Ln_chrono,Ln_alpha,string))
            i+=1
            string=''
    if string!='':
        cle.append(normrh1(Ln_chrono,Ln_alpha,string))
    return (cle)


def verif_obl(string):
    x,o,f=0,0,0  
    Ref=['a','‡','‚','Ê','·','‰','„','Â','a','e','È','Ë','Í','Î','e','e','e','r','z','t','y','ˇ','u','˚','˘','¸','˙','u','i','Ó','Ô','Ï','Ì','i','i','o','Ù','ú','ˆ','Ú','Û','ı','¯','o','∫','p','q','s','d','f','g','h','j','k','l','m','w','x','c','Á','c','c','v','b','n','Ò','n','1','2','3','4','5','6','7','8','9','0','@','&','Ä','$','£','•','?','?','-']
    while string[-1]==' ':#supprime les espaces en fin de requete
        string=string[:len(string)-1]
    while string[0]==' ':#supprime les espaces en fin de requete
        string=string[1:]
    while x<len(string):#supprime les elements non pris en compte
        if string[x] not in Ref+['{','}','(',')','[',']',' '] :
            #print(string[x])
            return 'erreur : la requete contient un caractËre non pris en charge'
        else :
            x+=1
    x=0
    while x<len(string):#supprime les espaces inutiles
        if string[x]==' ' and (string[x+1] in [' ','(',')','[',']','{','}'] or string[x-1] in [' ','(',')','[',']','{','}']):
            string=string[:x]+string[x+1:]
        else :
            x+=1
    x=0
    while x<len(string):#verifie si tous les jeux de crochets/accolades sont bien fermÈs
        if string[x]=='[':
            x+=1
            while x<len(string) and string[x]!=']':
                #print(string[x])
                if string[x] not in Ref+[' ']:
                    return 'Les crochets doivent se fermer avant de contenir des parenthËse ou accolades'
                else :
                    x+=1
            if string[x]!=']':
                return 'erreur'
            else :
                x+=1
        elif string[x]==']':
            return "les crochets doivent s'ouvrir avant de se fermer"
        elif string[x]=='{':
            if len(string)>x+4:
                if string[x+1]+string[x+2]+string[x+3]=='ou}':
                    x+=4
                else :
                    return 'erreur : pb accolade mal utilisÈe'
            else :
                return 'erreur : pb accolade mal utilisÈe '
        elif string[x]=='}':
            return "erreur : les accolades doivent s'ouvrir avant de se fermer"
        else :
            x+=1
    x=0
    while x<len(string):#verifier si une porte {ou} ne se situe pas n'importe ou
        if string[x]=='{':
            if x-1>0:
                if string[x]=='(':
                    return 'erreur : {ou} incomprÈhensible ou inutile'
            else :
                return 'erreur : {ou} incomprÈhensible ou inutile'
            if x+4<len(string):
                if string[x+4]==')':
                    return 'erreur : {ou} incomprÈhensible ou inutile'
            else :
                return 'erreur : {ou} incomprÈhensible ou inutile'
            x+=1
        else :
            x+=1
    x=0
    for i in string :#verifier si toutes les parenthese sont bien fermÈes ou ouvertes
        if i=='(':
            o+=1
        elif i==')':
            f+=1
    if o!=f:
        return "erreur : les parentheses doivent s'ouvrir et se fermer"
    return [string]


def logique_locale (liste,CV):
    while '(' in liste:
        for i in range (len(liste)):
            if liste[i]=='(':
                inf=i
            if liste[i]==')':
                sup=i
                liste[inf:sup+1]=[logique_locale(liste[inf+1:sup],CV)]
                break
    return operation_simple(liste,CV)


def operation_simple (liste,CV):
    #on vérifie si la lste est bien non vide
    if len(liste)==0:
        #sinon on renvoie vrai
        return True
    #on définit la variable currentBool comme la variable qui étape par étape 
    #vérifira si cle est vrai ou non
    currentBool=comparaison_liste(liste[0],CV)
    #on avant de deux pas en deux pas d'où le "2*" devant quasiment chaque "i"
    for i in range (1,int((len(liste)-1)/2+1)) :
        #on regarde si la connection entre deux bloc est un {et}...
        if liste[2*i-1]=='{et}':
            currentBool = currentBool and comparaison_liste(liste[2*i],CV)
        # ... ou un {ou}
        elif liste[2*i-1]=='{ou}':
            currentBool = currentBool or comparaison_liste(liste[2*i],CV)
    return currentBool


def comparaison_liste (objet,CV=1):
    x=0
    swl=['alors','au','aucuns','aussi','autre','avant','avec','avoir','bon','car','ce','cela','ces','ceux','chaque','ci','comme','comment','dans','des','du','dedans','dehors','depuis','devrait','doit','donc','dos','début','elle','elles','en','encore','essai','est','et','eu','fait','faites','fois','font','hors','ici','il','ils','je','juste','la','le','les','leur','là','ma','maintenant','mais','mes','mine','moins','mon','mot','même','ni','nommés','notre','nous','ou','où','par','parce','pas','peut','peu','plupart','pour','pourquoi','quand','que','quel','quelle','quelles','quels','qui','sa','sans','ses','seulement','si','sien','son','sont','sous','soyez','sujet','sur','ta','tandis','tellement','tels','tes','ton','tous','tout','trop','très','tu','voient','vont','votre','vous','vu','ça','étaient','état','étions','été','être', 'de', 'des', 'et', "d'", 'la', 'en', 'du', 'and', 'les', 'à', '-', "l'", 'of', "\uf0b7", 'sur', 'the', 'pour', '—', 'un', 'to', 'in', 'au', "\uf0a7", '<', '>', '#', "\uf0d8",2]
    #si le bloc est une liste alors...
    if type(objet) is list :
        #on supprime les mots de la stop word list
        i=0
        while i<len(objet) :
            if objet[i] in swl :
                objet.pop(i)
            else:
                i+=1
        if len(objet)==0:
            return True
        #on boucle sur le CV 
        for i in range (len(CV)-len(objet)) :
            #on boucle sur l'objet
            for j in range(len(objet)) :
                #on regarde si les elements concorde
                if objet[j]==CV[i+j]:
                    x+=1
                #sinon on sort de la boucle sur l'objet
                else :
                    x=0
                    break
            #si (apres avor bouclé sur l'objet) on atteind la taille de
            #l'objet c'est qu'on a bien la condition qui est vérifiée
            if x==len(objet) :
                return True 
        #sinon on renvoie False
        return False
    #si le bloc est un Booléen alors ...
    elif type(objet) is bool:
        #on revoie le Booléen (aucun traitement nécéssaire)
        return objet
    #sinon (c'est que c'est une chaine de caractère) alors ...
    else :
        #on regarde seulement si le mot est dans le CV
        if (objet in CV) or (objet in swl):
            return True
        #sinon on renvoie False
        return False


def placer_mot(Ln_alpha,mot):
    for i in range (len(Ln_alpha)):
        if sorted([Ln_alpha[i][0],mot])[0]==mot:
            Ln_alpha=Ln_alpha[:i]+[[mot,1]]+Ln_alpha[i:]
    return Ln_alpha

def concat(L1,L2):
    return L1+L2
