# MIT License
#
# Copyright (c) 2026 Cassie Cass
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sublime
import sublime_plugin
import re
import urllib.request
import json
import os


# Comando principal del plugin para descargar archivos JSON.
class LocalJnCommand(sublime_plugin.TextCommand):

    # Método principal ejecutado cuando se invoca el comando.
    def run(self, edit):

        # Obtener el texto de la línea donde se encuentra el cursor.
        linea = obtenerLaLineaDondeEstaElCursor(self.view)

        # Comprobar si la línea contiene una URL HTTP o HTTPS.
        if not existeUnaUrlConHttp(linea):
            sublime.status_message("Aviso: No existe una URL en esta línea: " + linea)
            return

        # Extraer la URL encontrada dentro de la línea.
        url = obtenerUrlDeLaLinea(linea)

        # Comprobar que se haya podido extraer correctamente la URL.
        if not url:
            sublime.status_message("Aviso: No se pudo extraer la URL")
            return

        # Obtener la ruta raíz del proyecto abierto en Sublime Text.
        ruta_raiz = obtenerRutaRaizDelProyecto(self.view)

        # Comprobar que exista una ruta raíz del proyecto.
        if not ruta_raiz:
            sublime.status_message("Aviso: No se pudo obtener la ruta raíz del proyecto")
            return

        # Ejecutar la descarga en segundo plano para no bloquear
        # la interfaz de Sublime Text.
        sublime.set_timeout_async(
            lambda: self.procesar_descarga(url, ruta_raiz),
            0
        )

    # Gestionar la petición HTTP, procesar el JSON y guardar el archivo.
    def procesar_descarga(self, url, ruta_raiz):

        try:

            # Crear una petición HTTP incluyendo un User-Agent
            # para mejorar la compatibilidad con diferentes servidores.
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            # Realizar la petición HTTP con un tiempo máximo de espera
            # de 10 segundos.
            with urllib.request.urlopen(req, timeout=10) as respuesta:

                # Leer el contenido de la respuesta y decodificarlo
                # utilizando UTF-8.
                contenido = respuesta.read().decode("utf-8")

                # Convertir el contenido recibido en un objeto Python.
                datos = json.loads(contenido)

            # Formatear el JSON para facilitar su lectura.
            # indent=4 aplica una indentación de cuatro espacios.
            # ensure_ascii=False permite conservar caracteres especiales.
            texto_formateado = json.dumps(
                datos,
                indent=4,
                ensure_ascii=False
            )

            # Construir la ruta de la carpeta donde se guardarán
            # los archivos JSON descargados.
            ruta_carpeta = os.path.join(ruta_raiz, "descargas_json")

            # Crear la carpeta si todavía no existe.
            os.makedirs(ruta_carpeta, exist_ok=True)

            # Inicializar el contador para generar nombres únicos.
            contador = 0

            # Buscar un nombre de archivo que todavía no exista.
            while True:

                # La primera descarga utilizará resultado.json.
                if contador == 0:
                    nombre_archivo = "resultado.json"

                # Las siguientes descargas utilizarán un número consecutivo.
                else:
                    nombre_archivo = "resultado_" + str(contador) + ".json"

                # Construir la ruta completa del archivo.
                ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

                try:

                    # Crear el archivo exclusivamente si no existe.
                    # El modo "x" evita sobrescribir archivos anteriores.
                    with open(ruta_archivo, "x", encoding="utf-8") as archivo:

                        # Escribir el contenido JSON formateado en el archivo.
                        archivo.write(texto_formateado)

                    # Salir del bucle cuando el archivo se haya creado.
                    break

                # Si el archivo ya existe, incrementar el contador
                # y volver a intentar con otro nombre.
                except FileExistsError:
                    contador += 1

            # Abrir el archivo descargado en Sublime Text.
            # Se utiliza set_timeout para ejecutar la operación
            # desde el hilo principal de la interfaz.
            sublime.set_timeout(
                lambda: self.abrir_en_pestana(ruta_archivo),
                0
            )

        # Capturar cualquier error producido durante la descarga,
        # la conversión del JSON o la escritura del archivo.
        except Exception as e:

            # Convertir el error en una cadena de texto.
            error = str(e)

            # Mostrar el mensaje de error en la interfaz de Sublime Text.
            sublime.set_timeout(
                lambda: sublime.error_message("Error al descargar:\n" + error),
                0
            )

    # Abrir el archivo JSON descargado en una nueva pestaña.
    def abrir_en_pestana(self, ruta_archivo):

        # Obtener la ventana actual de Sublime Text.
        window = self.view.window()

        # Comprobar que la ventana siga disponible.
        if window:

            # Abrir el archivo utilizando su ruta completa.
            window.open_file(ruta_archivo)


# Obtener el texto completo de la línea donde está situado el cursor.
def obtenerLaLineaDondeEstaElCursor(view):

    # Obtener la región correspondiente a la línea actual.
    region = view.line(view.sel()[0].begin())

    # Extraer el texto contenido en dicha región.
    texto = view.substr(region)

    # Devolver el texto de la línea.
    return texto


# Comprobar si una línea contiene una dirección HTTP o HTTPS.
def existeUnaUrlConHttp(linea):

    # Buscar los protocolos HTTP y HTTPS dentro de la línea.
    if "https://" in linea or "http://" in linea:
        return True

    # Devolver False si no se encuentra ninguno de los protocolos.
    return False


# Extraer la primera URL HTTP o HTTPS encontrada en una línea.
def obtenerUrlDeLaLinea(linea):

    # Expresión regular que identifica URLs HTTP y HTTPS.
    # Evita capturar espacios, comillas y paréntesis.
    patron = r'https?://[^\s"\'()]+'

    # Buscar la primera coincidencia dentro de la línea.
    coincidencia = re.search(patron, linea)

    # Si existe una coincidencia, devolver la URL encontrada.
    if coincidencia:
        return coincidencia.group(0)

    # Devolver False cuando no se encuentre ninguna URL.
    return False


# Obtener la ruta raíz del proyecto abierto en Sublime Text.
def obtenerRutaRaizDelProyecto(view):

    # Recuperar todas las carpetas configuradas en el proyecto actual.
    carpetas_proyecto = view.window().folders()

    # Obtener la primera carpeta del proyecto.
    # Si no existe ninguna carpeta, devolver None.
    ruta_raiz = next(iter(carpetas_proyecto), None)

    # Devolver la ruta raíz obtenida.
    return ruta_raiz