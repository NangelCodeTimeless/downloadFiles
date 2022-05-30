import requests
import subprocess
import socket
import os
from tqdm import tqdm
import pyfiglet
import sys
import youtube_dl


class Download:

    @classmethod
    def opt_videos(cls, url_video):
        list_formats = None
        try:
            d_video = youtube_dl.YoutubeDL({})
            meta = d_video.extract_info(url_video, download=False)
            seg = int(meta['duration']) % 60
            mints = int(meta['duration']) // 60
            codigo_text = "CODIGO"
            ext_text = "EXTENSION"
            reso_text = "RESOLUCION"
            size_text = "SIZE(MB)"

            print(f"""
              {meta['title']}   
              Tiempo de duracion: {mints} min : {seg}
            """)
            list_formats = meta.get('formats')
            print(
                f"|{codigo_text.center(9)} | {ext_text.center(10)} | {reso_text.center(28)} | {size_text.center(16)}|")
            for formats in list_formats:
                # sizeMB = int(formats['filesize']) / 1000000
                reso = formats['format'].split('-')[-1]
                print(f"|{formats['format_id'].center(10)}|"
                      f"{formats['ext'].center(12)}|"
                      f"{str(reso).center(30)}|")
                # f"{formats['filesize'].center(17)}|")
        except youtube_dl.utils.DownloadError:
            print("Error no ingreso correctamente un URL")
        return list_formats

    @classmethod
    def msg_download(cls):
        if ['status'] == 'finished':
            print('Done downloading')

    @classmethod
    def check_code_video(cls, code_video, list_videos):
        l_videos = list_videos
        for code in l_videos:
            if code_video == code['format_id']:
                return True
        return False

    @classmethod
    def download_video(cls, url_video):

        list_formats_video = cls.opt_videos(url_video)
        if list_formats_video is not None:
            opt_code = input('ENTER CODE OF VIDEO:').strip()
            if cls.check_code_video(opt_code, list_formats_video):
                opt = {'format': f'{opt_code}', }
                video = youtube_dl.YoutubeDL(opt)
                video.download([url_video])
            else:
                print("ingrese un codigo correcto")

    @classmethod
    def download_files(cls, url_file):

        if cls.check_internet() == 1:
            response = None
            output_file = None
            process = None
            try:
                '''ENVIAR UNA SOLICITUD con l metodo get ALA url_file definida por e usuario'''
                response = requests.get(url_file, stream=True)
                type_file = response.headers.get('text/html')
                path_user = os.environ.get("USERPROFILE")
                path_download = path_user + "\\Downloads\\Documents"
                file_name = str(response.url).split('/')[-1]

                if response.status_code == 200:
                    if not os.path.isfile(f"{path_download}\\{file_name}"):
                        if not type_file:
                            if os.path.exists(path_download):
                                output_file = open(path_download + f"\\{file_name}", mode="wb")
                                size = int(response.headers.get('Content-Length'))
                                progress_bar = tqdm(response.iter_content(chunk_size=1024), total=(size / 1024))
                                for byte in progress_bar:
                                    progress_bar.set_description("Download FILE:")
                                    output_file.write(byte)
                                process = subprocess.Popen(f"explorer /select, {path_download}\\{file_name}")
                                print("La descarga fue exitosa...")
                            else:
                                print(f" NO SE PUEDE ENCONTRAR LA RUTA: {path_download}")
                        else:
                            print(f"El archivo es una pagina web")
                    else:
                        print(f"El archivo existe")
                        response.close()
                else:
                    raise requests.ConnectionError("fail of connection..")
            except requests.ConnectionError:
                print("fail of connection..")
            except requests.URLRequired:
                print("Ingrese correctamente la URL")
            except TypeError:
                print("Error en descargar el archivo: el tamaño del archivo es invalido...")
            except requests.exceptions.MissingSchema:
                print("El Esquema de la URL es invalido..")
            except requests.exceptions.InvalidSchema:
                print("Error")
            finally:
                if response is not None:
                    response.close()
                if output_file is not None:
                    output_file.close()
                if process is not None:
                    if process.returncode is not None:
                        process.kill()
        else:
            print("No hay Conexion a Internet...")

    @classmethod
    def check_internet(cls):
        """Verifica la conexion a internet"""
        try:
            objSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            objSocket.connect(("www.google.com", 80))
            objSocket.close()
            return 1
        except socket.error:
            return 0

    def __del__(self):
        print("El objeto Download se esta borrado de la memoria...")


def menu():
    res = pyfiglet.figlet_format("DOWNLOAD FILE")
    print(f"""
               {res} 
              -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-
               |_                                 |
               |_ [1] Download videos             |
               |_ [2] Download files              |
               |_ [3] Exit                        |  
               |__________________________________|
    """)


def principal():
    menu()
    number = input("ENTER NUMBER:").strip()
    digit = number.isdigit()
    if digit:
        while int(number) < 1 or int(number) > 3:
            menu()
            number = input("ENTER NUMBER:")
    return number


if __name__ == "__main__":
    try:
        num_op_ele = int(principal())
        if num_op_ele == 1:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            url = input("ENTER URL OF VIDEO:")
            if len(url) == 0:
                print("No ha ingresdo URL")
            else:
                print("_________________________________________________________________________")
                url_clean = url.strip()
                Download.download_video(url_clean)
                print("_________________________________________________________________________")
        elif num_op_ele == 2:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            url = input("ENTER URL:")
            if len(url) == 0:
                print("No ha ingresdo URL")
            else:
                print("_________________________________________________________________________")
                url_clean = url.strip()
                Download.download_files(url_clean)
                print("_________________________________________________________________________")
                principal()
        elif num_op_ele == 3:
            sys.exit()
        else:
            pass
    except TypeError:
        print("ERROR DE CONVERSION DE LA VARIABLE DE ENTRADA...")
