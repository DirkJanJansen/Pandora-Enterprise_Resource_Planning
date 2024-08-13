import re

def _11check(zoekterm):
    number = str(zoekterm)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False

def zt(zoekterm, valnr):
    if valnr == 1:
        #accountnr
        ab = re.compile("^([1]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 2:
        #artikelnr
        ab = re.compile("^([2]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 3:
        #leverancier
        ab = re.compile("^([3]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 4:
        #inkooporders
        ab = re.compile("^([4]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 5:
        #verkooporders
        ab = re.compile("^([5]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)  
    elif valnr == 6:
        #kopers
        ab = re.compile("^([6]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 7:
        #werkorder
        ab = re.compile("^([7]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 8:
        # Werknummer
        ab = re.compile("^([8]{1}[0-9]{8})+$")
        if ab.match(zoekterm) and _11check(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 9:   
        # Postcode
        ab = re.compile("^([0-9]{4}[A-Za-z]{2})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 10:
        #Datum jjjj-mm-dd
        if len(zoekterm) == 10:
            ab =  re.compile("^([12]{1}[019]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1})+$")
        elif len(zoekterm) == 9:  
            ab = re.compile("^([12]{1}[019]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1})+$")
        elif len(zoekterm) == 7:
            ab = re.compile("^([12]{1}[019]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1})+$") 
        elif len(zoekterm) == 4:
            ab = re.compile("^([12]{1}[019]{1}[0-9]{2})+$") 
        else:
            return(False)
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 11:
        #jaarweek jjjjww
        ab = re.compile("^([2]{1}[01]{1}[0-9]{2}[0-5]{1}[0-9]{1})+$") 
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 12:
        #e-mail
        ab = re.compile("^([A-Za-z._-]{1,}@(\\w+)(\\.(\\w+))(\\.(\\w+))?(\\.(\\w+))?)$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 13:
        #alle ID's integer
        ab = re.compile("^([1-9]{1}[0-9]{0,7})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 14:
        #alle bedragen of getallen float
        ab = re.compile("^[-+]?[0-9]*\.?[0-9]+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 15:
        #inkoop, verkoop, webverkoop, interne werken, externe werken
        ab = re.compile("^([45678]{1}[0-9]{8})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 16:
        #kostensoort
        ab = re.compile("^([1-9]{1})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 17:
        #clusters werken extern
        ab = re.compile("^([A-Ka-k]{1}[A-Za-z]{1}[0-9]{5})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 18:
        #voortgangstatus werken
        ab = re.compile("^([ABCDEFGHJabcdefghj])+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 19:
        #clusters werken intern
        ab = re.compile("^([LMOPRSTlmoprst]{1}[A-Ka-k]{1}[0-9]{5})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 20:
        #loonperiode jjjjmm
        ab = re.compile("^([2]{1}[01]{1}[0-9]{2}[-]{1}[01]{1}[0-9]{1})+$") 
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 21:
        #interne of externe werken        
        ab = re.compile("^([78]{1}[0-9]{8})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)   
    elif valnr == 22:
        #Direkt of Indirekt       
        ab = re.compile("^([DIdi]{1})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False) 
    elif valnr == 23:
        #loonschalen        
        ab = re.compile("^([0-9]{1,3}[-]{1}[0-9]{1,3})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False) 
    elif valnr == 24:
        #categorie loonuren 
        item = False
        if zoekterm.upper().startswith(('10','12','15','2','F','D','Z','V','E','R','G','O')):
            item = True
        return(item)
    elif valnr == 25:
        #zoekterm clusters werken intern 1e positie
        ab = re.compile("^([LMNOPRSTlmoprst]{1})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)
    elif valnr == 26:
        #zoekterm clusters werken extern 1e positie
        ab = re.compile("^([ABCDEFGHJKabcdefghjk]{1})+$")
        if ab.match(zoekterm):
            return(True)
        else:
            return(False)       