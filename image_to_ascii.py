#image to ascii
from PIL import Image
import streamlit as st
st.set_page_config(page_title="Image to ASCII")
st.title("Image to ASCII")
st.caption("Created by Drew Warner")
st.caption("V1.1D")

image_upload = st.file_uploader("Upload an image or drag from another tab below", type=["jpg", "jpeg", "png", "webp"])





downscale_factor = st.number_input("Downscale Factor", min_value=1, value=10)

invert = st.toggle("Invert Colors (Use in light mode, otherwise leave off)")

#characters = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']#light to dark
characters_input = st.text_input("Input an ascii gradient from light to dark separated by commas (no spaces needed for separation), or leave blank for the default. Spaces allowed as colors in the gradient")

if st.button("Process"):
    if not image_upload:
        st.error("Please upload a file")
    else:
        try:
            if characters_input not in [None, ""]:
                characters = characters_input.split(',')
            else:
                characters = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        except:
            st.error("Cannot parse ascii gradient input")


        base_image = Image.open(image_upload)
        size_base = base_image.size
        image = base_image.resize((int(size_base[0]/downscale_factor), int(size_base[1]/downscale_factor)), resample=Image.BICUBIC)
        pix = image.load()
        size = image.size
        #Increase contrast by finding minimum and maximum color values
        colors = []
        for y in range(size[1]):
            for x in range(size[0]):
                color = pix[x, y]
                color = (color[0] + color[1] + color[2])/3#grayscale
                if invert:
                    color = 255-color
                colors.append(color)
        
        min_color = min(colors)#subtract this from any color value to bottom out values
        max_color = max(colors)#rescale all colors to make this the maximum value at 1
        colors = []
        total = ""
        for y in range(size[1]):
            line = []
            row = ""
            for x in range(size[0]):
                color = pix[x, y]
                color = (color[0] + color[1] + color[2])/3#grayscale
                if invert:
                    color = 255-color
                color = (color-min_color)*((max_color+min_color)/255)#rescale for contrast

                colors.append(color)

                color = color * ((len(characters))/255)#0.03921568627 is for 10 gradient items magic number to convert to 1-10    
                color = round(color)
                color = color - 1
                line.append(str(characters[color]))
            for i in range(len(line)):
                row += line[i] + line[i]#fix uneven characters
            total += row+"\n"
        st.code(total, language=None)
