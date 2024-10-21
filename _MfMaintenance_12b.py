#
# - IZLAZNI FAJL: _Rezultat.csv

# Parse Makefile files. Online regex:
# https://regex101.com/
# https://regexr.com/


import re
#import string
import sys
import os
#from csv import writer
from collections import defaultdict
from datetime import datetime


num_columns = 1
temp_fajl_lista = 'temp.csv'
____rezultat_csv_fajl = '_Rezultat.csv'
lista_red_promenljive = None

mejkfajl_sa_putanjom = None  # global
ulazni_mejkfajl = None  # global

_lista_mejkfajlova = [] # include makefile

_recnik_PROMENLJIVIH = dict() # 1MK:1pr
_recnik_IZMENJENIH = dict() # 1MK:[pr1 pr2 pr3]
#izmene_promenljivih_LISTA = []
_recnik_KORISCENJA = dict() # MK:[pr1 pr2 pr3]
#koriscenje_promenljivih_LISTA = []
_defdict_IZMENJENIH = defaultdict(list)
_defdict_KORISCENIH = defaultdict(list)


_temp_RecniK_IZMENJENIH = dict()
_set_MK_koji_MENJAJU = set()
_set_MK_koji_KORISTE = set()


__tabela_izmena = dict()
__tabela_koriscenja = dict()

# Otvara ulazni mejkfajl
broj_mejkfajlova = len(sys.argv)

if not sys.argv[1:]:
    print('\n**** Unesite mejkfajl kao argument! ***')
    sys.exit(2)


# CSV: ______________________________

def obrisi_csv_fajl(fajl):
    if fajl:
        f = open(fajl, "w+")
        f.close()




# TEMP: za ispomoc. Koristi se funkcija: UPIS U RECNIK(KLJUC:VREDNOST)
def upisi_red_u_temp_fajl(naziv_promenljive, mejkfajl, oznaka):
    mk = os.path.basename(mejkfajl)
    #print('     ', mk, ', ', oznaka, '\n')
    f = open('temp.csv', 'a+')
    f.write(str(naziv_promenljive))
    f.write(';')
    f.write(oznaka)
    f.write(';')
    f.write(mk)
    f.write('\n')
    f.close()


def ____upisi_u_csv_fajl(___interna_tabela):
    f = open(____rezultat_csv_fajl, 'a+')
    f.write(str(___interna_tabela))
    f.write('\n')
    f.close()
    return True


#
#
# .csv kraj ______________________________________________________________


#
#
# RECNICI: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# RECNIK DEFINICIJA:
# 1P -> 1Mk
def _upisi_u_recnik_DEFINICIJA(promenljiva, mejkfajl):
    #global _recnik_PROMENLJIVIH
    _recnik_PROMENLJIVIH[promenljiva] = mejkfajl
    print('>>>>>>>> _recnik_PROMENLJIVIH--->> dodaje:\n  ',promenljiva,' -> ', os.path.basename(mejkfajl) )




# RECNIK IZMENA: __________________________________

def _upisi_u_defdict_IZMENJENIH(promenljiva,mejkfajl):
    _defdict_IZMENJENIH[mejkfajl].append(promenljiva)
    #print('\n_defdict_IZMENJENIH:\n', _defdict_IZMENJENIH)


# SET ne dozvoljava ponovljene vrednosti.
def __popisi_mk_koji_menjaju_ovu_p(promenljiva):
    for red in _defdict_IZMENJENIH.items(): # [0] - mk : [1] - LISTA p
        #print('>>>> IZMENJENI: \n', _defdict_IZMENJENIH)
        for p in red[1]: # promenljive
            if p == promenljiva:
                _set_MK_koji_MENJAJU.add(red[0])





# RECNIK  KORISCENJA: __________________________________


def _upisi_u_defdict_KORISCENIH(promenljiva,mejkfajl):
    _defdict_KORISCENIH[mejkfajl].append(promenljiva)


# SET ne dozvoljava ponovljene vrednosti.
def __popisi_mk_koji_koriste_ovu_p(promenljiva):
    # print('>>>> KORISCENE: \n', _defdict_KORISCENIH)
    for red in _defdict_KORISCENIH.items(): # [0] - mk : [1] - LISTA p
        for p in red[1]: # red[1] - lista promenljivih
            if p == promenljiva:
                _set_MK_koji_KORISTE.add(red[0]) # lista MK koji menjaju ovu prom.
    #print('>>> SET MK KOJI KORISTE\n    ', _set_MK_koji_KORISTE)
# recnici kraj _________________________________________________________


# NE KORISTI SE.
#   ZA SVAKI MEJKFAJL:
def __upisi_u_INTERNU_TABELU():
    print('\n****************************************\n')
    print('\n<<<< DICTIONARY UMESTO TABELE.\n')
    print('.\n')
    # print('\n- Fajl temp.csv je samo za pregled.')
    print('.*****************************************************************\n')


# ______________________________________________________________________
def rutine_izlaza(kod_izlaza):
    print('\nUsage: ....')
    sys.exit(kod_izlaza)

# ______________________________________________________________________

def _popisi_mejkfajlove_():

    if sys.argv[1] == '--help':
        rutine_izlaza(0)
    else:
        #try:
            for arg in sys.argv[1:]:
                if os.path.isfile(arg):
                    _lista_mejkfajlova.append(arg)
                else:
                    rutine_izlaza(1)
        #except:
        #    rutine_izlaza(1)



   

def pronadji_included_mk(linija):
    # include makefile.mk. Trazi: include
    reg_included_mk = re.compile(r'(include)\s+(\w+.mk)')
    pronadjen_mk = reg_included_mk.search(linija)
    if pronadjen_mk:
        print("\n>>> REGEX PRONADJENO: include >makefile<\n\n      ",
              pronadjen_mk.group())
        naziv_majekfajla = pronadjen_mk.group(2)
        return naziv_majekfajla


# PRVA FUNKCIJA. TRAZI DEFINICIJE PROMENLJIVIH.
def pronadji_def_promenljivu(linija):
    # PRVO PRAVILO DEF. Trazi: naziv_prom := nesto
    reg_def_prom = re.compile(r'(^[^0-9]\w+)\s*:=\s*[^$\(\w\)]')
    pronadjena_prom = reg_def_prom.search(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADJENO: DEFINICIJA: naziv := nesto\n\n   ",
              pronadjena_prom.group())
        naziv_promenljive = pronadjena_prom.group(1)
        return naziv_promenljive.lstrip()

    # DRUGO PRAVILO DEF. Trazi: define naziv_prom kojesta
    reg_def_prom = re.compile(r'(define)\s*([^0-9]\w+)')
    pronadjena_prom = reg_def_prom.search(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADJENO: DEFINICIJA: define naziv kojesta\n\n ",
              pronadjena_prom.group())
        naziv_promenljive = pronadjena_prom.group(2)
        return naziv_promenljive

    # TRECE PRAVILO DEF. Trazi:     naziv_prom = nesto
    reg_def_prom = re.compile(r'(^[^0-9]\w+)\s*=\s*[^\$\(\w\)]\w+')
    pronadjena_prom = reg_def_prom.search(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADJENO: DEFINICIJA: naziv = nesto\n\n    ",
              pronadjena_prom.group())
        naziv_promenljive = pronadjena_prom.group(1)
        return naziv_promenljive

    # CETVRTO PRAVILO DEF. Trazi: naziv_prom ?= nesto
    reg_def_prom = re.compile(r'([^0-9]\w+)\s*\?=\s*[\w./]*')
    pronadjena_prom = reg_def_prom.search(linija) #findall(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADJENO: DEFINICIJA: naziv ?= nesto\n\n   ",
              pronadjena_prom.group())
        naziv_promenljive = pronadjena_prom.group(1)
        return naziv_promenljive

    return None


# DRUGA FUNKCIJA. Izmena promenljive.
def pronadji_izm_promenljivu(linija):

    # PRVO PRAVILO IZMENE. NAZIV += NESTO
    reg_izm_prom = re.compile(r'([^0-9]\w+)\s*\+=\s*[^$\(\w\)]')  
    pronadjena_prom = reg_izm_prom.search(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADJENO: IZMENA: naziv += nesto\n\n    ", pronadjena_prom.group(1))
        naziv_promenljive = pronadjena_prom.group(1)
        return naziv_promenljive


    # DRUGO PRAVILO IZMENE.     NAZIV = KOJESTA $(NAZIV) KOJESTA:
    reg_izm_prom = re.compile(
        r'(^[^0-9]\w+)\s*=\s*[\w\-\s]*\s*\$+(\([^0-9]\w+\))')
    pronadjena_prom = reg_izm_prom.search(linija)
    if pronadjena_prom:
        print("\n>>> REGEX PRONADEJENO: IZMENA: naziv = kojesta $(naziv) kojesta\n\n    ",
              pronadjena_prom.group())
        naziv_promenljive = pronadjena_prom.group(1)
        return naziv_promenljive
    return None

 

# TRECA FUNKCIJA. Koriscenje promenljive.
def pronadji_kor_promenljive(linija): # niz
    # PRAVILO KORISCENJА.    NESTO $(NAZIV) KOJESTA
    niz_koriscenih = re.findall(r'\$+(\([^0-9]\w+\))', linija)
    niz_koriscenih_format = []
    for prom in niz_koriscenih:
        prom = prom[1:]
        prom = prom[:-1]
        niz_koriscenih_format.append(prom)

    if niz_koriscenih_format:
        print("\n>>> REGEX PRONADEJENO: KORISCENJE: nesto $(PROM) kojesta\n\n    ",
              niz_koriscenih_format[0])
        return niz_koriscenih_format
        #print(' FINDALL \n  ', re.findall(r'\$+(\([^0-9]\w+\))', linija))
    else:
        return None



# ----------------------------------------------------------------------

def test():
    obrisi_csv_fajl(temp_fajl_lista)  # AKO POSTOJI OD RANIJE
    obrisi_csv_fajl(____rezultat_csv_fajl)

    f = open(____rezultat_csv_fajl, 'a+')
    f.write('Variabla;Definisana;Izmenjena;Koriscena\n')
    f.close()

    f = open(temp_fajl_lista, 'a+')
    f.write('Variabla;Primena;Mejkfajl\n')
    f.close()

    # ----------------------------------------------------------------
    # PRVI DEO:
    #       POPIS SVIH POJAVA PROMENLJIVIH u pomocne liste:


    ## 1. popis mejkfajlova:

    _popisi_mejkfajlove_() # u listu[]



    ## 2. popis promenljivih u liste:
    for mk in _lista_mejkfajlova:
        base = os.path.basename(mk)
        extension = os.path.splitext(os.path.abspath(mk))
        #extension = os.path.abspath(arg).rpartition(".")[-1]
        if extension[1] == '.mk':
            print(
                '\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            print('\n',base, '\n           ', os.path.abspath(mk), '\n')
            print('\n> trazi:   \n')
            mejkfajl_sa_putanjom = os.path.abspath(mk)  # = base

# >>>>>>>>  ZA OVAJ MEJKFAJL.
            v = _popisi_promenljive_mejkfajla_u_recnike(mejkfajl_sa_putanjom)
            if v:
                print(v)

            #print('>>>> IZMENJENI: \n', _defdict_IZMENJENIH)

# >>>>>>>>  UPISI RED U RECNIK IZMENJENIH.
            #       upisi_u_RECNIK_IZMENJENIH(mejkfajl_sa_putanjom)
            #       _lista_IZMENJENIH.clear()


        else:
            #print(mk, 'is not a Makefile file')  # ...
            rutine_izlaza(1)


    # POPISANE SU SVE P DEF I IZM I KOR OVOG MK.
    #

    # ----------------------------------------------------------------
    # DRUGI DEO:

    #t = __upisi_u_INTERNU_TABELU()
    #if t:
    #    print(t)

    # ----------------------------------------------------------------

    # TRECI DEO: REZULTAT.


    for red_promenljive_def in _recnik_PROMENLJIVIH.items():

        #___red_csv = red_promenljive_def[0]  # [0] promenljiva;
        ___red_csv = red_promenljive_def[0]  # [0] promenljiva;

        ___red_csv += ';'

        ___red_csv += os.path.basename(red_promenljive_def[1])  # [1] mejkfajl koji definise

        ___red_csv += ';'

        # IZMENE: mk koji menjaju ovu p >>>
        __popisi_mk_koji_menjaju_ovu_p(red_promenljive_def[0]) # [0] promenljiva
        ___red_csv += ','.join(str(os.path.basename(s)) for s in sorted(_set_MK_koji_MENJAJU))
        _set_MK_koji_MENJAJU.clear()#_defdict_IZMENJENIH


        ___red_csv += ';'


        # KORISCENJE: mk koji koriste ovu p >>>
        __popisi_mk_koji_koriste_ovu_p(red_promenljive_def[0])  # red[0] - promenljiva
        ___red_csv += ','.join(str(os.path.basename(s)) for s in sorted(_set_MK_koji_KORISTE))
        _set_MK_koji_KORISTE.clear()  # _defdict_KORISCENIH

        #___red_csv += ';'

        #print('\n CEO RED ZA UPIS:\n     ',  ___red_csv)

        r = ____upisi_u_csv_fajl(___red_csv)


# KRAJ...................................................................



# POPISUJE PO SVIM LINIJAMA JEDNOG MEJKFAJLA:
def _popisi_promenljive_mejkfajla_u_recnike(ulazni_mejkfajl):
    promenljive = {} #.. brisi
    fajl = open(ulazni_mejkfajl, 'r')


    def continuation_lines(fin):
        for line in fin:

            if line[0] == '#': # brise komentar
                continue
            line = line.rstrip('\n')
            while line.endswith('\\'):
                line = line[:-1] + next(fin).rstrip('\n')
            yield line


    while True:
        try:

            #global _lista_IZMENJENIH

            with open(ulazni_mejkfajl) as mejkfajl:

                for linija_mejkfajla in continuation_lines(mejkfajl):
                    if linija_mejkfajla:

                        # 0. TRAZI INCLUDED makefile:
                        ukljucen_mejkfajl = pronadji_included_mk(linija_mejkfajla)
                        if ukljucen_mejkfajl:
                            if ukljucen_mejkfajl not in _lista_mejkfajlova:
                                _lista_mejkfajlova.append(ukljucen_mejkfajl)
                            #print('LISTA MK: \n ', _lista_mejkfajlova)
                            continue

                        # 1. TRAZI DEFINICIJE:
                        naziv_def_promenljive = pronadji_def_promenljivu(linija_mejkfajla)
                        if naziv_def_promenljive:
                            upisi_red_u_temp_fajl(naziv_def_promenljive, ulazni_mejkfajl, 'def')
                            _upisi_u_recnik_DEFINICIJA(naziv_def_promenljive, ulazni_mejkfajl)
                            #_lista_def_promenljilve += naziv_def_promenljive
                            #continue

                        # 2. TRAZI IZMENE:
                        naziv_izm_promenljive = pronadji_izm_promenljivu(linija_mejkfajla)
                        if naziv_izm_promenljive:
                            upisi_red_u_temp_fajl(naziv_izm_promenljive, ulazni_mejkfajl, 'izm')
                            _upisi_u_defdict_IZMENJENIH(naziv_izm_promenljive,ulazni_mejkfajl)
                            #continue # isti red moze i da menja i da koristi: VAR1 = ...$(VAR2)...


                        # 3. TRAZI KORISCENJE:
                        # niz
                        niz_kor_promenljivih = pronadji_kor_promenljive(linija_mejkfajla)
                        if niz_kor_promenljivih:
                            #print('prom niz: \n ', niz_kor_promenljivih)
                            for prom in niz_kor_promenljivih:
                                upisi_red_u_temp_fajl(prom, ulazni_mejkfajl, 'kor')
                                _upisi_u_defdict_KORISCENIH(prom, ulazni_mejkfajl)
                            #print('>>> DEFDICT KOR:\n   ', _defdict_KORISCENIH)
                            #continue


        finally:
            fajl.close()
            return promenljive


if __name__ == '__main__':
    test()
