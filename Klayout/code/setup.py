import pya
import math
import pandas as pd
import numpy as np
import os

layout = pya.Layout()
#================================================================================#
#=========================  LAYER AND SIZE PARAMETERS   =========================#
#================================================================================#

l10 = layout.layer(1, 0) # Isolation
l20 = layout.layer(2, 0) # Large pillar
l30 = layout.layer(3, 0) # Small pillar
l40 = layout.layer(4, 0) # Shallow etch
l50 = layout.layer(5, 0) # CSL
l60 = layout.layer(6, 0) # n-Open
l70 = layout.layer(7, 0) # Metal
l80 = layout.layer(8, 0) # Metal-Sha
l1000 = layout.layer(100, 0) # Dicing
l1001 = layout.layer(1001, 0)
l1002 = layout.layer(1002, 0)
l1003 = layout.layer(1003, 0)

#================================================================================#
#==========================  parameters for the mask  ===========================#
#================================================================================#
factor = 1000

mask_size = 105*10**3*factor
margin_mask = 10*10**4*factor
wafer_size = 2.54*2*10**4*factor

pixel_x = 50*factor
pixel_y = 50*factor
margin_pixel = 10*factor
pitch_x = pixel_x + margin_pixel
pitch_y = pixel_y + margin_pixel

die_size_x = 5*10**3*factor
die_size_y = 5*10**3*factor
die_margin_x = 2200*factor
die_margin_y = die_margin_x
die_col = 4
die_row = 3
die_pitch_x = die_size_x
die_pitch_y = die_size_y
# die_col = int((mask_size-margin_mask)/die_pitch_x)
# die_row = int((mask_size-margin_mask)/die_pitch_y)

die_shift_x = (mask_size-die_pitch_x*die_col)/2
die_shift_y = (mask_size-die_pitch_y*die_row)/2

die_no_font = 8/die_margin_x
die_no_font_head = 0.8/die_margin_x

test_gap = 20*factor
# test_edge = die_margin_y/2 - 500*factor
test_edge = 50*factor
lys = [l10,l20,l30,l40,l50,l60,l70]
klayout_path = 'C:/Software/Klayout/klayout_app.exe'
df = pd.read_excel("mask_lyp.xlsx")

dicing = 0*factor

currentPath = os.getcwdb().decode("utf-8") 
# print(currentPath)
lichk_gen = currentPath + "/lithocheck.py"
align_gen = currentPath + "/alignmark.py"
body_gen = currentPath + "/maskbody.py"
testkey_gen = currentPath + "/testkey.py"
testdevice_gen = currentPath + "/testdevice.py"
extract_layer = currentPath + "/extractlayer.py"

print(currentPath)

outdir = currentPath + "/MaskCells/"

body_out = outdir + "/01_maskbody.gds"
lichk_out = outdir + "/02_lithocheck.gds"
align_out = outdir + "/03_alignmark.gds"
testkey_out = outdir + "/04_testkey.gds"
testdevice_out = outdir + "/05_testdevice.gds"

final_out = currentPath + "/MASK_FINAL.gds"
skip_exe = False
version = 'AC052'

#================================================================================#
#==============================  Basic Functions  ===============================#
#================================================================================#
# Return Region Rectangle
# input center coordinate and size of rectangle
def Rec(x, y, l, h):
    rec = pya.Region()
    rec.insert(pya.Box(x-l/2, y-h/2, x+l/2, y+h/2))
    return rec

# Return Region Circle
# input center coordinate and radius of circle
def Circle(x, y, r):
    cir = pya.Region()
    nr_points = 360
    angles = np.linspace(0,2*np.pi,nr_points+1)[0:-1]
    points = []
    for angle in angles:
        points.append(pya.Point(r*np.cos(angle),r*np.sin(angle)))
    cir.insert(pya.SimplePolygon(points).moved(x, y))
    return cir

def LED(ly, l, h, x=0, y=0):
    ly_data = str(layout.get_info(ly))
    ly_idx = df[df['Layer'] == ly_data].index.values.astype(int)[0]
    ly_name = df['Name'][ly_idx]

    led = layout.create_cell(ly_name)
    led.shapes(ly).insert(Rec(l/2+x, h/2+y, l, h))
    return led

def sha_shape(l=50*factor,h=50*factor,lw=5*factor):
    rec = pya.Region()
    for k in range(int(l/lw/3)):
        if 4*lw*k+lw < l or 4*lw*k+lw == l:
            rec.insert(pya.Box(4*lw*k, 0, 4*lw*k+lw, h-2*lw))
        if 4*lw*k+lw+2*lw < l or 4*lw*k+lw+2*lw == l:
            rec.insert(pya.Box(4*lw*k+2*lw, 2*lw, 4*lw*k+lw+2*lw, h))
    rec.insert(pya.Box(0, 0, l, lw))
    rec.insert(pya.Box(0, 0, lw, h))
    rec.insert(pya.Box(0, h-lw, l, h))
    
    return rec

# Return Cell Pixel
# input [size of Pixel] OR [size and gap of LED]
def Pixel(l, h, type=1, rgb='rgb', ratio='316'):
    rc = int(ratio[0])
    gc = int(ratio[1])
    bc = int(ratio[2])

    edge_gap_x = 3*factor
    led_gap = 3*factor
    edge_gap_y = 3*factor
    n_gap = 12*factor

    if type == 1:
        led_x = (l - 2*led_gap - 2*edge_gap_x)/3
        led_y = h - n_gap - edge_gap_y
        rsize = [led_x, led_y]
        gsize = [led_x, led_y]
        bsize = [led_x, led_y]
        rpos = [edge_gap_x, n_gap]
        gpos = [edge_gap_x + led_x + led_gap, n_gap]
        bpos = [edge_gap_x + 2*led_x + 2*led_gap, n_gap]
    elif type == 2:
        l0 = l - 2*edge_gap_x
        h0 = h - n_gap - edge_gap_y

        gled_y = (h0-led_gap)*gc/(rc+gc)
        gled_x = (l0-led_gap)*gc*h0/(bc*gled_y+gc*h0)
        rled_x = gled_x
        rled_y = h0-led_gap-gled_y
        bled_x = l0-led_gap-gled_x
        bled_y = h0
        rsize = [rled_x, rled_y]
        gsize = [gled_x, gled_y]
        bsize = [bled_x, bled_y]
        rpos = [edge_gap_x, n_gap+gled_y+led_gap]
        gpos = [edge_gap_x, n_gap]
        bpos = [edge_gap_x + rled_x + led_gap, n_gap]
    elif type == 3:
        l0 = l - 2*edge_gap_x
        h0 = h - n_gap - edge_gap_y

        rsize = [l0, h0]
        gsize = [l0, h0]
        bsize = [l0, h0]
        rpos = [edge_gap_x, n_gap]
        gpos = [edge_gap_x, n_gap]
        bpos = [edge_gap_x, n_gap]

    pixel_box = Rec(l/2, h/2, l, h)
    pixel = layout.create_cell('Pixel'+rgb.upper()+str(type))
    pixel.shapes(l10).insert(pixel_box)
    if 'r' in rgb.lower():
        rled = LED(l20, rsize[0], rsize[1], rpos[0], rpos[1])
        pixel.insert(pya.CellInstArray(rled.cell_index(),pya.Trans(0, 0)))
    if 'g' in rgb.lower():
        gled = LED(l30, gsize[0], gsize[1], gpos[0], gpos[1])
        pixel.insert(pya.CellInstArray(gled.cell_index(),pya.Trans(0, 0)))
    if 'b' in rgb.lower():
        bled = LED(l40, bsize[0], bsize[1], bpos[0], bpos[1])
        pixel.insert(pya.CellInstArray(bled.cell_index(),pya.Trans(0, 0)))
    return pixel

def Pixel1(l, h):

    pixel_box = Rec(l/2, h/2, l, h)
    pixel = layout.create_cell('Pixels')
    pixel.shapes(l40).insert(pixel_box)
    pixel.shapes(l20).insert(pixel_box.transform(pya.Trans(pitch_x, 0)))
    pixel.shapes(l40).insert(pixel_box)
    pixel.shapes(l30).insert(pixel_box.transform(pya.Trans(pitch_x, 0)))
    pixel.shapes(l40).insert(pixel_box)
    csl_box = Rec(l/2, h/2, l-10*factor, h-10*factor)
    pixel.shapes(l50).insert(csl_box)
    pixel.shapes(l50).insert(csl_box.transform(pya.Trans(pitch_x, 0)))
    pixel.shapes(l50).insert(csl_box.transform(pya.Trans(pitch_x, 0)))
    pmetal = Rec(l/2, h/2, 20*factor, h+100*factor)
    pixel.shapes(l70).insert(pmetal)
    pixel.shapes(l70).insert(pmetal.transform(pya.Trans(pitch_x, 0)))
    pixel.shapes(l70).insert(pmetal.transform(pya.Trans(pitch_x, 0)))

    pmetal_sha = sha_shape(l, h, lw=5*factor) + pya.Box(0, 0, 20*factor, 10*factor).transformed(pya.Trans(l/2-10*factor, h)) + \
        pya.Box(0, 0, 20*factor, 10*factor).transformed(pya.Trans(l/2-10*factor, -10*factor))
    pixel.shapes(l80).insert(pmetal_sha)
    pixel.shapes(l80).insert(pmetal_sha.transform(pya.Trans(pitch_x, 0)))
    pixel.shapes(l80).insert(pmetal_sha.transform(pya.Trans(pitch_x, 0)))
    return pixel

def auto_router(n=30, up_l=2400*factor, h=700*factor,boxwidth=100*factor,linewidth=20*factor,linegap=50*factor, box_hgap=30*factor, box_tip=50*factor):

    boxpitch = up_l/n
    linepitch = linewidth+linegap
    low_l = n*linepitch-linegap

    center_x = low_l/2
    up_left = center_x-up_l/2

    metal = pya.Region()
    for k in range(n):
        metal += pya.Box(0+k*linepitch, 0, linewidth+k*linepitch, box_tip)

        if k%2 == 1:
            metal += pya.Box(up_left+k*boxpitch, h-boxwidth, up_left+boxwidth+k*boxpitch, h)
            metal += pya.Box(up_left+k*boxpitch+boxwidth/2-linewidth/2, h-2*boxwidth-box_hgap-box_tip, up_left+k*boxpitch+boxwidth/2+linewidth/2, h-boxwidth)
        else:
            metal += pya.Box(up_left+k*boxpitch, h-2*boxwidth-box_hgap, up_left+boxwidth+k*boxpitch, h-boxwidth-box_hgap)
            metal += pya.Box(up_left+k*boxpitch+boxwidth/2-linewidth/2, h-2*boxwidth-box_hgap-box_tip, up_left+k*boxpitch+boxwidth/2+linewidth/2, h-2*boxwidth-box_hgap)
        metal += pya.Polygon([pya.Point(0+k*linepitch, box_tip), pya.Point(up_left+k*boxpitch+boxwidth/2-linewidth/2, h-2*boxwidth-box_hgap-box_tip), \
                                        pya.Point(up_left+k*boxpitch+boxwidth/2+linewidth/2, h-2*boxwidth-box_hgap-box_tip), pya.Point(linewidth+k*linepitch, box_tip)])
    return metal


die_bound = Rec(die_size_x/2, die_size_y/2, die_size_x, die_size_y)
wafer_bound = Circle(mask_size/2, mask_size/2, wafer_size/2)
mask_bound = Rec(mask_size/2, mask_size/2, mask_size, mask_size)
#================================================================================#
#============================  Generator and Output  ============================#
#================================================================================#


# if __name__ == '__main__':
#     # print(outfile)
#     ly = layout.create_cell('Test')
#     ly.insert(pya.CellInstArray(Pixel1(40*factor,40*factor).cell_index(), pya.Trans(0, 0)))

#     layout.write('test.gds')