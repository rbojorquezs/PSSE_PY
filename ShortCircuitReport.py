# -*- coding: utf-8 -*-
"""  Get shortcircuit levels report from .SAV case
    12/09/25
 
    Eng. Roberto Bojorquez
    robertobojorquez55@gmail.com
 
"""
 
# Librerias
import os
import sys
import datetime
from math import sqrt
 
# Inicializar PSSE V_35
pssepy_PATH = r'C:\Program Files\PTI\PSSE36\36.3\PSSPY313'
sys.path.append(pssepy_PATH)
import psse36 # type: ignore
import psspy # type: ignore
psspy.psseinit()
import pssplot # type: ignore
import dyntools # type: ignore
import pssarrays # type: ignore
 
# Declarar variables default
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s=psspy.getdefaultchar()
 
 
# Función para calcular el nivel de cortocircuito según IEC 60909 en el PoI
def SC_IEC():
    rlst = pssarrays.iecs_currents(
    sid=1,               # your subsystem id; define with psspy.bsys if all=0
    all=1,               # 1 = all buses; set 0 if you defined SID above
    flt3ph=1,            # include 3φ faults
    fltlg=0,             # omit LG
    fltllg=0,            # omit LLG
    fltll=0,             # omit LL
    fltloc=0,            # 0 = fault at network bus
    linout=0,            # omit line-out faults
    linend=0,            # omit line-end faults
    tpunty=1,            # set transformer taps = 1.0 pu and phase shift = 0°
    lnchrg=0,            # leave line charging as-is (represented in sequences)
    shntop=0,            # leave shunts/magnetizing as-is (represented)
    dcload=0,            # DC/FACTS blocked
    zcorec=0,            # do not apply zero-seq transformer Z corrections
    optnftrc=2,          # use user-specified voltage factor C
    loadop=1,            # set loads to 0.0 in +/− seq
    genxop=0,            # use subtransient for sync machines (IEC mode ignores ZSOURCE here)
    brktime=0.083333,    # 5 cycles @ 60 Hz
    vfactorc=1.10,       # C = 1.10 (used because optnftrc=2)
    iecfil='',           # optional .iec file path, '' for none
    fcdfil='',           # optional .fcd control file, '' for none
    scfile=''            # optional .sc output file, '' for none
    )
 
    names = get_buses_name()[0]
    vbase = get_buses_basekv()[0]  # Voltage base per bus (list)
    numbers = rlst.fltbus
    mvabase = 100  # MVA base
 
    numbers = rlst.fltbus
    mvabase = 100  # MVA base
 
    # Empareja número, nombre, I [A] y MVA
    bus_list = []
    for idx, (num, name) in enumerate(zip(numbers, names)):
        try:
            v_base = vbase[idx]
            i_pu = rlst.flt3ph[idx].ia1  # Corriente en pu (compleja)
            i_base = mvabase * 1e6 / (sqrt(3) * v_base * 1e3)  # Vbase en kV, pasa a V
            i_actual = (abs(i_pu) * i_base)/1000
            mva = v_base * (i_actual*1000) * sqrt(3) / 1e3  # v_base en kV, i_actual en A, resultado en MVA
            bus_list.append((num, name.strip(), i_actual, mva))
        except Exception as e:
            print(f"Error en bus {num}: {e}")
 
    print("Num | Nombre      | I [kA]    | MVA")
    for num, name, i_actual, mva in bus_list:
        print(f"{num:3} | {name:12} | {i_actual:8.1f} | {mva:8.2f}")
 
def get_buses_name():
    #psspy.bsys()
    ierr, carray = psspy.abuschar(-1, 1, 'NAME')
    return carray
 
def get_buses_basekv():
    ierr, rarray = psspy.abusreal(-1, 1, 'BASE')
    return rarray
 
 
CASE = r"C:\Users\rober\Desktop\Constitucion\Constitucion.sav" # Ruta de caso de estudio .sav
psspy.case(CASE)
SC_IEC()