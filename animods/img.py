from PIL import Image
import os
from pathlib import Path
from animods.misc import c
# Generate a an.ico file 




def create_ico(path,source):
    """Creates a an.ico file in the specified path using image.jpg 
    
    @Params : 
        path : where the jpeg rests 
        Source : A path that points to where image.jpg is 

    """
    # current_folder = Path.cwd()
    current_folder = Path(path)
    oi_path = Path.joinpath(current_folder, 'c.jpg')
    
    if oi_path.exists():
        print(f'{c.purple}Generating icon from : {oi_path}{c.o}')
        
        tc = Image.new('RGBA', (256, 256), color = (0,0,0,0))
        tc_path = Path.joinpath(current_folder, 'tc.png')
        tc.save(tc_path)
        print(f'{c.b_black}Created Transparent Canvas at : {tc_path}{c.o}')

        # original image resize 
        oi = Image.open(oi_path)
        roi = oi.resize((180, 256))
        roi_path = Path.joinpath(current_folder, 'roi.png')
        roi.save(roi_path,format="png")
        print(f'{c.b_black}Generated Resized PNG at :{roi_path}{c.o}')
        
        rio = Image.open(roi_path)
        tc.paste(rio,(38,0))
        fp_path = Path.joinpath(current_folder, 'fp.png')
        tc.save(fp_path,format="png")
        print(f'{c.b_black}Generated Final PNG at {fp_path}{c.o}')

        fp = Image.open(fp_path)
        sizes = [(256, 256)]
        fpi_path = Path.joinpath(current_folder, 'an.ico')
        fp.save(fpi_path,format="ICO",sizes=sizes)
        print(f'{c.green}Generated Icon at {fpi_path}{c.o}')
        print(f'{c.purple}Cleaning up residual files in {fpi_path}{c.o}')
        residual_files = ['fp.png', 'tc.png','roi.png']
        for file in residual_files : 
            residual_file_path = Path.joinpath(current_folder, file)
            print(f'{c.b_black}Info: {c.red}Removing {residual_file_path}{c.o}')
            # TODO: Danger ... deletion access
            os.remove(residual_file_path)
        print(f'{c.green}Cleaning up complete ...{c.o}')
    else:
        print(f'\n{c.red}Origin image not found {oi_path}{c.o}\n')



