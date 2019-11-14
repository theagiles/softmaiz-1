# Importación de librerías.
import os
import json
from PIL import ImageDraw
from PIL import Image
import argparse

porcentaje_minimo = 0.5 # Porcentaje de color en el archivo que se agregará. 
transparent_pixels = True # Usaremos pixeles transparentes.
circle_size_create = 500 # Tamaño de archivo circular en pixeles.
color_files_flag = True # Obtener resultados con archivos de imagen. 
   
file_for_results = True # Obtendremos resultados con JSON. 
format_for_results = 'hex'  # Lo hacemos porque conocemos que el formato es hex - rgb - rgba.
json_extension = '.json' # Nuestros resultados tendrán la extensión en json.
 
## Diccionario para nuestros pixels.
dictionary_for_colors = {}
## Lista de los colores ordenados.
sorted_all_colors = []

## Nuestra función.
def logic_images(args):
    ## Abrimos nuestra imagen
    global pixels_per_image
    PIL_IMAGE_FILE = Image.open(args.file)
    ## Obtenemos el tamaño y lo multiplicamos(alto por ancho).
    pixels_per_image = PIL_IMAGE_FILE.size[0] * PIL_IMAGE_FILE.size[1]
    ##Si no llegase a existir el directorio, hay que crearlo
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    ## Declaramos nuestra variable global, porque la tenemos local.
   
    ## Obtenemos la información de nuestra imagen con un loop.
    for pixels_rgba in PIL_IMAGE_FILE.getdata(): 
        if pixels_rgba[3] == 0:
            if transparent_pixels == True:
                pixels_rgba = (0, 0, 0, 0)
            else:
                pixels_per_image -= 1
                continue
        try:
            ## Asignamos en nuestro diccionario el pixel rgba junto al identificador col.
            col = dictionary_for_colors[pixels_rgba]['col']
            # Incrementamos nuestro col.
            dictionary_for_colors[pixels_rgba] = {'col': col + 1}
        
        except:
            dictionary_for_colors[pixels_rgba] = {'col':1}
     
    ## Recorremos nuestro diccionario.
    for color in dictionary_for_colors:
         ## De nuestro diccionario de los pixeles que obtuvimos, lo vamos a multiplicar y lo dividimos entre el flotanto de el total de píxeles.
        percentage_of_color = dictionary_for_colors[color]['col'] * 100 / float(pixels_per_image)
        # Ahora condicionamos, si la anterior variable es mayor o igual a nuestro porcentaje mínimo(qu es del 0.5) entonces... 
        if percentage_of_color >= porcentaje_minimo:
            # Además, condicionamos si vamos a obtener los resultavos en formato de imagen, entonces...
            if color_files_flag == True:
                # Creamos una nueva imagen, le asiganmos el modo,tamaño y los colores.
                img = Image.new('RGBA', (100, 100), (color[0],color[1],color[2],color[3]))
                # Aqi asignamos el porcentaje de color para posteriormente guardarlas.
                file_name = 'Per_Color_%03.4f.png' % percentage_of_color
                # Ahora las guardamos en nuestro directorio de salida en formato PNG.
                img.save(os.path.join(args.output,file_name),format="png")
            # Para un mayor orden, se me ocurrió ordenar los colores. Abrimos nuestra lista con los datos respectivos.
            sorted_all_colors.append({'color':color,'number':percentage_of_color})
    # Por último, ordenamos con sort.
    sorted_all_colors.sort(key=lambda k: k['number'],reverse=True)
    
    # Creamos un círculo para mostrar los resultados como en una torta de resultados. 
    circle = Image.new('RGBA', (circle_size_create,circle_size_create), (0,0,0,0))
    _current_angle = 0

    # Mediante el loop y los colores ordenados, lo recorremos...
    for x in sorted_all_colors:
        # Lo multiplicamos para expandirlo.
        _current_pieslice_angle = x['number'] * 3.6
        # Dibujamos nuestro circulo y además, lo llenamos de los colores que están en nuestra lista de colores ordenados.
        ImageDraw.Draw(circle).pieslice([10, 10, circle_size_create-10, circle_size_create-10], _current_angle, _current_angle + _current_pieslice_angle, fill=(x['color'][0],x['color'][1],x['color'][2],x['color'][3]))
        # Acumulamos.
        _current_angle += _current_pieslice_angle
     
        # Condicionamos, si vamos a obtener los resultados en .json entonces...
        if file_for_results == True:
            # Si el formato del color de resultados además es hex, entonces...
            if format_for_results == 'hex':
                x['color'] = '#%02x%02x%02x' % (x['color'][0],x['color'][1],x['color'][2])
            elif format_for_results == 'rgb':
                x['color'] = (x['color'][0],x['color'][1],x['color'][2])
    # Guardamos nuestro círculo, en donde hemos elegido guardar todo y le llamamos torta en formato png.
    circle.save(os.path.join(args.output,"torta.png"),format="png")
    
     # Condicionamos, si vamos a obtener los resultados en .json entonces... RECORDAR QUE SIEMPRE ESTÁ EN TRUE.
    if file_for_results == True:
        # Guardamos nuestro archivo de JSON en un archivo de json llamado colors.json.
        with open(os.path.join(args.output,"colors"+json_extension), 'w') as outfile:
            json.dump(sorted_all_colors, outfile)
    
    # Al finalizar todo el proceso, imprimimos, analizado.
    print("Analizado correctamente. Verificar la ruta de salida.")
#logic_images()
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output', help='Output of the colors.')
    parser.add_argument('-f','--file', help='Image to Scan colors.')
    args = parser.parse_args()
    # -f -> La imagen de la cual queremos obtener los colores.
    # -o -> Directorio para obtener los colores(se obtienen separados).
    logic_images(args)

if __name__ == '__main__':
    main()
 