#!/usr/bin/env python
# Part of TotalDepth: Petrophysical data processing and presentation
# Copyright (C) 1999-2012 Paul Ross
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
# Paul Ross: apaulross@gmail.com
"""Tests ...

Created on Jan 12, 2012

@author: paulross
"""

__author__  = 'Paul Ross'
__date__    = '2011-08-03'
__version__ = '0.1.0'
__rights__  = 'Copyright (c) 2012 Paul Ross.'

#Paul-Rosss-MacBook-Pro:LAS paulross$ python3 ReadLASFiles.py ../../../HgIgnore/PyParsing/LAS/
#Cmd: ReadLASFiles.py ../../../HgIgnore/PyParsing/LAS/
#ReadLASFiles:
#   Files:         27
#  Errors:          0
#Critical:          0
#Files OK:         27
#   Bytes:   20914361 (19.9455 Mb)
#Sections:        134
#  Frames:     137499
#    Data:    1894450 (1.80669 M)
#  CPU time =    1.831 (S)
#Exec. time =    1.831 (S)
#Bye, bye!
#Paul-Rosss-MacBook-Pro:LAS paulross$

#: Descriptions for each mnemonic based on a study of the popularity of 27 files. 
MNEM_DESCRIPTION = {
    "AC"   : "Acoustic Travel Time",
    "AHV"  : "Annular Volume Mark",
    "API"  : "Api Number",
    "BHT"  : "Bottom Hole Temperature",
    "BHV"  : "Bore Hole Volume Mark",
    "BLI"  : "Bottom Logged Interval",
    "BS"   : "Bit Size",
    "C13"  : "Caliper Arms 1 & 3",
    "C24"  : "Caliper Arms 2 & 4",
    "CAL"  : "Caliper",
    "CAL1" : "Caliper 1",
    "CALI" : "Caliper",
    "CBD"  : "Casing Bottom Driller 1",
    "CBL"  : "Casing Bottom Logger 1",
    "CDD"  : "Casing Depth-Driller",
    "CDL"  : "Casing Depth-Logger",
    "CGR"  : "Gamma Ray Contribution From Thorium And Potassium",
    "CILD" : "Calibrated Induction Deep Conductivity",
    "CNC"  : "Corrected Neutron Porosity From Cn",
    "CNTY" : "County",
    "COMP" : "Company Name",
    "COUN" : "County",
    "CS"   : "Casing Size",
    "CTRY" : "Country",
    "DATE" : "Date",
    "DD"   : "Total Depth-Driller",
    "DEPT" : "Depth Curve",
    "DFD"  : "Drilling Fluid Density",
    "DFL"  : "Digitialy Focused Laterolog",
    "DFPH" : "Drilling Fluid Ph",
    "DFT"  : "Drilling Fluid Type",
    "DFV"  : "Drilling Fluid Viscosity",
    "DL"   : "Total Depth-Logger",
    "DMF"  : "Drilling Measured From",
    "DPHI" : "Density Porosity",
    "DRHO" : "Density Correction",
    "DT"   : "Delta-T (Also Called Slowness Or Interval Transit Time)",
    "EDF"  : "Elevation, Derrick Floor",
    "EDPH" : "Evr Density Porosity",
    "EGL"  : "Elevation, Ground Level",
    "EGR"  : "Egr",
    "EKB"  : "Elevation, Kelly Bushing",
    "ENGI" : "Logging Engineer'S Name",
    "ENPH" : "Evr Neutron Porosity",
    "EPD"  : "Elevatation Of Permanent Datum",
    "EPE"  : "Evr Photo-Electric Factor",
    "ERHO" : "Evr Bulk Density",
    "ERPO" : "Error Potassium",
    "ERTH" : "Error Thorium",
    "ERUR" : "Error Uranium",
    "FEXP" : "Cementation Exponent Archies (M)",
    "FL"   : "Field Location",
    "FLD"  : "Field Name",
    "FNUM" : "Tortuosity Constant Archies (A)",
    "GKCL" : "Gamma Kcl",
    "GKUT" : "Gamma Kut",
    "GR"   : "Gamma Ray",
    "GR4"  : "Gamma Ray 4",
    "GRD"  : "Gamma Ray",
    "GRK"  : "Gamma Potassium",
    "GRKT" : "Gamma Kt",
    "GRTH" : "Gamma Thorium",
    "GRTO" : "Total Gamma (150Kev - 3Mev)",
    "GRUR" : "Gamma Uranium",
    "HDCN" : "High Res Deep Conductivity",
    "HDRS" : "High Res Deep Resistivity",
    "HMRS" : "High Res Medium Resistivity",
    "ILD"  : "Induction Deep Resistivity",
    "ILM"  : "Induction Medium Resistivity",
    "ITT"  : "Integrated Travel Time Mark",
    "ITTT" : "Integrated Travel Time Total",
    "LMF"  : "Logging Measured From",
    "LOC"  : "Location",
    "LOC1" : "Quarters",
    "LOC2" : "Footages",
    "LOGM" : "Logging Direction",
    "LUL"  : "Equipment Location",
    "LUN"  : "Logging Unit Number",
    "MATR" : "Neutron Matrix (0=Lime,1=Sand,2=Dolo)",
    "MCSS" : "Mud Cake Sample Source",
    "MCST" : "Mud Cake Sample Temperature",
    "MDEN" : "Logging Matrix Density",
    "MFSS" : "Mud Filtrate Sample Source",
    "MFST" : "Mud Filtrate Sample Temp",
    "MINV" : "Microinverse Resistivity",
    "MNOR" : "Micronormal Resistivity",
    "MRT"  : "Maximum Recorded Temperature",
    "MSFD" : "Micro Focused Resistivity",
    "MSFL" : "Micro Focused Resistivity",
    "MSS"  : "Mud Sample Source",
    "MST"  : "Mud Sample Temperature",
    "NOIS" : "Spectral Noise",
    "NPHI" : "Neutron Porosity",
    "NULL" : "Null Value",
    "OS1"  : "Other Services Line 1",
    "PD"   : "Permanent Datum",
    "PE"   : "Photo-Electric Factor",
    "PEF"  : "Photoelectric Factor",
    "PORA" : "Porosity From Acoustilog",
    "PORZ" : "Porosity From Z-Densilog",
    "POTA" : "Potassium",
    "PROV" : "State",
    "QL"   : "Sdl Quality Long",
    "QS"   : "Sdl Quality Short",
    "RANG" : "Range",
    "RFOC" : "Resistivity From Cfoc",
    "RHOB" : "Bulk Density",
    "RILD" : "Resistivity From Cild",
    "RILM" : "Resistivity From Cilm",
    "RLML" : "Resistivity Of 1\" Lateral",
    "RM"   : "Mud Sample Resistivity",
    "RMB"  : "Resistivity Of Mud - Bht",
    "RMBH" : "Mud Resistivity At Bht",
    "RMC"  : "Mud Cake Resistivity",
    "RMCS" : "Mud Cake Source",
    "RMCT" : "Rmc Temperature",
    "RMF"  : "Mud Filtrate Resistivity",
    "RMFS" : "Mud Filtrate Source",
    "RMFT" : "Rmf Temperature",
    "RMS"  : "Mud Sample Source",
    "RMT"  : "Rm Temperature",
    "RNML" : "Resistivity Of 2\" Normal",
    "RUN"  : "Run Number",
    "RXRT" : "Rxo Rt Ratio",
    "SDT2" : "Delta T (2 Foot)",
    "SECT" : "Section",
    "SFLA" : "Sfl Resistivity Averaged Over 2.5 Feet",
    "SFLU" : "Sfl Resistivity Unaveraged",
    "SGR"  : "Spectroscopy Gamma Ray",
    "SON"  : "Service Order Number",
    "SP"   : "Spontaneous Potential",
    "SPHI" : "Sonic Porosity",
    "SRVC" : "Service Company",
    "STAT" : "State",
    "STEP" : "Depth Increment",
    "STOP" : "Bottom Depth",
    "STRT" : "Top Depth",
    "TCS"  : "Time Circulation Stopped",
    "TDD"  : "Drillers Depth",
    "TDL"  : "Loggers Depth",
    "TENS" : "Line Tension",
    "THOR" : "Thorium",
    "TLAB" : "Time Logger At Bottom",
    "TLI"  : "Top Logged Interval",
    "TOWN" : "Township",
    "URAN" : "Uranium",
    "UWI"  : "Unique Well Id",
    "VERS" : "Cwls Log Ascii Standard - Version 2.0",
    "WELL" : "Well Name",
    "WITN" : "Witness'S Name",
    "WRAP" : "One Line Per Depth Step",
}

#ReadLASFiles:
#   Files:       1211
#  Errors:          1
#Critical:          0
#Files OK:       1210
#   Bytes:  405697513 (386.903 Mb)
#Sections:       6102
#  Frames:    3978196
#    Data:   33823991 (32.2571 M)
#  CPU time =   57.721 (S)
#Exec. time =   60.162 (S)
#Bye, bye!
#Paul-Rosss-MacBook-Pro:LAS paulross$ 
#Paul-Rosss-MacBook-Pro:LAS paulross$ python3 ReadLASFiles.py ../../../../TDTestData/LAS/uz_med/
#Cmd: ReadLASFiles.py ../../../../TDTestData/LAS/uz_med/
#2012-01-18 08:58:25,930 ERROR    File: "../../../../TDTestData/LAS/uz_med/1001179028.las", Error: Line [96] array overflow; frame length 42 which should be length 41

#: Curve descriptions from a study of numerous LIS Files
CURVE_DESCRIPTION = {
    "AC"       : "Ac",
    "AC01"     : "Ac01",
    "AC02"     : "Ac02",
    "AC03"     : "Ac03",
    "AC04"     : "Ac04",
    "AC1"      : "Ac1",
    "AC2"      : "Ac2",
    "AC3"      : "Ac3",
    "ACAPL"    : "Porosity",
    "ACCL1"    : "Density Caliper",
    "ACCL2"    : "Neutron Caliper",
    "ACGR"     : "Gamma Ray",
    "ACQ"      : "['Acq', 'Acoustic Quality Indicator']",
    "ACQ1"     : "Acq1",
    "ACQ2"     : "Acq2",
    "ACSP"     : "Spontaneous Potential",
    "ACTC"     : "Sonic Interval Transit Time (Compensated)",
    "ACTC01"   : "Sonic Interval Transit Time (Compensated)",
    "ACTCL"    : "Long-Spaced Sonic Interval Transit Time",
    "ACTN"     : "????????",
    "AHV"      : "['Ahv', 'N/A']",
    "AHV1"     : "Ahv1",
    "AHVT"     : "N/A",
    "ALAT"     : "Alat",
    "ALT"      : "Alt",
    "AMAT"     : "Amat",
    "AVOL"     : "Annular Volume",
    "AZID"     : "Borehole Azimuth",
    "BHV"      : "['N/A', 'Bhv']",
    "BHV1"     : "Bhv1",
    "BHVT"     : "N/A",
    "BIT"      : "Bit Size",
    "BMIN"     : "Micro Inverse",
    "BMNO"     : "Micro Normal",
    "C13"      : "Caliper Arms 1 & 3",
    "C14"      : "C14",
    "C24"      : "Caliper Arms 2 & 4",
    "C25"      : "C25",
    "CADF"     : "Microlog Caliper",
    "CAL"      : "Caliper",
    "CAL1"     : "Cal1",
    "CAL2"     : "Cal2",
    "CAL3"     : "Cal3",
    "CAL4"     : "Cal4",
    "CAL5"     : "Cal5",
    "CAL6"     : "Cal6",
    "CAL7"     : "Cal7",
    "CAL8"     : "Cal8",
    "CAL9"     : "Cal9",
    "CALA"     : "Cala",
    "CALI"     : "Caliper",
    "CALML"    : "Curve #  20",
    "CAPD"     : "Density Caliper",
    "CGR"      : "Computed Gr From Thor., Uran., Pota.",
    "CIL1"     : "Cil1",
    "CILD"     : "Deep Conductivity",
    "CILM"     : "['Dil Medium Conductivity', 'Medium Conductivity', 'Curve #   2']",
    "CN01"     : "Cn01",
    "CN02"     : "Cn02",
    "CN03"     : "Cn03",
    "CN1"      : "Cn1",
    "CN2"      : "Cn2",
    "CNC"      : "Corrected Neutron Porosity From Cn",
    "CNC1"     : "Cnc1",
    "CNC2"     : "Cnc2",
    "CNL"      : "Cnl",
    "CNLS"     : "['Cn Limestone Porosity', 'Curve #  11']",
    "CNPOR"    : "Cn Selected Porosity",
    "COUN"     : "Cn",
    "DCAL"     : "Cdl Caliper",
    "DCOR"     : "Density Correction",
    "DEN"      : "Density",
    "DEN1"     : "Den1",
    "DEN2"     : "Den2",
    "DEN3"     : "Den3",
    "DEPT"     : "Depth Curve",
    "DEPTH"    : "Curve #   1",
    "DGA"      : "Curve #  16",
    "DLCL"     : "Caliper",
    "DLDC"     : "Density Correction",
    "DLDN"     : "Bulk Density",
    "DLDNH"    : "Bulk Density",
    "DLDP"     : "['Logged By Sc On 870216.  Digitized By Ad On 870313.', 'Logged By Sc On 930312.  Digitized By Sc On 930415.', 'Logged By Ha On 920919.  Digitized By Ha On 921009.', 'Logged By Ha On 921222.  Digitized By Ha On 940118.', 'Logged By Sc On 920213.  Digitized By Sc On 920304.', 'Logged By Ha On 920908.  Digitized By Ha On 930204.', 'Logged By Ha On 940812.  Digitized By Ha On 940912.', 'Logged By Sc On 930221.  Digitized By Sc On 930311.']",
    "DLDPH"    : "Porosity",
    "DLDPL"    : "Density Porosity (Limestone)",
    "DLGR"     : "Gamma Ray",
    "DLGRH"    : "Gamma Ray",
    "DLPE"     : "Photo-Electric Effect",
    "DLPEH"    : "Photo-Electric Effect",
    "DLTN"     : "????????",
    "DLTNH"    : "????????",
    "DPE"      : "Dpe",
    "DPE1"     : "Dpe1",
    "DPH1"     : "Dph1",
    "DPH2"     : "Dph2",
    "DPHI"     : "Dphi",
    "DPO1"     : "Dpo1",
    "DPOR"     : "Limestone Density Porosity",
    "DPTH"     : "Depth",
    "DRH1"     : "Drh1",
    "DRH2"     : "Drh2",
    "DRHO"     : "Drho",
    "DT"       : "Dt",
    "DT01"     : "Dt01",
    "DT1"      : "Dt1",
    "DT2"      : "Dt2",
    "DTCM"     : "Delta T Compensated",
    "DTDL"     : "N/A",
    "DTE1"     : "Dte1",
    "DTEM"     : "Dtem",
    "DTL"      : "Delta T, Long Spaced",
    "EATT"     : "Ept Attenuation",
    "ELN16"    : "Short Normal",
    "ELN161"   : "Short Normal",
    "EPHI"     : "Ept Porosity",
    "EPR"      : "Ept Resistivitu",
    "FCD"      : "Fcd",
    "FCD1"     : "Fcd1",
    "FCD2"     : "Fcd2",
    "FCD3"     : "Fcd3",
    "FDC"      : "Fdc",
    "GCGR"     : "Sgs Corrected Gamma Ray",
    "GR"       : "Gamma Ray",
    "GR01"     : "Gr01",
    "GR02"     : "Gr02",
    "GR03"     : "Gr03",
    "GR04"     : "Gr04",
    "GR05"     : "Gr05",
    "GR06"     : "Gr06",
    "GR07"     : "Gr07",
    "GR1"      : "Gr1",
    "GR11"     : "Gr11",
    "GR12"     : "Gr12",
    "GR2"      : "Gr2",
    "GR21"     : "Gr21",
    "GR3"      : "Gr3",
    "GR4"      : "Gr4",
    "GR5"      : "Gr5",
    "GRDI"     : "Dis Gamma Ray",
    "GRDIL"    : "Curve #  14",
    "GRML"     : "Curve #  21",
    "GRPD"     : "Pns Gamma Ray",
    "GRPO"     : "Potassium Gamma",
    "GRSG"     : "Sgs Gamma Ray",
    "GRTH"     : "Thorium Gamma",
    "GRUR"     : "Uranium Gamma",
    "GSGR"     : "Gamma Ray",
    "GSK"      : "????????",
    "GST"      : "????????",
    "GSTH"     : "Thorium",
    "GSTK"     : "????????",
    "GSUR"     : "Uranium",
    "HRD1"     : "Long Space Counts (140-200 Kev)",
    "HRD2"     : "Long Space Counts (200-540 Kev)",
    "HRD3"     : "Hrd3",
    "HRD4"     : "Hrd4",
    "HVOL"     : "Hole Volume",
    "IDCL1"    : "Density Caliper",
    "IDCL2"    : "Neutron Caliper",
    "IDCNH"    : "Fc",
    "IDFL"     : "Logged By Ha On 920908.  Digitized By Ha On 930204.",
    "IDGR"     : "Gamma Ray",
    "IDID"     : "Deep Induction",
    "IDIDC"    : "Induction (Conductivity Units)",
    "IDIDH"    : "Deep Induction",
    "IDIM"     : "Medium Induction",
    "IDIMH"    : "Medium Induction",
    "IDL3"     : "Focussed Resistivity",
    "IDLL"     : "Focussed Resistivity",
    "IDPH"     : "Induction Deep Phasor Resistivity",
    "IDSF"     : "['Logged By Sc On 930221.  Digitized By Sc On 930311.', 'Logged By Sc On 870216.  Digitized By Sc On 870714.']",
    "IDSP"     : "Spontaneous Potential",
    "IDTN"     : "????????",
    "ILD"      : "Ild",
    "ILD1"     : "Ild1",
    "ILD2"     : "Ild2",
    "ILM"      : "Ilm",
    "ILM1"     : "Ilm1",
    "ILM2"     : "Ilm2",
    "IMPH"     : "Induction Medium Phasor Resistivity",
    "IPGR"     : "Logged By Sc On 920213.  Digitized By Sc On 920304.",
    "IPID"     : "['Logged By Sc On 920213.  Digitized By Sc On 920303.', 'Logged By Sc On 870216.  Digitized By Sc On 870714.']",
    "IPIM"     : "['Logged By Sc On 920213.  Digitized By Sc On 920303.', 'Logged By Sc On 870216.  Digitized By Sc On 870714.']",
    "IPSF"     : "Logged By Sc On 920213.  Digitized By Sc On 920304.",
    "IPSP"     : "Logged By Sc On 920213.  Digitized By Sc On 920304.",
    "IPTN"     : "Logged By Sc On 920213.  Digitized By Sc On 920304.",
    "ITT"      : "['Integrated Travel Time Blips', 'Integrated Transit Time']",
    "ITTT"     : "N/A",
    "IXID"     : "Deep Induction",
    "IXID01"   : "Deep Induction",
    "IXIDC"    : "Induction (Conductivity Units)",
    "IXIDC1"   : "Induction (Conductivity Units)",
    "KTH"      : "Potassium Plus Thorium",
    "LAT"      : "Lat",
    "LAT1"     : "Lat1",
    "LL"       : "Ll",
    "LL01"     : "Ll01",
    "LL1"      : "Ll1",
    "LL8U"     : "Ll8U",
    "LLL3"     : "Focussed Resistivity",
    "LLL301"   : "Focussed Resistivity",
    "LLLDC"    : "Fc",
    "LN"       : "Ln",
    "LS"       : "Ls",
    "LS01"     : "Ls01",
    "LS1"      : "Ls1",
    "LSN"      : "Lsn",
    "LSN1"     : "Lsn1",
    "LSN2"     : "Lsn2",
    "MATF"     : "Matf",
    "MCA1"     : "Mca1",
    "MCAL"     : "Mcal",
    "MDM3"     : "Mdm3",
    "ME"       : "Micro Normal 2\"",
    "MEGR"     : "Gamma Ray",
    "MEL1"     : "Micro Inverse 1\"",
    "MI"       : "['Micro Inverse Resistivity', 'Curve #  19']",
    "MID1"     : "Mid1",
    "MIDD"     : "Midd",
    "MIN1"     : "Min1",
    "MIN2"     : "Min2",
    "MIN3"     : "Min3",
    "MIN4"     : "Min4",
    "MINM"     : "Minm",
    "MINV"     : "Micro-Inverse",
    "ML"       : "????????",
    "ML01"     : "????????",
    "ML1"      : "Ml1",
    "ML2"      : "Ml2",
    "MLA1"     : "Mla1",
    "MLAT"     : "Mlat",
    "MLL"      : "Mll",
    "MMR1"     : "Mmr1",
    "MMR2"     : "Mmr2",
    "MMR3"     : "Mmr3",
    "MMRK"     : "Mmrk",
    "MN"       : "['Micro Normal Resistivity', 'Curve #  18']",
    "MNO1"     : "Mno1",
    "MNO3"     : "Mno3",
    "MNO4"     : "Mno4",
    "MNOR"     : "['Mnor', 'Microlog, Normal']",
    "MNRL"     : "Micro-Normal 2\"",
    "MP1"      : "Mp1",
    "MP2"      : "Mp2",
    "MP3"      : "Mp3",
    "MP4"      : "Mp4",
    "MP5"      : "Mp5",
    "MP6"      : "Mp6",
    "MR1F"     : "Micro-Inverse 1\"",
    "MR2F"     : "Micro-Normal 2\"",
    "MRS1"     : "Micro-Inverse 1\" Raw",
    "MRS2"     : "Micro-Normal 2\" Raw",
    "MSFL"     : "Msfl Resistivity",
    "NCNP"     : "['Logged By Sc On 930221.  Digitized By Sc On 930311.', 'Logged By Sc On 930312.  Digitized By Sc On 930415.', 'Logged By Ha On 920919.  Digitized By Ha On 921009.', 'Logged By Ha On 921222.  Digitized By Ha On 940118.', 'Logged By Sc On 920213.  Digitized By Sc On 920304.', 'Logged By Ha On 920908.  Digitized By Ha On 930204.', 'Logged By Ha On 940812.  Digitized By Ha On 940912.', 'Logged By Sc On 870216.  Digitized By Sc On 870714.']",
    "NCNPH"    : "Porosity",
    "NCNPL"    : "Neutron Porosity (Limestone)",
    "NEUT"     : "Neut",
    "NLI1"     : "Nli1",
    "NLIM"     : "Nlim",
    "NPE1"     : "Npe1",
    "NPES"     : "Npes",
    "NPH1"     : "Nph1",
    "NPH2"     : "Nph2",
    "NPHI"     : "Nphi",
    "NPOR"     : "Limest. Neutron Porosity",
    "NPRL"     : "Limest. Neutron Porosity",
    "NRAT"     : "Neutron Ratio (Nd/Fd)",
    "NSD1"     : "Nsd1",
    "NSDL"     : "Nsdl",
    "PE"       : "Photo Electric Cross Section",
    "PE1"      : "Pe1",
    "PE2"      : "Pe2",
    "PEDN"     : "Near Pe Curve",
    "PEF"      : "Photoelectric Factor",
    "PEF1"     : "Pef1",
    "PEF2"     : "Pef2",
    "PH12"     : "Ph12",
    "PH13"     : "Ph13",
    "PH14"     : "Ph14",
    "PH15"     : "Ph15",
    "PH23"     : "Ph23",
    "PH24"     : "Ph24",
    "PHN1"     : "Phn1",
    "PHND"     : "Phnd",
    "PHT1"     : "Pht1",
    "PHTL"     : "Phtl",
    "POR"      : "Por",
    "POR1"     : "Por1",
    "POR2"     : "Por2",
    "POR3"     : "Por3",
    "POR4"     : "Por4",
    "PORA"     : "['Pora', 'Porosity From Acoustilog']",
    "PORZ"     : "Porosity From Z-Densilog",
    "POT2"     : "Pot2",
    "PSD3"     : "Psd3",
    "PSU3"     : "Psu3",
    "QDT"      : "Qdt",
    "QDT1"     : "Qdt1",
    "QDTS"     : "Qdts",
    "QL"       : "Ql",
    "QL1"      : "Ql1",
    "QPE"      : "Qpe",
    "QPE1"     : "Qpe1",
    "QS"       : "Qs",
    "QS1"      : "Qs1",
    "R1"       : "R1.5",
    "R2"       : "R2",
    "RFA"      : "Rfa",
    "RFA1"     : "Rfa1",
    "RFO1"     : "Rfo1",
    "RFOC"     : "Resistivity From Cfoc",
    "RGC1"     : "Rgc1",
    "RGCN"     : "Rgcn",
    "RHG1"     : "Rhg1",
    "RHGA"     : "Rhga",
    "RHO1"     : "Rho1",
    "RHO2"     : "Rho2",
    "RHOB"     : "Bulk Density",
    "RHOC"     : "['Curve #   9', 'Cdl Density Correction']",
    "RIL1"     : "Ril1",
    "RIL2"     : "Ril2",
    "RIL3"     : "Ril3",
    "RIL4"     : "Ril4",
    "RILD"     : "Resistivity From Cild",
    "RILM"     : "Resistivity From Cilm",
    "RLL3"     : "['Dil Shallow Resistivity', 'Curve #   3']",
    "RLL3F"    : "Dil Shallow Resistivity Filtered",
    "RLM1"     : "Rlm1",
    "RLM2"     : "Rlm2",
    "RLM3"     : "Rlm3",
    "RLML"     : "Resistivity Of 1\" Lateral",
    "RMF1"     : "Rmf1",
    "RMFA"     : "Rmfa",
    "RNM1"     : "Rnm1",
    "RNM2"     : "Rnm2",
    "RNM3"     : "Rnm3",
    "RNML"     : "Resistivity Of 2\" Normal",
    "RO"       : "Ro",
    "RSFE"     : "Shallow Fe",
    "RSFR"     : "Shallow Fe Raw",
    "RT"       : "Rt",
    "RT1"      : "Rt1",
    "RT2"      : "Rt2",
    "RT3"      : "Rt3",
    "RWA"      : "Rwa",
    "RWA1"     : "Rwa1",
    "RXCL"     : "Caliper",
    "RXGR"     : "Gamma Ray",
    "RXGR01"   : "Gamma Ray",
    "RXORT"    : "['Rxo / Rt', 'Curve #  13']",
    "RXRT"     : "N/A",
    "RXSP"     : "Spontaneous Potential",
    "RXSP01"   : "Spontaneous Potential",
    "RXT1"     : "Rxt1",
    "RXTD"     : "Rxtd",
    "SCAE"     : "Scae",
    "SCF1"     : "Scf1",
    "SCF3"     : "Scf3",
    "SCSP"     : "Spontaneous Potential",
    "SDCS"     : "Sdcs",
    "SDS1"     : "Sds1",
    "SDSO"     : "Sdso",
    "SDSS"     : "Sdss",
    "SDT2"     : "N/A",
    "SFL"      : "Sflaterolog",
    "SFL1"     : "Sfl1",
    "SFL2"     : "Sfl2",
    "SFL3"     : "Sfl3",
    "SFL4"     : "Sfl4",
    "SFLA"     : "Sfla",
    "SFLU"     : "Sfl Resistivity (Unaveraged)",
    "SFT2"     : "Long Space Counts (100-140 Kev)",
    "SFT3"     : "Sft3",
    "SGR"      : "Spectroscopy Gamma-Ray",
    "SGR1"     : "Sgr1",
    "SGR2"     : "Sgr2",
    "SGRD"     : "Sgrd",
    "SGRU"     : "Sgru",
    "SHR"      : "Sft2/Hrd2 Ratio",
    "SHR1"     : "Shr1",
    "SN"       : "Sn",
    "SN01"     : "Sn01",
    "SON"      : "Sonic",
    "SP"       : "Spontaneous Potential From Tool Electrode",
    "SP02"     : "Sp02",
    "SP1"      : "Sp1",
    "SP2"      : "Sp2",
    "SPC"      : "Curve #  14",
    "SPD"      : "Speed",
    "SPD1"     : "Spd1",
    "SPD2"     : "Spd2",
    "SPD3"     : "Spd3",
    "SPD4"     : "Spd4",
    "SPH1"     : "Sph1",
    "SPH2"     : "Sph2",
    "SPHI"     : "Sphi",
    "SPOR"     : "Sonic Porosity",
    "SPR"      : "Dis Sp Raw",
    "SSD"      : "Short Spaced Counts",
    "SSD1"     : "Ssd1",
    "SSN"      : "Ssn",
    "SSN1"     : "Ssn1",
    "STI1"     : "Sti1",
    "STI2"     : "Sti2",
    "STI3"     : "Sti3",
    "STI4"     : "Sti4",
    "STI5"     : "Sti5",
    "STI6"     : "Sti6",
    "STIA"     : "Stia",
    "STIT"     : "Stit",
    "SVE1"     : "Sve1",
    "SVEL"     : "Svel",
    "TDIC"     : "Tdic",
    "TDIS"     : "Tdis",
    "TEN"      : "Differential Tension",
    "TENDIL"   : "Curve #  19",
    "TENML"    : "Curve #  24",
    "TENS"     : "Line Tension",
    "TENZDEN"  : "Curve #  10",
    "TEXD"     : "Dis Borehole Temperature",
    "THO1"     : "Tho1",
    "THO2"     : "Tho2",
    "TILD"     : "Borehole Tilt",
    "TNPH"     : "Thermal Neutron Porosity",
    "TPDS"     : "Tension Of Cable",
    "TPL3"     : "Tpl3",
    "TPL4"     : "Tpl4",
    "TSS1"     : "Tension Of Cable",
    "V1M3"     : "V1M3",
    "V1M4"     : "V1M4",
    "V2M3"     : "V2M3",
    "V2M4"     : "V2M4",
    "V3M3"     : "V3M3",
    "V3M4"     : "V3M4",
    "VCVS"     : "Vcvs",
    "VIL1"     : "Vil1",
    "VIL2"     : "Vil2",
    "VILD"     : "Raw Output Of Deep Induction",
    "VILM"     : "Raw Output Of Medium Induction",
    "ZCO1"     : "Zco1",
    "ZCO2"     : "Zco2",
    "ZCOR"     : "Z-Densilog Bulk Density Correction",
    "ZDE1"     : "Zde1",
    "ZDE2"     : "Zde2",
    "ZDEN"     : "Z-Densilog Bulk Density",
}

#: A mapping of LgFormat mnemonics to typical LAS mnemonics
LGFORMAT_OUTP_UNIQUEID = {
    "A22H"       : ['A22H_ARC'],
    "A34H"       : ['A34H_ARC'],
    "AAI"        : ['AAI'],
    "AHF10"      : ['AHF10_6'],
    "AHF20"      : ['AHF20_5'],
    "AHF30"      : ['AHF30_7'],
    "AHF60"      : ['AHF60_8'],
    "AHF90"      : ['AHF90_9'],
    "AHO10"      : ['AHO10_6'],
    "AHO20"      : ['AHO20_5'],
    "AHO30"      : ['AHO30_7'],
    "AHO60"      : ['AHO60_8'],
    "AHO90"      : ['AHO90_9'],
    "AHT10"      : ['AHT10_6', 'AIT-H_10_InchInvestigation'],
    "AHT20"      : ['AIT-H_20_InchInvestigation', 'AHT20_5'],
    "AHT30"      : ['AIT-H_30_InchInvestigation', 'AHT30_7'],
    "AHT60"      : ['AHT60_8', 'AIT-H_60_InchInvestigation'],
    "AHT90"      : ['AIT-H_90_InchInvestigation', 'AHT90_9'],
    "APDC"       : ['APS_CorrectedDolomitePorosity'],
    "APLC"       : ['APS_CorrectedLimestinePorosity'],
    "APSC"       : ['APS_CorrectedSandstonePorosity'],
    "ATR"        : ['ATR'],
    "B1TR"       : ['MRPS1_Temp'],
    "BFR1"       : ['MRPS1_Resis'],
    "BMIN"       : ['MicroInverseB'],
    "BMNO"       : ['MicroNormalB'],
    "BQP1"       : ['BQP1', 'BQP1_tens'],
    "BS"         : ['BitSize', 'BS_7', 'BS'],
    "BSG1"       : ['BSG1'],
    "BTAB"       : ['BTAB'],
    "C1"         : ['C1', 'C1Caliper'],
    "C1_OBMT"    : ['C1_OBMT-11'],
    "C2"         : ['C2', 'C2Caliper'],
    "C2_OBMT"    : ['C2_OBMT-12'],
    "CALI"       : ['Cali', 'Caliper', 'CALI_8', 'CALI'],
    "CALI_CDN"   : ['CALI_CDN'],
    "CATR"       : ['CATR'],
    "CGR"        : ['CGR_2'],
    "CILD"       : ['CILD'],
    "CLLD"       : ['CLLD'],
    "CMFF"       : ['CMR_FreeFluidPorosity'],
    "CMRP"       : ['CMR_POROSITY'],
    "DCAL"       : ['DCAL'],
    "DEVI"       : ['DEVI'],
    "DPHB"       : ['DPHB'],
    "DPHI"       : ['DensityPorosity'],
    "DPHZ"       : ['StdResDensityPorosity'],
    "DPOR_CDN"   : ['DPOR_CDN'],
    "DRHB"       : ['DRHB'],
    "DRHL"       : ['DRHL'],
    "DRHO"       : ['DRHO'],
    "DRHR"       : ['DRHR'],
    "DRHU"       : ['DRHU'],
    "DSOZ"       : ['DensityStandoff'],
    "DT"         : ['DT'],
    "DT0S"       : ['Delta-T_Shear2'],
    "DT1"        : ['Delta-T_Shear_LDipole', 'Delta-T_Shear1'],
    "DT1R"       : ['Delta-T_Shear4'],
    "DT2"        : ['Delta-T_Shear6', 'Delta-T_Shear2', 'Delta-T_Shear_UDipole'],
    "DT2R"       : ['MonopoleStoneley2'],
    "DT3R"       : ['Delta-T_Stonley'],
    "DT4S"       : ['Delta-T_Shear5'],
    "DTAB"       : ['DTAB'],
    "DTBC"       : ['DTBoreholeComp'],
    "DTCO"       : ['Delta-T_Comp', 'DTCompressionalSDT'],
    "DTCU"       : ['DTComputedUphole'],
    "DTL"        : ['DTL_DDBHC'],
    "DTLF"       : ['DTLF_DDBHC'],
    "DTLN"       : ['DTLN_DDBHC'],
    "DTR2"       : ['SlownessUpperDipoleMode'],
    "DTR5"       : ['SlownessFirstMotionMode'],
    "DTRA"       : ['DTReceiverArray'],
    "DTRP"       : ['Delta-T_PS_Comp'],
    "DTRS"       : ['Delta-T_Shear3', 'Delta-T_PS_Shear'],
    "DTSH"       : ['Delta-T_Shear7'],
    "DTSM"       : ['Delta-T_ShearMonoPole', 'Delta-T_Shear'],
    "DTST"       : ['MonopoleStoneley', 'Delta-T_Stonely'],
    "DTTA"       : ['DTTransArray'],
    "ENPH"       : ['EpithermalPorosity'],
    "GR"         : ['GR_2', 'GammaRay', 'GR_9'],
    "GRDN_RAB"   : ['GRDN_RAB'],
    "GRLT_RAB"   : ['GRLT_RAB'],
    "GRRT_RAB"   : ['GRRT_RAB'],
    "GRUP_RAB"   : ['GRUP_RAB'],
    "GR_RAB"     : ['GammaRay', 'GammaRayRAB'],
    "GR_SL"      : ['GR_2'],
    "HAZI"       : ['HAZI'],
    "HAZIM"      : ['HoleAzimuth'],
    "HCAL"       : ['HILTCaliper', 'HiltCaliper'],
    "HDIA"       : ['HDIA'],
    "HMIN"       : ['ComputedMicroInverse'],
    "HMNO"       : ['ComputedMicroNormal'],
    "ILD"        : ['ILD'],
    "ILM"        : ['ILM'],
    "INFD"       : ['INFD_17'],
    "INFD_SL"    : ['INFD_17'],
    "LLD"        : ['LLD'],
    "LLM"        : ['LLM'],
    "MINV"       : ['MicroInverse'],
    "MLL"        : ['MicroLaterolog'],
    "MNOR"       : ['MicroNormal'],
    "MSFL"       : ['MicroSFL', 'MSFL'],
    "NPHI"       : ['OLDESTNeutronPorosity'],
    "NPOR"       : ['OLDNeutronPorosity'],
    "OBRA3"      : ['OBRA3-14'],
    "OBRB3"      : ['OBRB3-15'],
    "OBRC3"      : ['OBRC3-16'],
    "OBRD3"      : ['OBRD3-17'],
    "P16H_RT"    : ['P16H_ARC'],
    "P1AZ"       : ['Pad1Azimuth'],
    "P1NO_OBMT"  : ['P1NO_OBMT-13'],
    "P28H_RT"    : ['P28H_ARC'],
    "P34H_RT"    : ['P34H_ARC'],
    "PCAL"       : ['PCAL'],
    "PEB"        : ['PEB'],
    "PEF"        : ['PEF'],
    "PEFZ"       : ['StdResFormationPe'],
    "PEL"        : ['PEL'],
    "PER"        : ['PER'],
    "PEU"        : ['PEU'],
    "POHP"       : ['POHP'],
    "POTA"       : ['POTA'],
    "PROX"       : ['Provimity'],
    "PSR"        : ['PSR'],
    "RDBD"       : ['RDBD'],
    "RDBL"       : ['RDBL'],
    "RDBR"       : ['RDBR'],
    "RDBU"       : ['RDBU'],
    "RES_BD"     : ['RES_BD'],
    "RES_BM"     : ['RES_BM'],
    "RES_BS"     : ['RES_BS'],
    "RES_RING"   : ['RES_RING'],
    "RHOB"       : ['RHOB'],
    "RHOZ"       : ['RHOZ'],
    "RLA0"       : ['RLA0_ALAT', 'RLA0'],
    "RLA1"       : ['RLA1', 'RLA1_ALAT'],
    "RLA2"       : ['RLA2', 'RLA2_ALAT'],
    "RLA3"       : ['RLA3', 'RLA3_ALAT'],
    "RLA4"       : ['RLA4_ALAT', 'RLA4'],
    "RLA5"       : ['RLA5', 'RLA5_ALAT'],
    "RMBD"       : ['RMBD'],
    "RMBL"       : ['RMBL'],
    "RMBR"       : ['RMBR'],
    "RMBU"       : ['RMBU'],
    "ROBB"       : ['ROBB'],
    "ROBL"       : ['ROBL'],
    "ROBR"       : ['ROBR'],
    "ROBU"       : ['ROBU'],
    "ROP5"       : ['ROP5'],
    "RPM"        : ['RPM'],
    "RSBD"       : ['RSBD'],
    "RSBL"       : ['RSBL'],
    "RSBR"       : ['RSBR'],
    "RSBU"       : ['RSBU'],
    "RSOZ"       : ['ResistivityStandoff'],
    "RTAB"       : ['RTAB'],
    "RXO"        : ['RXO', 'ResistivityFlushedZone'],
    "RXOZ"       : ['StdResInvadedZoneResistivity'],
    "SCN2"       : ['SCN2'],
    "SFL"        : ['SFL'],
    "SGR"        : ['SGR_1'],
    "SIGM"       : ['SIGM_14'],
    "SIGM_SL"    : ['SIGM_14'],
    "SNP"        : ['SIDEWALLNEUTRONPorosity'],
    "SOAB"       : ['SOAB'],
    "SOAL"       : ['SOAL'],
    "SOAR"       : ['SOAR'],
    "SOAU"       : ['SOAU'],
    "SONB"       : ['SONB'],
    "SOXB"       : ['SOXB'],
    "SP"         : ['SP_10', 'SP'],
    "SPHI"       : ['SonicPorosity'],
    "TAU"        : ['TAU'],
    "TAU_SL"     : ['TAU'],
    "TCAF"       : ['TCAF_13'],
    "TCAF_SL"    : ['TCAF_13'],
    "TENS"       : ['Tension', 'TENSION', 'TENS_16', 'TENS_6'],
    "TENS_SL"    : ['TENS_16'],
    "THOR"       : ['THOR'],
    "TNPB"       : ['TNPB'],
    "TNPH"       : ['NeutronPorosity', 'TNPH'],
    "TNPH_CDN"   : ['TNPH_CDN'],
    "TPHI"       : ['TPHI_15'],
    "TPHI_SL"    : ['TPHI_15'],
    "TSCF"       : ['TSCF_12'],
    "TSCF_SL"    : ['TSCF_12'],
    "TSCN"       : ['TSCN_13'],
    "TSCN_SL"    : ['TSCN_13'],
    "URAN"       : ['URAN'],
    "VDIA"       : ['VDIA'],
}

#: This is a map of LgFormat <ChannelName/> to correspondingly appropriate LAS menmonics
#: It's a best guess...
LGFORMAT_LAS = {
    'BS'        : ['BIT',],
    'C1'        : ['C13', 'CAL1',],
    'C2'        : ['C24', 'CAL2',],
    'CALI'      : ['CAL', 'DLCL',],
    'CGR'       : ['ACGR', 'GCGR',],
    'DEVI'      : ['TILT',],
    'DRHO'      : ['DLDC',],
    'GR'        : ['DLGR', 'DLGRH', 'GRDI', 'GRPD', 'GRSG', 'GSGR', 'IDGR', 'MEGR', 'RXGR', 'RXGR01',],
    'HAZI'      : ['AZID',],
    'POTA'      : ['GRPO',],
    'SFL'       : ['SFLU',],
    'THOR'      : ['GSTH', 'GRTH',],
    'URAN'      : ['GSUR', 'GRUR',],
}

#: Reverse map to LAS mnemonics to LgFormat <ChannelName/> values.
LAS_LGFORMAT = {}
for __k in LGFORMAT_LAS:
    for __v in LGFORMAT_LAS[__k]:
        assert(__v not in LAS_LGFORMAT)
        LAS_LGFORMAT[__v] = __k

#import functools
#c = set(CURVE_DESCRIPTION.keys())
#l = set(LGFORMAT_OUTP_UNIQUEID.keys())
#print(' Num curves:', len(c))
#print('Num formats:', len(l))
#print('   Num both:', len(c & l))
#print('Formats in LAS:', sorted(c & l))
#print('Formats not in LAS:', len(l - c))
#print(sorted(l - c))
#print('Formats not in LAS (interpreted):', len(l - c - set(LGFORMAT_LAS.keys())))
#print(sorted(l - c - set(LGFORMAT_LAS.keys())))
##print('Formats in LAS (interpreted):', len(sorted((c & l) | set(LGFORMAT_LAS.keys()))))
##print(sorted((c & l) | l))
#__l = set(functools.reduce(lambda x,y,: x+y, LGFORMAT_LAS.values(), []))
#print('Formats in LAS (interpreted):', len(((c & l) | __l)))
#print(sorted((c & l) | __l))
