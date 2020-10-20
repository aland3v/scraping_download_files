import os
import time
import requests
from bs4 import BeautifulSoup
resultado = []

# Pagina de donde se va a descargar
url = "pon aqui la url"

# Es necesario especificar la cabezara para que el servidor no rechace nuestra conexion
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

# Hace la conexion y descarga la pagina en html, return 'page'
def conecta():
  sw = True
  while sw:
    try:
      page = requests.get(url,headers=headers)
      sw = False      
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Timeout -> Reintentando")        
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Muchas redireccionles -> Reintentando")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)
  return page

#Inicio del programa
def main():
  print("Obteniendo la pagina")
  page = conecta() # obtiene la pagina
  soup = BeautifulSoup(page.content,'html.parser')
  
  print("Obteniendo tags que cumplen la condición")
  url_files = soup.find_all('tag que contienela url',class_='clase que identifica al tag')

  print("Obteniendo las Urls absolutas")
  for item in url_files:
    if("https://" not in item["href"]): # Hay URLs relativas y absolutas
      file_url = "pon aka el dominio si la url es relativa" + item["href"]
    else:
      file_url = item["href"]
    
    print("Url encontrada: {0}".format(file_url))
    
    # path donde se almacenará
    file_name = "files/"+os.path.basename(file_url) 

    # Verifica si el archivo ya esta descargado, sino entonces descarga
    if(not os.path.isfile(file_name)):
      sw = True
      while sw:
        try:
          # Si no ponemos esto habra errores de sincronismo con el servidor
          # y por tanto no se descargaran todos los files
          time.sleep(0.01)
          
          # Inicia la descarga, indicamos los headers correspondientes
          print("Descargando fichero: {0}".format(file_url))
          r = requests.get(file_url, headers=headers)
          with open(file_name, 'wb') as f:
              f.write(r.content)

          # Retrieve HTTP meta-data
          print("METADATA")
          print("Status code: {0}".format(r.status_code))
          print("Content-type: {0}".format(r.headers['content-type']))
          print("Encoding: {0}".format(r.encoding))

          sw = False
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print("Timeout -> Reintentando")        
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print("Muchas redireccionles -> Reintentando")
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print("Oops hubo un error en Solicitud: ")
            raise SystemExit(e)
    else:
      print("El archivo: "+file_url+" ya esta descargado!!!")

main()