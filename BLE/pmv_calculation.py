# -*- coding: utf-8 -*-
from math import exp, log


#This module contains the following psychrometric functions:
#As configured here, pressures are expected in atmospheres and
#  relative humidities are expected as fractions, and
#  temperatures as °F
#FUNCTION               CALCULATES
#SatPress(T)            Saturation pressure
#SatTemp(Ps)            Saturation temperature
#HumRatRH(T,RH,PAtm)    Humidity ratio
#RelHum(T,W,PAtm)       Relative humidity
#Enthalpy(T,W)          Enthalpy
#DewPoint(W,PAtm)       Dew-point temperature
#WetBulb(T,W,PAtm)      Wet-bulb temperature
#SpecVol(T,W,PAtm)      Specific volume
#HumRatH(T,H)           Humidity ratio
#TempH(W,H)             Temperature
#RHTwb(T,TWB,PAtm)      Relative humidity
#HumRatTwb(T,TWB,PAtm)  Humidity ratio
#HfgWat(T)              Heat of vaporization of water
#TAdp(T1,W1,T2,W2,PAtm) Apparatus dew-point temperature for two specified points


NMol = 0.62198
RHMax = 1
tolRel = 0.000001
HfgRef = 1061.0
CpVap = 0.444
CpWat = 1.0
CpAir = 0.24
RAir = 0.02521
kPaMult = 101.325
TAbs = 459.67
TKelMult = 0.555556
TAmb = 70.0

def SatPress(TArg):
    _ret = None
    # Function to calculate saturation pressure of water vapor
    # Correlation from Hyland and Wexler (1983) using SI units.
    # Function returns pressure in user units according to constants
    # TAbs = multiplier to get absolute temperature in user units
    # TKelMult = multiplier to get K from user absolute temperature
    # kPaMult = multiplier to get Pascals from user pressure units
    #Define constants for vapor pressure correlations

    C1, C2, C3  = -5674.5359, -0.51523058, -0.009677843
    C4, C5, C6  = 0.00000062215701, 2.0747825E-09, -9.484024E-13
    C7, C8, C9, C10  = 4.1635019, -5800.2206, -5.516256, -0.048640239
    C11, C12, C13  = 0.000041764768, -0.000000014452093, 6.5459673


    T = ( TArg + TAbs )  * TKelMult
    # Use different correlations for pressure over ice or water
    if T < 273.15:
        kPa = exp(C1 / T + C2 + T * C3 + T * T *  ( C4 + T *  ( C5 + C6 * T ) )  + C7 * log(T))
    elif T >= 273.15:
        kPa = exp(C8 / T + C9 + T *  ( C10 + T *  ( C11 + T * C12 ) )  + C13 * log(T))
    _ret = kPa / kPaMult
    return _ret

def SatTemp(Ps):
    _ret = None
    # function to calculate saturation temperature from pressure
    TOld = TAmb
    POld = SatPress(TOld)
    TNew = TOld + 1
    while 1:
        T = TNew
        P = SatPress(T)
        slope = ( P - POld )  /  ( T - TOld )
        TNew = T -  ( P - Ps )  / slope
        if abs(P - Ps) < abs(POld - Ps):
            POld = P
            TOld = T
        if abs(TNew - T) < tolRel:
            break
    _ret = TNew
    return _ret

def HumRatRH(T, RH, PAtm):
    _ret = None
    # function to calculate humidity ratio from temperature
    # and relative humidity
    pw = SatPress(T) * RH / RHMax
    _ret = NMol * pw /  ( PAtm - pw )
    return _ret

def RelHum(T, W, PAtm):
    _ret = None
    # function to calculate relative humidity from temperature
    # and humidity ratio
    Pv = PAtm * W /  ( NMol + W )
    _ret = Pv / SatPress(T) * RHMax
    return _ret

def Enthalpy(T, W):
    _ret = None
    #Function to calculate moist air enthalpy
    _ret = CpAir * T + W *  ( HfgRef + CpVap * T )
    return _ret

def DewPoint(HumRat, PAtm):
    _ret = None
    # function to determine saturation temperature for given humidity ratio
    # and atmospheric pressure
    psw = PAtm * HumRat /  ( NMol + HumRat )
    _ret = SatTemp(psw)
    return _ret

def WetBulb(T, WDes, PAtm):
    _ret = None
    # Function to calculate wet-bulb temperature from dry-bulb
    # and humidity ratio
    Wsat = HumRatRH(T, RHMax, PAtm)
    TWBOld = T
    WOld = Wsat
    TWBNew = TWBOld - 1
    while 1:
        TWB = TWBNew
        WStar = HumRatRH(TWB, RHMax, PAtm)
        W = ( ( HfgRef -  ( CpWat - CpVap )  * TWB )  * WStar - CpAir *  ( T - TWB ) )  /  ( HfgRef + CpVap * T - CpWat * TWB )
        slope = ( W - WOld )  /  ( TWB - TWBOld )
        TWBNew = TWB -  ( W - WDes )  / slope
        if abs(W - WDes) < abs(WOld - WDes):
            WOld = W
            TWBOld = TWB
        if abs(( TWBNew - TWB )  / TWB) < tolRel:
            break
    _ret = TWB
    return _ret

def SpecVol(T, W, PAtm):
    _ret = None
    # Function to calculate specific volume of moist air mixture
    # ( calculates m3/kgda of mixture)
    pAir = NMol * PAtm /  ( NMol + W )
    _ret = RAir *  ( T + TAbs )  / pAir
    return _ret

def HumRatH(T, H):
    _ret = None
    # function to calculate humidity ratio from dry bulb
    # temperature and enthalpy
    _ret = ( H - CpAir * T )  /  ( HfgRef + CpVap * T )
    return _ret

def TempH(W, H):
    _ret = None
    # function to calculate temperature from humidity ratio and enthalpy
    _ret = ( H - W * HfgRef )  /  ( CpAir + CpVap * W )
    return _ret

def TempHRH(H, RH, PAtm):
    _ret = None
    #Calculates temperature from enthalpy and relative humidity
    YTarget = H
    XOld = TAmb
    YOld = Enthalpy(XOld, HumRatRH(XOld, RH, PAtm))
    XNew = XOld + 1
    while 1:
        X = XNew
        Y = Enthalpy(X, HumRatRH(X, RH, PAtm))
        slope = ( Y - YOld )  /  ( X - XOld )
        XNew = X -  ( Y - YTarget )  / slope
        if abs(Y - YTarget) < abs(YOld - YTarget):
            YOld = Y
            XOld = X
        if abs(XNew - X) / X < tolRel:
            break
    _ret = XNew
    return _ret

def RHTwb(T, TWB, PAtm):
    _ret = None
    # function to calculate relative humidity (%) from dry bulb
    # and wet bulb temperatures (celcius) and atmospheric pressure (kPa)
    psatDB = SatPress(T)
    Wsat = NMol * psatDB /  ( PAtm - psatDB )
    psatWB = SatPress(TWB)
    WStar = NMol * psatWB /  ( PAtm - psatWB )
    W = ( ( HfgRef -  ( CpWat - CpVap )  * TWB )  * WStar - CpAir *  ( T - TWB ) )  /  ( HfgRef + CpVap * T - CpWat * TWB )
    Pv = PAtm * W /  ( NMol + W )
    _ret = Pv / psatDB * RHMax
    return _ret

def HumRatTWB(T, TWB, PAtm):
    _ret = None
    # Function to calculate humidity ratio from dry bulb
    # and wet bulb temperatures
    RH = RHTwb(T, TWB, PAtm)
    _ret = HumRatRH(T, RH, PAtm)
    return _ret

def HfgWat(T):
    _ret = None
    # Function to calculate the heat of vaporization of pure water
    _ret = HfgRef -  ( CpWat - CpVap )  * T
    return _ret

def TAdp(T1, W1, T2, W2, PAtm):
    _ret = None
    # Function to calculate the bypass factor given two points on psychrometric chart
    # T = temperature (C)
    # W = humidity ratio
    SHRSlope = ( W1 - W2 )  /  ( T1 - T2 )
    RH1 = RelHum(T1, W1, PAtm)
    RH2 = RelHum(T2, W2, PAtm)
    TAdpOld = T1 -  ( RH1 - RHMax )  /  ( RH1 - RH2 )  *  ( T1 - T2 )
    WAdp = HumRatRH(TAdpOld, RHMax, PAtm)
    TAdpNew = T1 -  ( W1 - WAdp )  / SHRSlope
    ErrOld = TAdpNew - TAdpOld
    while 1:
        _ret = TAdpNew
        WAdp = HumRatRH(_ret, RHMax, PAtm)
        TAdpNew = T1 -  ( W1 - WAdp )  / SHRSlope
        Err = TAdpNew - _ret
        TAdpNew = _ret - Err *  ( _ret - TAdpOld )  /  ( Err - ErrOld )
        if abs(Err) < abs(ErrOld):
            ErrOld = Err
            TAdpOld = _ret
        if abs(Err) / TAmb < tolRel:
            break
    return _ret


#Constants independent of unit system
#Constants for English Units
#Note: constants currently configured for PAtm in atmospheres
#Constants for SI Units
#Note: constants currently configured for PAtm in atmospheres
#Public Const HfgRef = 2501000#  'heat of vaporization at 0C, J/kg
#Public Const CpVap = 1805#      'specific heat of water vapor, J/kg C
#Public Const CpWat = 4186#      'specific heat of liquid water, J/kg C
#Public Const CpAir = 1006#      'specific heat of dry air, J/kg C
#Const RAir = 0.002833           'gas constant for air, RAir*kPaMult*1000 = J/kg C
# if P in pascals RAir = 287.05 J/kg K
#Const kPaMult = 101.325         'multiplier to get kPascals from user pressure
#Public Const TAbs = 273.15      'add to user temperature to get absolute temp
#Const TKelMult = 1#             'multiplier to get Kelvin from user temp
#Const TAmb = 25#                'typical temperature in user units (initial value)
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################

#This module contains functions for predicting thermal comfort:
#As configured here, pressures are expected in atmospheres and
#  relative humidities are expected as fractions, and
#  temperatures as °F
#FUNCTION                        CALCULATES
#PMV(Ta,Tr,Wa,V,Icl,Met,Patm)    Predicted Mean Vote
#PPD(PMV)                        Percent People Dissatisfied
#


def PMV(Temperature = 22, Temperature_radiant = 22, Humidity = 40, V = 0.1, Icl = 0.5, Met = 1.1, PAtm = 1):
    #Function to evaluate Predicted Mean Vote
    #  from ASHRAE Handbook of Fundamentals (2001), based on Fanger (1982)
    #TA = air temperature, C
    #TR = mean radiant temperature, C
    #WA = humidity ratio
    #V = bulk air velocity, m/s
    #PAtm = atmospheric pressure, atm
    #Icl = insulation level of clothing, clo (1 clo = 0.155 m2.K/W = 0.88 ft2.F.h/Btu)
    #   walking shorts, short sleeve shirt                  0.36 clo
    #   trousers, short sleeve shirt                        0.57 clo
    #   trousers, long sleeve shirt                         0.61 clo
    #   trousers, long sleeve shirt, suit jacket            0.96 clo
    #   trousers, long sleeve shirt, t-shirt, sweater       1.01 clo
    #   skirt, short sleeve shirt, pantyhose                0.54 clo
    #   skirt, long sleeve shirt, slip, pantyhose           0.67 clo
    #   skirt, long sleeve shirt, slip, pantyhose, sweater  1.10 clo
    #   insulated coveralls, long underwear                 1.37 clo
    #Met = metabolic rate, met (1 met = 58.2 W/m2 = 18.4 Btu/h ft2)
    #   seated quietly                  1.0 met
    #   standing, relaxed               1.2 met
    #   typing                          1.1 met
    #   filing, standing                1.4 met
    #   office, walking about           1.7 met
    #   house cleaning                  2.0-3.4 met
    #   light machine work              2.0-2.4 met
    #   competitive wrestling           7.0-8.7 met

    WA = HumRatRH((Temperature * 1.8) + 32, Humidity/100.0, PAtm)

    TA = Temperature
    TR = Temperature_radiant

    work = 0
    M = Met * 58.2
    MW = M - work
    Rcl = Icl * 0.155
    fcl = 1.05 + 0.1 * Icl
    hc = 12.1 * V ** 0.5
    hr = 4.2
    TSk = 35.7 - 0.0275 * MW
    qSweat = 0.42 *  ( MW - 58.15 )
    WSatSk = HumRatRH(TSk * 1.8 + 32, 1, PAtm)
    qRespSen = 0.0014 * M *  ( 34 - TA )
    qRespLat = 2.78 * M *  ( 0.0365 - WA )
    qEvapDiff = 491 *  ( WSatSk - WA )
    Tcl = ( TSk + Rcl * fcl *  ( hc * TA + hr * TR ) )  /  ( 1 + Rcl * fcl *  ( hc + hr ) )
    if Tcl < TA:
        Tcl = TA
    hc1 = 2.38 *  ( Tcl - TA )  ** 0.25
    hc2 = 12.1 * V ** 0.5
    if hc1 > hc2:
        hc = hc1
    else:
        hc = hc2
    Tcl = ( TSk + Rcl * fcl *  ( hc * TA + hr * TR ) )  /  ( 1 + Rcl * fcl *  ( hc + hr ) )
    L = MW - fcl * hr *  ( Tcl - TR )  - fcl * hc *  ( Tcl - TA )  - qEvapDiff - qSweat - qRespSen - qRespLat
    pmv = L *  ( 0.303 * exp(- 0.036 * M) + 0.028 )
    return pmv

def PPD(pmv):
    #Function to calculate percent of people dissatisfied from predicted mean vote
    ppd = 100 - 95 * exp(- ( 0.03353 * pmv ** 4 + 0.2179 * pmv ** 2 ))
    return ppd
