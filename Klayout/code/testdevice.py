import pya
import setup
from setup import Rec, auto_router, sha_shape
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
outfile = setup.testdevice_out

pixel_x = setup.pixel_x
pixel_y = setup.pixel_y
margin_pixel = setup.margin_pixel
pitch_x = setup.pitch_x
pitch_y = setup.pitch_y

#================================================================================#
#=================================  TestDevice  =================================#
#================================================================================#


def td_unit_nometal(l,h):
    td_unit = layout.create_cell('No_Metal')
    
    for k in range(3):
        td_unit.shapes(l40).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l50).insert(pya.Box(5*factor, 5*factor, l-5*factor, h-5*factor).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l70).insert(pya.Box(0, 0, 20*factor, 10*factor).transformed(pya.Trans(k*pitch_x+margin_pixel+l/2-10*factor, margin_pixel)))

    td_unit.shapes(l20).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(pitch_x+margin_pixel, margin_pixel)))
    td_unit.shapes(l30).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(2*pitch_x+margin_pixel, margin_pixel)))

    td_unit.shapes(l10).insert(pya.Box(0, 0, 3*l+4*margin_pixel, 100*factor))
    td_unit.shapes(l60).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    td_unit.shapes(l70).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    
    return td_unit

def td_unit_metal(l,h):
    td_unit = layout.create_cell('Full_Metal')
    
    for k in range(3):
        td_unit.shapes(l40).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l50).insert(pya.Box(5*factor, 5*factor, l-5*factor, h-5*factor).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l70).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))

    td_unit.shapes(l20).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(pitch_x+margin_pixel, margin_pixel)))
    td_unit.shapes(l30).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(2*pitch_x+margin_pixel, margin_pixel)))

    td_unit.shapes(l10).insert(pya.Box(0, 0, 3*l+4*margin_pixel, 100*factor))
    td_unit.shapes(l60).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    td_unit.shapes(l70).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    
    return td_unit

def td_unit_shametal(l,h,lw):
    td_unit = layout.create_cell('ShaShape_'+str(int(lw/factor))+'um')
    
    for k in range(3):
        td_unit.shapes(l40).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l50).insert(pya.Box(5*factor, 5*factor, l-5*factor, h-5*factor).transformed(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))
        td_unit.shapes(l70).insert(sha_shape(l, h, lw=lw).transform(pya.Trans(k*pitch_x+margin_pixel, margin_pixel)))

    td_unit.shapes(l20).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(pitch_x+margin_pixel, margin_pixel)))
    td_unit.shapes(l30).insert(pya.Box(0, 0, l, h).transformed(pya.Trans(2*pitch_x+margin_pixel, margin_pixel)))

    td_unit.shapes(l10).insert(pya.Box(0, 0, 3*l+4*margin_pixel, 100*factor))
    td_unit.shapes(l60).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    td_unit.shapes(l70).insert(pya.Box(0, 70*factor, 3*l+4*margin_pixel, 90*factor))
    
    return td_unit

def td_npad(s='left'):
    td_npad = layout.create_cell('nPad_'+s)
    
    td_npad.shapes(l10).insert(pya.Box(0, 0, 100*factor, 100*factor))
    td_npad.shapes(l60).insert(pya.Box(10*factor, 10*factor, 100*factor, 90*factor))
    td_npad.shapes(l70).insert(pya.Box(10*factor, 10*factor, 100*factor, 90*factor))
    
    return td_npad

def td_ppad():
    lw = 20*factor
    td_ppad = layout.create_cell('pPad_router')
    td_ppad.shapes(l70).insert(auto_router(n=3*5, up_l=60*3*5*factor, h=300*factor, linewidth=lw, linegap=pitch_x - lw,boxwidth=80*factor, box_hgap=20*factor, box_tip=20*factor))
    
    return td_ppad

if __name__ == '__main__':
    # print(outfile)
    testdevice = layout.create_cell('TestDevice')
    testdevice.insert(pya.CellInstArray(td_npad().cell_index(), pya.Trans(0, 0)))

    testdevice.insert(pya.CellInstArray(td_unit_nometal(pixel_x,pixel_y).cell_index(), pya.Trans(100*factor, 0)))
    testdevice.insert(pya.CellInstArray(td_unit_metal(pixel_x,pixel_y).cell_index(), pya.Trans(3*pitch_x+100*factor, 0)))
    testdevice.insert(pya.CellInstArray(td_unit_shametal(pixel_x,pixel_y,lw=2*factor).cell_index(), pya.Trans(6*pitch_x+100*factor, 0)))
    testdevice.insert(pya.CellInstArray(td_unit_shametal(pixel_x,pixel_y,lw=5*factor).cell_index(), pya.Trans(9*pitch_x+100*factor, 0)))
    testdevice.insert(pya.CellInstArray(td_unit_shametal(pixel_x,pixel_y,lw=10*factor).cell_index(), pya.Trans(12*pitch_x+100*factor, 0)))

    testdevice.insert(pya.CellInstArray(td_npad(s='right').cell_index(), pya.Trans.M90*pya.Trans(-(15*pitch_x+margin_pixel+200*factor), 0)))

    testdevice.insert(pya.CellInstArray(td_ppad().cell_index(), pya.Trans.M0*pya.Trans(100*factor+pixel_x/2, -10*factor)))

    layout.write(outfile)