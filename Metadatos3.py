import os #Funcinalidades del Sistema operativo
import subprocess #Linea de comandos
from PIL import Image as PImage #Librería Pillow para extraer metadatos
from PIL.ExifTags import TAGS
from pyexiv2 import Image #Libreria pyexiv2 para extraer metadatos

def downloadImages():
    # Pregunta al usuario por el query a buscar
    data = input('¿Qué estás buscando? ')
    print('Empieza la busqueda...')

    #Busca  el termino mediante un comando por la linea de comandos y descarga las 100 imagenes
    subprocess.run('image_search bing '+data+' --limit 100 --json') 
    #Esta librería también serviría para google si no fuese porque recientemente este buscador modifico la estructura de la busqueda.
    #El archivo json incluye los metadatos del archivo. 

    print('\n Descarga finalizada. Verifique el directorio \dataset\bing\\'+data+' para ver las imagenes \n')

    return data

def readImage(data):
    print('\n Escaneando el directorio ' + r'.\dataset\bing\\' + data + ' para extraer los metadatos \n')

    #Recorre los archivos en el directorio, y guarda en una variable de tipo String el directrio a ser abierto para la extracción de los metadatos.
    walk = os.walk(r'.\dataset\bing\\' + data)
    for root, dirs, files in walk:
        for name in files:
            #print(os.path.join(root, name))
            if root[-1:] == "/": 
                file_full_path = root+name
            else: 
                file_full_path = root+os.path.sep+name
            if file_full_path[-4:]!='json':
                try:
                    img = PImage.open(file_full_path) #Intenta obtener los metadatos
                    readMetadata(file_full_path) #Envia el string como parametro al metodo de extracción
                except: #En caso de excepción
                    print('\n' + file_full_path + ' no es una imagen válida \n')


def readMetadata(image):
    print("Resultados para "+image+ ' \n ') #indica en consola los metadatos
    file=open("metadatos.html","a") #Crea el archivo donde se exportan los metadatos, y dado el caso que ya exista, lo abre con el puntero en la ultima línea
    file.write(' \n Resultados para' + image + ' \n ') #Escribe en el archivo
    try:
        for (k,v) in PImage.open(image)._getexif().items(): #Por cada metadato extraido de la imagen
            print('%s = %s ' % (TAGS.get(k), v)) #Imprime en pantalla
            file.write('\n')
            file.write('\n %s = %s ' % (TAGS.get(k), v)) #Escribe en el archivo
            file.write('\n') #Salto de linea en el archivo

        with Image(image) as img: #Otros metadatos imprimidos en consola
            data=img.read_exif()
            data2=img.read_iptc()
            data3=img.read_raw_xmp()

        
        if data:
            print("Metadatos Exif")
            file.write(" \n Metadatos Exif \n ")
            file.write(' \n ')
            for key, value in data.items():
                print (key, ":", value)
                file.write(key, ":", value)
                file.write('\n')
        if data2:
            print("Metadatos IPTC")
            file.write("\n Metadatos IPTC \n")
            file.write('\n')
            for key, value in data2.items():
                print (key, ":", value)
                file.write(key, ":", value)
                file.write('\n')
       
        if data3:
            print("Metadatos RAW XMP")
            file.write("\n Metadatos RAW XMP \n ")
            file.write('\n')
            for key, value in data3.items():
                print (key, ":", value)
                file.write(key, ":", value)
                file.write('\n')
        
    except:
        print ("Metadata no encontrada! \n ")
        file.write(" \n Metadata no encontrada \n ")
    file.write('\n')
    file.write('\n')
    file.close()


if __name__ == '__main__':
    data=downloadImages()
    readImage(data)
    print('\n Proceso finalizado. Verifique el archivo Metadatos.html para obtener la impresión de los metadatos \n')

