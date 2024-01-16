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
outfile = setup.align_out

#================================================================================#
#================================================================================#
#=======================>>>>>>>>>>  ALIGNMARK  <<<<<<<<<<========================#
#================================================================================#
#================================================================================#


def align_cross():
    align_cross_h1 = pya.Region()
    align_cross_h1.insert(pya.Box(-20*factor, -2*factor, 20*factor, 2*factor))
    align_cross_h2 = pya.Region()
    align_cross_h2.insert(pya.Box(-60*factor, -6*factor, -20*factor, 6*factor))
    align_cross_h3 = pya.Region()
    align_cross_h3.insert(pya.Box(20*factor, -6*factor, 60*factor, 6*factor))
    align_cross_h4 = pya.Region()
    align_cross_h4.insert(pya.Box(-100*factor, -10*factor, -60*factor, 10*factor))
    align_cross_h5 = pya.Region()
    align_cross_h5.insert(pya.Box(60*factor, -10*factor, 100*factor, 10*factor))

    align = align_cross_h1+align_cross_h2+align_cross_h3+align_cross_h4+align_cross_h5
    return align


def align_cross_box(ly):
    i_ly_data = str(layout.get_info(ly))
    i_ly_idx = df[df['Layer'] == i_ly_data].index.values.astype(int)[0]
    i_ly_name = df['Name'][i_ly_idx]

    vscale = layout.create_cell('Align_'+i_ly_name)
    vscale.shapes(ly).insert(align_cross())
    vscale.shapes(ly).insert(align_cross().transform(pya.Trans.R90))
    vscale.shapes(ly).insert(pya.Box(-100*factor, 200*factor, 0*factor, 300*factor))
    return vscale

def reg_mark_arr():
    reg_mark = layout.create_cell('RegularMark')
    lys = setup.lys
    for ly in lys:
        mark = align_cross_box(ly)
        reg_mark.insert(pya.CellInstArray(mark.cell_index(),pya.Trans(100*factor, 100*factor),pya.Vector(0, 0), pya.Vector(0, 500*factor), 1, 5))

    # single mark above
    vscale=layout.create_cell('Align_TOP')
    for ly in lys:
        vscale.shapes(ly).insert(align_cross())
        vscale.shapes(ly).insert(align_cross().transform(pya.Trans.R90))
    reg_mark.insert(pya.CellInstArray(vscale.cell_index(),pya.Trans(100*factor, 5*500*factor+100*factor),pya.Vector(0, 0), pya.Vector(0, 0), 1, 1))
    return reg_mark


#================================================================================#
#===============================  Vernier Scale  ================================#
#================================================================================#

def scale(lw=2*factor):

    align_cross_h0 = pya.Region()
    align_cross_h0.insert(pya.Box(-40*factor, -2*factor, 20*factor, 2*factor))
    align_cross_h1 = pya.Region()
    align_cross_h1.insert(pya.Box(-25*factor, -4*factor, 5*factor, 4*factor))

    align_cross_h2 = pya.Region()
    align_cross_h2.insert(pya.Box(38*factor, -lw/2, 50*factor, lw/2))
    align_cross_h3 = pya.Region()
    align_cross_h3.insert(pya.Box(38*factor, (1/2+1)*lw, 48*factor, (1/2+2)*lw))
    align_cross_h4 = pya.Region()
    align_cross_h4 = align_cross_h3.moved(0, 2*lw)
    align_cross_h5 = pya.Region()
    align_cross_h5 = align_cross_h3.moved(0, 4*lw)
    align_cross_h6 = pya.Region()
    align_cross_h6 = align_cross_h3.moved(0, -4*lw)
    align_cross_h7 = pya.Region()
    align_cross_h7 = align_cross_h3.moved(0, -6*lw)
    align_cross_h8 = pya.Region()
    align_cross_h8 = align_cross_h3.moved(0, -8*lw)

    align_cross_h9 = pya.Region()
    align_cross_h9.insert(pya.Box(26*factor, -lw/2, 38*factor, lw/2))
    align_cross_h10 = pya.Region()
    align_cross_h10.insert(pya.Box(28*factor, (1/2+1)*lw+1*factor, 38*factor, (1/2+2)*lw+1*factor))
    align_cross_h11 = pya.Region()
    align_cross_h11 = align_cross_h10.moved(0, 2*lw+1*factor)
    align_cross_h12 = pya.Region()
    align_cross_h12 = align_cross_h10.moved(0, (2*lw+1*factor)*2)
    align_cross_h13 = pya.Region()
    align_cross_h13 = align_cross_h10.moved(0, -(2*lw+1*factor)*2)
    align_cross_h14 = pya.Region()
    align_cross_h14 = align_cross_h10.moved(0, -(2*lw+1*factor)*3)
    align_cross_h15 = pya.Region()
    align_cross_h15 = align_cross_h10.moved(0, -(2*lw+1*factor)*4)

    align_body = align_cross_h0+align_cross_h1

    align_low = align_body + align_cross_h2+align_cross_h3+align_cross_h4+align_cross_h5+\
    align_cross_h6+align_cross_h7+align_cross_h8

    align_up = align_body + align_cross_h0+align_cross_h1+align_cross_h9+align_cross_h10+align_cross_h11+\
    align_cross_h12+align_cross_h13+align_cross_h14+align_cross_h15

    return align_up, align_low

def s_mark(ly1, ly2):
    i_ly_data1 = str(layout.get_info(ly1))
    i_ly_idx1 = df[df['Layer'] == i_ly_data1].index.values.astype(int)[0]
    i_ly_name1 = df['Name'][i_ly_idx1]
    i_ly_data2 = str(layout.get_info(ly2))
    i_ly_idx2 = df[df['Layer'] == i_ly_data2].index.values.astype(int)[0]
    i_ly_name2 = df['Name'][i_ly_idx2]

    s_mark = layout.create_cell('Scale_'+i_ly_name1+'_'+i_ly_name2)
    align_up, align_low = scale(lw=4*factor)

    s_mark.shapes(ly1).insert(align_up.transformed(pya.Trans(50*factor,260*factor)))
    s_mark.shapes(ly1).insert(align_up.transformed(pya.Trans.R270).transformed(pya.Trans(40*factor,250*factor)))
    s_mark.shapes(ly2).insert(align_low.transformed(pya.Trans(50*factor,260*factor)))
    s_mark.shapes(ly2).insert(align_low.transformed(pya.Trans.R270).transformed(pya.Trans(40*factor,250*factor)))
    return s_mark

def scale_mark_arr():

    scale_mark = layout.create_cell('ScaleMark')
    scale_mark.insert(pya.CellInstArray(s_mark(l30, l20).cell_index(),pya.Trans(100*factor, (4*500+100)*factor)))
    scale_mark.insert(pya.CellInstArray(s_mark(l40, l20).cell_index(),pya.Trans(100*factor, (3*500+100)*factor)))
    scale_mark.insert(pya.CellInstArray(s_mark(l10, l40).cell_index(),pya.Trans(100*factor, (2*500+100)*factor)))
    scale_mark.insert(pya.CellInstArray(s_mark(l50, l10).cell_index(),pya.Trans(100*factor, (1*500+100)*factor)))
    scale_mark.insert(pya.CellInstArray(s_mark(l60, l10).cell_index(),pya.Trans(100*factor, (0*500+100)*factor)))
    scale_mark.insert(pya.CellInstArray(s_mark(l70, l10).cell_index(),pya.Trans(100*factor, (0*500+100)*factor)))
    return scale_mark

if __name__ == '__main__':
    align_mark = layout.create_cell('AlignMark')

    align_mark.insert(pya.CellInstArray(reg_mark_arr().cell_index(),pya.Trans(0, 0)))
    align_mark.insert(pya.CellInstArray(scale_mark_arr().cell_index(),pya.Trans(0, 0)))
    layout.write(outfile)