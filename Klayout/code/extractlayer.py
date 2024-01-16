import pya
import setup

#================================================================================#
#=========================  LAYER AND SIZE PARAMETERS   =========================#
#================================================================================#

final_output = setup.final_out
df = setup.df
mask_size = setup.mask_size
outdir = setup.outdir

#================================================================================#
#================================================================================#
#================================================================================#
def extract(ly, layout):
    TOP = layout.top_cell()
    TOP.transform(pya.Trans(mask_size, 0)*pya.Trans.M90)
    ly_data = str(layout.get_info(ly))
    ly_idx = 0
    ly_name = ''
    if int(ly_data.split('/')[0]) <1000:
        ly_idx = df[df['Layer'] == ly_data].index.values.astype(int)[0]
        ly_name = df['Name'][ly_idx]
    else:
        return

    for layer in ly_list:
        if layer != ly:
            for c in layout.each_cell():
                c.clear(layer)
    TOP.write(outdir+"/layer_"+ly_data.replace("/","_")+"_"+ly_name+".gds")
    layout.delete_cell(TOP.cell_index())

if __name__ == '__main__':
    layout = pya.Layout()
    layout.read(final_output)
    TOP = layout.top_cell()

    ly_list = layout.layer_indexes()
    for ly in ly_list:
        layout.read(final_output)
        extract(ly, layout)

