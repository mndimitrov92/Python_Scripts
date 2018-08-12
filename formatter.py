from os import listdir,rename
import re

def format_image(image_name):
    """ Function formatting the image name """
    img = r"%s" %image_name
    formatted_img = img.replace('&','and')
    formatted_img = re.sub('[^a-zA-Z0-9.]+','_', formatted_img, flags = re.IGNORECASE)
    return formatted_img

def image_capturer(item):
    """ Collecting only the images from the directory """
    extentions = ['jpg', 'jpeg', 'bmp', 'gif', 'png']
    file_ext = item.split('.')[-1]
    if file_ext in extentions:
        return item

def rename_image(current_name, new_name):
    """ Replacing the image name with the formatted one """
    return rename(current_name, new_name)

def populate_res(img_number, filename):
    res_tag = '<res label="_{}"><div class="img-holder"><img src="[rel {}]" /></div></res>'.format(img_number,str(filename))
    return res_tag

if __name__ == "__main__":
    while True:
        current_dir = raw_input("Type the directory where the images are to be formatted, or . for current directory: ")
        dir_contents = os.listdir(current_dir)
        print dir_contents
        
        all_images = []
        formatted_images = []
        
        for item in dir_contents:
            all_images.append(image_capturer(item))
        
        for x in all_images:
            formatted_images.append(format_image(x))
        
        # Renaming the files
        for i,e in enumerate(all_images):
            rename(e, formatted_images[i])

        # preparing the res tags and exporting the file 
        export_res = raw_input("Do you want to export a file with the images placed in resources? 1=yes, 0=no :")
        if eval(export_res):
            resource_tags = []
            for i,eachImg in enumerate(formatted_images):
                resource_tags.append(populate_res(i+1,eachImg))

            with open('shtsksm.txt', 'w') as f:
                f.write('\n'.join(resource_tags))

        # exit condition 
        exit_text = raw_input("Do you want to format images in another directory (1 = yes; 0 = no) :")
        if not eval(exit_text):
            print "Job done!"
            break
