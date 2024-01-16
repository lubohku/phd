import pya
import setup
from setup import Rec
layout = setup.layout

#================================================================================#
#=========================  LAYER AND SIZE PARAMETERS   =========================#
#================================================================================#

l10 = setup.l10 # Isolation
l20 = setup.l20 # Large pillar
l30 = setup.l30 # Small pillar
l40 = setup.l40 # Shallow etch
l50 = setup.l50 # CSL
l60 = setup.l60 # n-Open
l70 = setup.l70 # Metal
l1000 = setup.l1000

factor = setup.factor
df = setup.df
outfile = setup.testkey_out

#================================================================================#
#================================================================================#
#=======================>>>>>>>>>>  TEST KEY  <<<<<<<<<<=========================#
#================================================================================#
#================================================================================#

#================================================================================#
#==================================  OVERLAY  ===================================#
#================================================================================#
def i_overlay(ly):
    ovl_box = pya.Region()
    ovl_box.insert(pya.Box(0, 0, 100, 100)*factor)
    ovl_center = pya.Region()
    ovl_center.insert(pya.Box(30, 30, 70, 70)*factor)
    ovl_align = pya.Region()
    ovl_align.insert(pya.Box(40, 40, 60, 60)*factor)
    i_ovl = ovl_box-ovl_center+ovl_align
    if str(layout.get_info(ly)) != '0/0':
        return ovl_align
    return i_ovl

def o_overlay():
    ovl1 = pya.Region()
    ovl1.insert(pya.Box(25, 10, 75, 20)*factor)
    ovl2 = pya.Region()
    ovl2.insert(pya.Box(25, 80, 75, 90)*factor)
    ovl3 = pya.Region()
    ovl3.insert(pya.Box(10, 25, 20, 75)*factor)
    ovl4 = pya.Region()
    ovl4.insert(pya.Box(80, 25, 90, 75)*factor)
    o_ovl = ovl1+ovl2+ovl3+ovl4
    return o_ovl

def overlay(i_ly, o_ly):
    i_ly_data = str(layout.get_info(i_ly))
    i_ly_idx = df[df['Layer'] == i_ly_data].index.values.astype(int)[0]
    i_ly_name = df['Name'][i_ly_idx]

    o_ly_data = str(layout.get_info(o_ly))
    o_ly_idx = df[df['Layer'] == o_ly_data].index.values.astype(int)[0]
    o_ly_name = df['Name'][o_ly_idx]

    ovl_single = layout.create_cell('OVL_'+i_ly_name+'_'+o_ly_name)
    i_text = pya.TextGenerator.default_generator().text(i_ly_data.replace("/",""), 0.00003)
    ovl_single.shapes(i_ly).insert(i_overlay(i_ly), pya.Trans(32*factor, 0))
    ovl_single.shapes(i_ly).insert(i_text, pya.Trans(1, False, 27*factor, 7*factor))

    o_text = pya.TextGenerator.default_generator().text(o_ly_data.replace("/",""), 0.00003)
    ovl_single.shapes(o_ly).insert(o_overlay(), pya.Trans(32*factor, 0))
    ovl_single.shapes(o_ly).insert(o_text, pya.Trans(1, False, 27*factor, 56*factor))
    return ovl_single

def ovl_array():

    ovl1 = overlay(l20, l30)
    ovl1.shapes(l40).insert(pya.Box(0, 0, 132, 100)*factor)
    ovl1.shapes(l10).insert(pya.Box(0, 0, 132, 100)*factor)
    
    ovl2 = overlay(l20, l40)
    ovl2.shapes(l40).insert(pya.Box(0, 0, 32, 50)*factor)
    ovl2.shapes(l40).insert(pya.Box(72-5, 40-5, 92+5, 60+5)*factor)
    ovl2.shapes(l10).insert(pya.Box(0, 0, 132, 100)*factor)

    ovl3 = overlay(l40, l10)
    ovl3.shapes(l10).insert(pya.Box(0, 0, 32, 50)*factor)
    ovl3.shapes(l10).insert(pya.Box(72-5, 40-5, 92+5, 60+5)*factor)
    ovl3.shapes(l10).insert(pya.Box(72-5, 40-5, 92+5, 60+5)*factor)

    ovl4 = overlay(l10, l50)
    ovl4.shapes(l10).insert(pya.Box(0, 50, 32, 100)*factor)

    ovl5 = overlay(l10, l60)
    ovl5.shapes(l10).insert(pya.Box(0, 50, 32, 100)*factor)

    ovl6 = overlay(l50, l60)
    # ovl6.shapes(l10).insert(pya.Box(0, 0, 132, 100)*factor)

    ovl7 = overlay(l10, l70)
    ovl7.shapes(l10).insert(pya.Box(0, 50, 32, 100)*factor)

    ovl8 = overlay(l50, l70)
    # ovl8.shapes(l10).insert(pya.Box(0, 0, 132, 100)*factor)
    
    ovl_all = layout.create_cell('OVL')
    for k, ovl_mark in enumerate([ovl1, ovl2, ovl3, ovl4, ovl5, ovl6, ovl7, ovl8]):
        ovl_all.insert(pya.CellInstArray(ovl_mark.cell_index(),pya.Trans(k*132*factor, 0)))
    return ovl_all



#================================================================================#
#==================================  THKPAD  ====================================#
#================================================================================#

def thk_single(ly):
    ly_data = str(layout.get_info(ly))
    ly_idx = df[df['Layer'] == ly_data].index.values.astype(int)[0]
    ly_name = df['Name'][ly_idx]

    thk = layout.create_cell('THKPAD_'+ly_name)
    thkbox = pya.Region()
    thkbox.insert(pya.Box(0, 0, 120, 100)*factor)
    thkpad = pya.Region()
    thkpad.insert(pya.Box(40, 20, 100, 80)*factor)

    text = pya.TextGenerator.default_generator().text(str(ly_data).replace('/',''), 0.00003)
    thk.shapes(ly).insert(text, pya.Trans(1, False, 30*factor, 35*factor))

    thk.shapes(l10).insert(thkbox)
    thk.shapes(ly).insert(thkpad)

    return thk

def thk_array():

    thk_mark = layout.create_cell('THK')
    thk_mark.insert(pya.CellInstArray(thk_single(l40).cell_index(),pya.Trans(0, 0)))
    return thk_mark

#================================================================================#
#==================================  TML  ====================================#
#================================================================================#
def tml():
    l = 490*factor
    h = 100*factor
    n = 6
    tml = layout.create_cell('TML')
    tml.shapes(l10).insert(Rec(l/2, h/2, l, h))
    # tml.shapes(l60).insert(pya.Box(5*factor, 5*factor, 55*factor, 165*factor))
    # tml.shapes(l70).insert(pya.Box(5*factor, 5*factor, 55*factor, 165*factor))
    tml.shapes(l40).insert(Rec(l/2, h/2, l-20*factor, h-30*factor))
    for k in range(n):
        tml.shapes(l50).insert(Rec((50-5)*factor+(50*k+10*k*(1+k)/2)*factor, 50*factor, 50*factor, 50*factor))
        tml.shapes(l70).insert(Rec((50-5)*factor+(50*k+10*k*(1+k)/2)*factor, 50*factor, 50*factor, 50*factor))

    return tml

if __name__ == '__main__':
    # print(outfile)
    testkey = layout.create_cell('TestKey')
    testkey.insert(pya.CellInstArray(ovl_array().cell_index(), pya.Trans(120*factor, 0)))
    # testkey.insert(pya.CellInstArray(cdbar_array().cell_index(), pya.Trans(-4*factor, 0)))
    testkey.insert(pya.CellInstArray(thk_array().cell_index(), pya.Trans(0, 0)))
    testkey.insert(pya.CellInstArray(tml().cell_index(), pya.Trans(1200*factor, 0)))

    layout.write(outfile)