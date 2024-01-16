import pya
import setup
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
outfile = setup.lichk_out

#================================================================================#
#================================================================================#
#=======================>>>>>>>>>>  ALIGNMARK  <<<<<<<<<<========================#
#================================================================================#
#================================================================================#

#================================================================================#
#===================================  CDline  ====================================#
#================================================================================#

def cdl(ly):
    ly_data = str(layout.get_info(ly))
    ly_idx = df[df['Layer'] == ly_data].index.values.astype(int)[0]
    ly_name = df['Name'][ly_idx]

    cd_coor = [0,1,2,3,4,6,8,10,12,15,18,21,24,28,32,36,40,45,50,55]
    cdline = layout.create_cell('CDline_'+ly_name)
    cdl = pya.Region()
    for i in range(10):
        temp = pya.Region()
        temp.insert(pya.Box(cd_coor[2*i]*factor, 0, cd_coor[2*i+1]*factor, 40*factor))
        cdl+=temp

    text = pya.TextGenerator.default_generator().text(str(layout.get_info(ly)).replace("/",""), 0.00004)
    cdline.shapes(ly).insert(text, pya.Trans(1, False, (25-5)*factor, 5*factor))
    cdline.shapes(ly).insert(cdl, pya.Trans(25*factor, 0))
    return cdline

def cdline_array():
    deep_frame1 = pya.Region()
    deep_frame1.insert(pya.Box(0, 0, 90*factor, 40*factor))
    cdb1 = cdl(l10)
    cdb2 = cdl(l20)
    cdb2.shapes(l10).insert(deep_frame1, pya.Trans(-5*factor, 0))
    cdb2.shapes(l40).insert(deep_frame1, pya.Trans(-5*factor, 0))
    cdb3 = cdl(l30)
    cdb3.shapes(l10).insert(deep_frame1, pya.Trans(-5*factor, 0))
    cdb3.shapes(l40).insert(deep_frame1, pya.Trans(-5*factor, 0))
    cdb4 = cdl(l40)
    cdb4.shapes(l10).insert(deep_frame1, pya.Trans(-5*factor, 0))
    cdb5 = cdl(l50)
    cdb6 = cdl(l60)
    cdb7 = cdl(l70)

    cdb_mark = layout.create_cell('CDline')
    for k, c_mark in enumerate([cdb1, cdb2, cdb3, cdb4, cdb5, cdb6, cdb7]):
        cdb_mark.insert(pya.CellInstArray(c_mark.cell_index(),pya.Trans(k*100*factor, 0)))
    return cdb_mark

#================================================================================#
#=================================  EXPOSURE  ===================================#
#================================================================================#

def exposure(ly):
    ly_data = str(layout.get_info(ly))
    ly_idx = df[df['Layer'] == ly_data].index.values.astype(int)[0]
    ly_name = df['Name'][ly_idx]

    expo_mark = layout.create_cell('EXPOSURE_'+ly_name)
    expo = pya.Region()
    for j in range(4):
        temp1 = pya.Region()
        temp1.insert(pya.Box(0, (5+10*j)*factor, 5*factor, (10+10*j)*factor))
        temp2 = pya.Region()
        temp2.insert(pya.Box(20*factor, (5+10*j)*factor, 25*factor, (10+10*j)*factor))
        temp3 = pya.Region()
        temp3.insert(pya.Box(40*factor, (5+10*j)*factor, 45*factor, (10+10*j)*factor))
        temp4 = pya.Region()
        temp4.insert(pya.Box(5*factor, (0+10*j)*factor, 10*factor, (5+10*j)*factor))
        temp5 = pya.Region()
        temp5.insert(pya.Box(24*factor, (0+10*j)*factor, 29*factor, (5+10*j)*factor))
        temp6 = pya.Region()
        temp6.insert(pya.Box(46*factor, (0+10*j)*factor, 51*factor, (5+10*j)*factor))
        expo+=(temp1+temp2+temp3+temp4+temp5+temp6)

    text = pya.TextGenerator.default_generator().text(str(layout.get_info(ly)).replace("/",""), 0.00004)
    expo_mark.shapes(ly).insert(text, pya.Trans(1, False, (25-5)*factor, 5*factor))
    expo_mark.shapes(ly).insert(expo, pya.Trans(25*factor, 0))
    return expo_mark

def expo_array():
    deep_frame3 = pya.Region()
    deep_frame3.insert(pya.Box(0, 0, 85*factor, 50*factor))
    expo1 = exposure(l10)
    expo2 = exposure(l20)
    expo2.shapes(l10).insert(deep_frame3, pya.Trans(-5*factor, -5*factor))
    expo2.shapes(l40).insert(deep_frame3, pya.Trans(-5*factor, -5*factor))
    expo3 = exposure(l30)
    expo3.shapes(l10).insert(deep_frame3, pya.Trans(-5*factor, -5*factor))
    expo3.shapes(l40).insert(deep_frame3, pya.Trans(-5*factor, -5*factor))
    expo4 = exposure(l40)
    expo4.shapes(l10).insert(deep_frame3, pya.Trans(-5*factor, -5*factor))
    expo5 = exposure(l50)
    expo6 = exposure(l60)
    expo7 = exposure(l70)

    expo_mark = layout.create_cell('Exposure')
    for k, e_mark in enumerate([expo1, expo2, expo3, expo4, expo5, expo6, expo7]):
        expo_mark.insert(pya.CellInstArray(e_mark.cell_index(),pya.Trans(k*100*factor, 0)))
    return expo_mark

if __name__ == '__main__':
    alignmark = layout.create_cell('Lithocheck')
    alignmark.insert(pya.CellInstArray(cdline_array().cell_index(),pya.Trans(0, 0*factor)))
    alignmark.insert(pya.CellInstArray(expo_array().cell_index(),pya.Trans(0, 55*factor)))
    layout.write(outfile)