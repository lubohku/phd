import pya
import setup
from setup import Pixel1, auto_router
layout = setup.layout

#================================================================================#
#=========================  LAYER AND SIZE PARAMETERS   =========================#
#================================================================================#

l1001 = setup.l1001
l1002 = setup.l1002
l1003 = setup.l1003
l10 = setup.l10 # Isolation
l20 = setup.l20 # Large pillar
l30 = setup.l30 # Small pillar
l40 = setup.l40 # Shallow etch
l50 = setup.l50 # CSL
l60 = setup.l60 # n-Open
l70 = setup.l70 # Metal
l80 = setup.l80 # Metal
l1000 = setup.l1000


factor = setup.factor
df = setup.df
outfile = setup.body_out
mask_size = setup.mask_size
mask_bound = setup.mask_bound
wafer_size = setup.wafer_size
wafer_bound = setup.wafer_bound
die_size_x = setup.die_size_x
die_size_y = setup.die_size_y
die_bound = setup.die_bound
dicing = setup.dicing
die_pitch_x = setup.die_pitch_x
die_pitch_y = setup.die_pitch_y
die_col = setup.die_col
die_row = setup.die_row
die_shift_x = setup.die_shift_x
die_shift_y = setup.die_shift_y
lys = setup.lys
#================================================================================#
#===============================  PIXEL PARAMETERS   ============================#
#================================================================================#

pixel_x = setup.pixel_x
pixel_y = setup.pixel_y
led_x = 12*factor
led_y = 35*factor
edge_gap_x = 3*factor
led_gap = 3*factor
edge_gap_y = 3*factor
n_gap = 12*factor

margin_pixel = setup.margin_pixel
pitch_x = setup.pitch_x
pitch_y = setup.pitch_y

margin_die_x = setup.die_margin_x
margin_die_y = setup.die_margin_y
die_no_font = setup.die_no_font
die_no_font_head = setup.die_no_font_head

# col = int((die_size_x-dicing-margin_die_x)/pitch_x)
# row = int((die_size_y-dicing-margin_die_y)/pitch_y)

col = 30
row = 30
# print('col: ' + str(col) + ', row: ' + str(row))
pixels_shiftx = (die_size_x-pitch_x*col+margin_pixel+(col%3)*pitch_x)/2
pixels_shifty = (die_size_y-pitch_y*row+margin_pixel)/2
# pixels_shiftx = 1000*factor
# pixels_shifty = 1000*factor
def logosh():
    options = pya.LoadLayoutOptions()
    options.warn_level = 0
    layout1 = pya.Layout()
    layout1.read('logo.gds',options)
    logoshape = layout1.top_cell().shapes(l10)
    return pya.Region(logoshape)
#================================================================================#
#================================================================================#
#======================>>>>>>>>>>  GENERATE LED  <<<<<<<<<<======================#
#================================================================================#
#================================================================================#

if __name__ == '__main__':
    #================================================================================#
    #======================  Die, Pixel and deep etch isolation  ====================#
    #================================================================================#
    pixel = Pixel1(pixel_x, pixel_y)
    mask_body = layout.create_cell('MASK_BODY')
    die = layout.create_cell('DIE')
    label = layout.create_cell('DIE_LABEL')
    rowpixel = layout.create_cell('Row')
    array = layout.create_cell('Array')
    pmetal = layout.create_cell('pMetal')
    nmetal = layout.create_cell('nMetal')
    #================================================================================#
    # Deep Etch 
    rowpixel.insert(pya.CellInstArray(pixel.cell_index(),pya.Trans(pya.Point(0, 0)),pya.Vector(3*pitch_x, 0 ), pya.Vector(0, 0), col/3, 1))
    rowpixel.shapes(l10).insert(pya.Box(-100*factor, -2.5*factor, col*pitch_x-(col%3)*pitch_x-margin_pixel+100*factor, pixel_y+2.5*factor))

    # n-Open

    rowpixel.shapes(l60).insert(pya.Box(-95*factor, 2.5*factor, -50*factor, pixel_y-2.5*factor))
    rowpixel.shapes(l60).insert(pya.Box(col*pitch_x-(col%3)*pitch_x-margin_pixel+100*factor-50*factor, 2.5*factor, col*pitch_x-(col%3)*pitch_x-margin_pixel+95*factor, pixel_y-2.5*factor))

    # Array
    trans1 = pya.Trans(pya.Point(pixels_shiftx, pixels_shifty))
    new_instance = pya.CellInstArray(rowpixel.cell_index(),trans1,pya.Vector(0, 0 ), pya.Vector(0, pitch_y), 1, row)
    array.insert(new_instance)
    # die.insert(pya.CellInstArray(array.cell_index(),pya.Trans(0, 0),pya.Vector(pitch_x*col+1000*factor, 0), pya.Vector(0, pitch_y*row+1000*factor), 2, 2))
    die.insert(pya.CellInstArray(array.cell_index(),pya.Trans(0, 0)))

    # Router
    metalwidth=20*factor
    metalgap_x=pitch_x-metalwidth
    metalgap_y=pitch_y-metalwidth
    pmetal.shapes(l70).insert(auto_router(n=int(col/3)*3, up_l=col*80*factor, h=col*25*factor, linewidth=metalwidth, linegap=metalgap_x))
    pmetal.shapes(l80).insert(auto_router(n=int(col/3)*3, up_l=col*80*factor, h=col*25*factor, linewidth=metalwidth, linegap=metalgap_x))
    trans2 = pya.Trans(pya.Point(pixels_shiftx+pixel_x/2-20*factor/2, pixels_shifty+pitch_y*row-margin_pixel))
    array.insert(pya.CellInstArray(pmetal.cell_index(),trans2))
    trans3 = pya.Trans(pya.Point(pixels_shiftx+pitch_x*(col-(col%3))-margin_pixel-pixel_x/2+20*factor/2, pixels_shifty))
    array.insert(pya.CellInstArray(pmetal.cell_index(),trans3*pya.Trans.R180))

    nmetal.shapes(l70).insert(auto_router(n=row, up_l=row*80*factor, h=row*25*factor, linewidth=metalwidth, linegap=metalgap_y))
    nmetal.shapes(l80).insert(auto_router(n=row, up_l=row*80*factor, h=row*25*factor, linewidth=metalwidth, linegap=metalgap_y))
    trans4 = pya.Trans(pya.Point(pixels_shiftx-50*factor, pixels_shifty+pixel_y/2-20*factor/2))
    array.insert(pya.CellInstArray(nmetal.cell_index(),trans4*pya.Trans.R90))
    trans5 = pya.Trans(pya.Point(pixels_shiftx+pitch_x*(col-(col%3))-margin_pixel+50*factor, pixels_shifty+pitch_y*row-margin_pixel-pixel_y/2+20*factor/2))
    array.insert(pya.CellInstArray(nmetal.cell_index(),trans5*pya.Trans.R270))

    #================================================================================#
    #====================================  Dicing1  =================================#
    #================================================================================#

    device_bound=die_bound.sized(-dicing/2)
    dicing_shape = die_bound-device_bound
    die.shapes(l1003).insert(die_bound)
    die.shapes(l1000).insert(dicing_shape)

    #================================================================================#
    #====================================  Dicing2  =================================#
    #================================================================================#
    array_h = array.bbox().height()
    array_w = array.bbox().width()

    dic_dis = 200*factor
    dic_wid = 50*factor
    dicing_mark_v1 = pya.Box(die_size_x/2-array_w/2-(dic_dis+dic_wid), die_size_y/2+array_h/2, die_size_x/2-array_w/2-dic_dis, die_size_y/2+array_h/2+(dic_dis+dic_wid+50*factor))
    dicing_mark_v2 = pya.Box(die_size_x/2+array_w/2+dic_dis, die_size_y/2-array_h/2, die_size_x/2+array_w/2+(dic_dis+dic_wid), die_size_y/2-array_h/2-(dic_dis+dic_wid+50*factor))
    die.shapes(l1000).insert(dicing_mark_v1)
    die.shapes(l1000).insert(dicing_mark_v2)

    dicing_mark_h1 = pya.Box(die_size_x/2+array_w/2, die_size_y/2-array_h/2-(dic_dis+dic_wid), die_size_x/2+array_w/2+(dic_dis+dic_wid+50*factor), die_size_y/2-array_h/2-dic_dis)
    dicing_mark_h2 = pya.Box(die_size_x/2-array_w/2, die_size_y/2+array_h/2+dic_dis, die_size_x/2-array_w/2-(dic_dis+dic_wid+50*factor), die_size_x/2+array_h/2+(dic_dis+dic_wid))
    die.shapes(l1000).insert(dicing_mark_h1)
    die.shapes(l1000).insert(dicing_mark_h2)
    #================================================================================#
    #=====================================  Logo  ===================================#
    #================================================================================#s
    logo = layout.create_cell('logo')
    logoshape = logosh()
    logo_h = logoshape.bbox().height()
    logo_w = logoshape.bbox().width()
    for ly in lys:
        logo.shapes(ly).insert(logoshape, pya.Trans(pya.Point(0, 0)))
    # logo.write('logo.gds')
    # die.insert(pya.CellInstArray(logo.cell_index(),pya.Trans(pya.Point(die_size_x, die_size_y))))
    die.insert(pya.CellInstArray(logo.cell_index(),pya.Trans(pya.Point(die_size_x-dicing/2-logo_w/2-50*factor, die_size_y-dicing/2-logo_h/2-50*factor))))
    trans6 = pya.Trans(pya.Point(die_shift_x, die_shift_y))
    mask_body.insert(pya.CellInstArray(die.cell_index(),trans6,pya.Vector(die_pitch_x, 0 ), pya.Vector(0, die_pitch_y), die_col, die_row))

    #================================================================================#
    #=====================================  Label  ==================================#
    #================================================================================#

    for i in range(die_row):
        row_text = pya.TextGenerator.default_generator().text(str(die_row-i), die_no_font_head)
        row_text_h = row_text.bbox().height()
        row_text_w = row_text.bbox().width()
        label.shapes(l1001).insert(row_text, pya.Trans(pya.Point(die_shift_x - row_text_w - 1500*factor, \
            die_shift_y + die_size_y/2 - row_text_h/2 + i*die_pitch_y)))
        for j in range(die_col):
            # Die number A3 ...
            # die_no = pya.TextGenerator.default_generator().text(chr(j+ord('A'))+str(die_row-i), 0.000003)
            die_no = pya.TextGenerator.default_generator().text(chr(j+ord('A'))+str(die_row-i), die_no_font)
            die_no_h = die_no.bbox().height()
            die_no_w = die_no.bbox().width()
            die_no_shift_y = ((die_size_y - dicing - pitch_y*row - col*25*factor + margin_pixel)/2 - die_no_h)/2
            for ly in lys:
                # Left Top
                label.shapes(ly).insert(die_no, pya.Trans(pya.Point(die_shift_x + dicing/2 + 50*factor + j*die_pitch_x, \
                    die_shift_y+ die_size_y - dicing/2 - 50*factor - die_no_h + i*die_pitch_y)))

                # Left Top with Shift
                # label.shapes(ly).insert(die_no, pya.Trans(pya.Point(die_shift_x + dicing/2 + 50*factor + j*die_pitch_x+j*(die_no_w+30*factor), \
                #     die_shift_y+ die_size_y - dicing/2 - 50*factor - die_no_h + i*die_pitch_y-(die_row-1-i)*(die_no_h+30*factor))))

                # Center Top
                # label.shapes(ly).insert(die_no, pya.Trans(pya.Point(die_shift_x + die_size_x/2 + j*die_pitch_x - die_no_w/2, \
                #     die_shift_y + die_size_y + i*die_pitch_y - die_no_h - dicing/2 - die_no_shift_y)))
    for k in range(die_col):
        col_text = pya.TextGenerator.default_generator().text(chr(k+ord('A')), die_no_font_head)
        col_text_h = col_text.bbox().height()
        col_text_w = col_text.bbox().width()
        label.shapes(l1001).insert(col_text, pya.Trans(pya.Point(die_shift_x + die_size_x/2 - col_text_w/2 + k*die_pitch_x, \
            die_shift_y + die_row*die_pitch_y + 1500*factor)))

    # mask_body.shapes(l1001).insert(mask_bound)
    mask_body.insert(pya.CellInstArray(label.cell_index(),pya.Trans(pya.Point(0, 0))))
    mask_body.shapes(l1002).insert(wafer_bound)

    layout.write(outfile)
