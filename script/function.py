import requests
import os
from dotenv import load_dotenv

load_dotenv()


def getRequests(url):
    import requests

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def unlock(link):
    apiAgent = "agent=" + os.getenv("API_NAME")
    apiKey = "apikey=" + os.getenv("API_KEY")

    apiUrl = "https://api.alldebrid.com/v4/link/unlock?"
    response = getRequests(apiUrl + apiAgent + "&" + apiKey + "&" + link)

    if response is not None and "data" in response:
        infoData = response["data"]

        if "link" in infoData and infoData["link"] != "":
            return infoData["link"]
        else:
            idLink = infoData["id"]
            for el in infoData["streams"]:
                if "type" in el and el["type"] == "audio":
                    stream = el["id"]
            if stream is not None:
                response = streaming(apiAgent, apiKey, idLink, stream)
                if response is not None and "data" in response:
                    infoData = response["data"]
                    if "filename" in infoData and infoData["filename"] != "":
                        fileName = infoData["filename"]
                    if "link" in infoData:
                        return {
                            "filename": fileName,
                            "link": infoData["link"],
                        }
                    elif "delayed" in infoData:
                        response = delayed(apiAgent, apiKey, str(infoData["delayed"]))
                        if response is not None and "data" in response:
                            infoData = response["data"]
                            if "link" in infoData and infoData["link"] != "":
                                return {
                                    "filename": fileName,
                                    "link": infoData["link"],
                                }
                            else:
                                print("Error al obtener el link de descarga")
                    else:
                        print("No se puedo encontrar el stream")
            else:
                print("No se puedo encontrar el audio")


def streaming(apiAgent, apiKey, idLink, stream):
    apiUrl = "https://api.alldebrid.com/v4/link/streaming?"
    return getRequests(
        apiUrl + apiAgent + "&" + apiKey + "&id=" + idLink + "&stream=" + stream
    )


def delayed(apiAgent, apiKey, idDelayed):
    import time

    apiUrl = "https://api.alldebrid.com/v4/link/delayed?"
    time.sleep(5)
    return getRequests(apiUrl + apiAgent + "&" + apiKey + "&id=" + idDelayed)


def saveMp3(url, path):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(path, "wb") as archivo:
                archivo.write(response.content)
            # print("Descarga completada con éxito.")
        else:
            print(
                f"Error al descargar el archivo. Código de estado: {response.status_code}"
            )

    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
