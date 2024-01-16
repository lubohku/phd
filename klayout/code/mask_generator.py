import os
import subprocess
import pya
import setup
import time

start = time.time()
print("################################################################################")
print("#                                                                              #")
print("#                        MASK AUTO GENERATING SCRIPT V0.1                      #")
print("#                            HKU EEE PHD STUDENT LU BO                         #")
print("#                                                                              #")
print("#                 --------------------------------------------                 #")
print("#                 |   Klayout + Python only generate layout  |                 #")
print("#                 | Please do LED BASIC DRC in Klayout Macro |                 #")
print("#                 --------------------------------------------                 #")
print("#                                                                              #")

#================================================================================#
#===========================   GENERATOR AND OUTPUT   ===========================#
#================================================================================#
factor = setup.factor
klayout_path = setup.klayout_path
mask_bound = setup.mask_bound

body_generator = setup.body_gen
lichk_generator = setup.lichk_gen
align_generator = setup.align_gen
testkey_generator = setup.testkey_gen
testdevice_generator = setup.testdevice_gen
extract_layer = setup.extract_layer

outdir = setup.outdir
if not os.path.exists(outdir):
    os.makedirs(outdir)
mask_output = setup.body_out
lichk_output = setup.lichk_out
align_output = setup.align_out
testkey_output = setup.testkey_out
testdevice_output = setup.testdevice_out
final_output = setup.final_out

mask_size = setup.mask_size
die_size_x = setup.die_size_x
die_size_y = setup.die_size_y
die_shift_x = setup.die_shift_x
die_shift_y = setup.die_shift_y
die_col = setup.die_col
die_row = setup.die_row
die_pitch_x = setup.die_pitch_x
die_pitch_y = setup.die_pitch_y

test_gap = setup.test_gap
test_edge = setup.test_edge

dicing = setup.dicing
version = setup.version
skip_exe = setup.skip_exe
#================================================================================#
#================================================================================#
#================================================================================#
import sys
def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "="*x, "."*(size-x), j, count), 
                end='          #\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("", flush=True, file=out)

if __name__ == '__main__':
    if not skip_exe:
        layouts = [body_generator, lichk_generator, align_generator, testkey_generator, testdevice_generator]
        k = 0
        for i in progressbar(range(len(layouts)), "#          GENERATING: ", 40):
            subprocess.call('python "%s"'%layouts[k], 
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
            k += 1
            time.sleep(0.1)
    else:
        print("#  =========================  SKIP PARTS GENERATING  ========================  #")
    
    options = pya.LoadLayoutOptions()
    options.warn_level = 0

    layout = pya.Layout()
    l1001 = layout.layer(1001, 0)
    layout.read(mask_output, options)
    layout.read(lichk_output)
    layout.read(align_output)
    layout.read(testkey_output)
    layout.read(testdevice_output)

    cells = layout.top_cells()
    body = cells[0]
    lithocheck = cells[1]
    alignmark = cells[2]
    testkey = cells[3]
    testdevice = cells[4]
    l1 = lithocheck.bbox().width()
    l1_new = alignmark.bbox().width()
    h_new = alignmark.bbox().height()
    l2 = testkey.bbox().width()
    l_td = testdevice.bbox().width()
    h_td = testdevice.bbox().height()
    h = max(lithocheck.bbox().height(), testkey.bbox().height())
    # test_edge = test_edge - h
    test_pitch_x = die_size_x - dicing - l1 - l2 - 2*test_gap-2*test_edge
    test_pitch_y = die_size_y - dicing - h - 2*test_edge

    #================================================================================#
    #===============================  INLINE & OFFLINE  =============================#
    #================================================================================#
    col = 1
    row = 2

    inline = layout.create_cell('INLINE')
    hori_test_x = die_size_x - dicing - l1 - l2 - 2*test_gap
    inline.insert(pya.CellInstArray(testkey.cell_index(), pya.Trans(pya.Point(hori_test_x/2+dicing/2,test_edge+dicing/2)), \
        pya.Vector(0, 0), pya.Vector(0, test_pitch_y), col, row))
    inline.insert(pya.CellInstArray(testkey.cell_index(), pya.Trans(pya.Point(test_edge+dicing/2, die_size_y-hori_test_x/2-dicing/2))*pya.Trans.R270, \
        pya.Vector(test_pitch_y, 0), pya.Vector(0, 0), row, col))
    
    inline.insert(pya.CellInstArray(lithocheck.cell_index(), pya.Trans(pya.Point(hori_test_x/2+test_gap+l2+dicing/2, test_edge+dicing/2)), \
        pya.Vector(0, 0), pya.Vector(0, test_pitch_y), col, row))
    inline.insert(pya.CellInstArray(lithocheck.cell_index(), pya.Trans(pya.Point(test_edge+dicing/2, die_size_y-hori_test_x/2-test_gap-l2-dicing/2))*pya.Trans.R270, \
        pya.Vector(test_pitch_y, 0), pya.Vector(0, 0), row, col))
    
    hori_test_y_new = die_size_y - dicing - h_new
    inline.insert(pya.CellInstArray(alignmark.cell_index(), pya.Trans(pya.Point(test_edge+dicing/2+h+test_gap, hori_test_y_new/2+dicing/2)), \
        pya.Vector(0, 0), pya.Vector(0, 0), 1, 1))
    inline.insert(pya.CellInstArray(alignmark.cell_index(), pya.Trans(pya.Point(test_edge+dicing/2-test_gap+test_pitch_y, hori_test_y_new/2+dicing/2))\
                                    *pya.Trans.M90, pya.Vector(0, 0), pya.Vector(0, 0), 1, 1))
    hori_test_x_new = die_size_x - dicing - h_new
    inline.insert(pya.CellInstArray(alignmark.cell_index(), pya.Trans(pya.Point(h_new+hori_test_x_new/2+dicing/2, test_edge+dicing/2+h+test_gap))\
                                    *pya.Trans.R90, pya.Vector(0, 0), pya.Vector(0, 0), 1, 1))
    inline.insert(pya.CellInstArray(alignmark.cell_index(), pya.Trans(pya.Point(hori_test_x_new/2+dicing/2, test_edge+dicing/2-test_gap+test_pitch_y))\
                                    *pya.Trans.R270, pya.Vector(0, 0), pya.Vector(0, 0), 1, 1))
    
    offline = layout.create_cell('OFFLINE')
    offline.insert(pya.CellInstArray(testdevice.cell_index(), pya.Trans(pya.Point(test_edge+dicing/2, test_edge+dicing/2+h_td-100*factor)), \
        pya.Vector(die_size_x - dicing - 2*test_edge-l_td, 0), pya.Vector(0, 0), 2, 1))
    
    MASK = layout.create_cell('TOP')
    MASK.insert(pya.CellInstArray(body.cell_index(), pya.Trans(0,0)))
    MASK.insert(pya.CellInstArray(inline.cell_index(), pya.Trans(pya.Point(die_shift_x,die_shift_y)), \
        pya.Vector(die_pitch_x, 0), pya.Vector(0, die_pitch_y), die_col, die_row))
    MASK.insert(pya.CellInstArray(offline.cell_index(), pya.Trans(pya.Point(die_shift_x,die_shift_y)), \
        pya.Vector(die_pitch_x, 0), pya.Vector(0, die_pitch_y), die_col, die_row))
    #================================================================================#
    #====================  NFF&LABEL: SMALL BOXES EACH MASK LAYER  ==================#
    #================================================================================#
    obj_cell = layout.create_cell("OBJ")
    obj_cell.copy_tree(layout.cell("TOP"))
    idx = obj_cell.cell_index()
    all_mask = obj_cell.flatten(idx)

    nff_label = layout.create_cell('NFF&LABEL')
    nff_label.shapes(l1001).insert(mask_bound)
    ly_list = layout.layer_indexes()
    for ly in ly_list:
        if all_mask.shapes(ly).is_empty():
            layout.delete_layer(ly)
            continue
        ly_data = str(layout.get_info(ly))
        if int(ly_data.split('/')[0]) >= 0 and int(ly_data.split('/')[0]) <1000:
            nff_label.shapes(ly).insert(pya.Box(0, 0, 1*factor, 1*factor))
            nff_label.shapes(ly).insert(pya.Box(mask_size-1*factor, mask_size-1*factor, mask_size, mask_size))
    text1 = pya.TextGenerator.default_generator().text('HKU EEE', 0.0000001)
    text2 = pya.TextGenerator.default_generator().text('semi L&D LAB', 0.0000002)
    text3 = pya.TextGenerator.default_generator().text(version, 0.0000001)
    h1 = text1.bbox().height()
    w1 = text1.bbox().width()
    h2 = text2.bbox().height()
    w2 = text2.bbox().width()

    
    nff_label.shapes(l1001).insert(text1, pya.Trans(pya.Point(mask_size-w1-1000*factor, mask_size-h1-1000*factor)))
    nff_label.shapes(l1001).insert(text2, pya.Trans(pya.Point(mask_size-w1-1000*factor, mask_size-h1-h2-1500*factor)))
    nff_label.shapes(l1001).insert(text3, pya.Trans(pya.Point(1000*factor, 1000*factor)))

    #================================================================================#
    #===============================  FINAL GENERATION  =============================#
    #================================================================================#
    
    MASK.insert(pya.CellInstArray(nff_label.cell_index(), pya.Trans(0,0)))
    layout.delete_cell(obj_cell.cell_index())
    MASK.write(final_output)
    # subprocess.Popen('python "%s"'%extract_layer)
    end = time.time()
    print("#                                                                              #")
    print("#                 >>>>>>>>>>  MASK GENERATED IN "+'%.1f'%(end - start)+"s  <<<<<<<<<<               #")
    print("#                      >>>>>>>>>>  OPENING...  <<<<<<<<<<                      #")
    subprocess.Popen('%s "%s"'%(klayout_path, final_output))
    print("#                                                                              #")
    print("################################################################################")
