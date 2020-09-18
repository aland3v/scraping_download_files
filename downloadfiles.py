import os
import requests
import urllib.request
from bs4 import BeautifulSoup
resultado = []

url = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

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


def main():
  page = conecta()
  soup = BeautifulSoup(page.content,'html.parser')
  url_files = soup.find_all('a',class_='ptb_link_button')

  print("***Primera pagina: "+str(lista_imgs.__len__())+"***")
  for img in lista_imgs:
    imgUrl = img["src"]
    img_name = "images/"+os.path.basename(imgUrl)
    if(not os.path.isfile(img_name)):      
      sw = True
      while sw:
        try:
          urllib.request.urlretrieve(imgUrl,img_name)
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
    else:
      print("La imagen: "+img_name+" -> ya esta descargada!!!")

main()