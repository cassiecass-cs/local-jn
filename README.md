# local-jn
Plugin de Sublime Text para descargar, formatear y guardar archivos JSON desde una URL en el proyecto local.
# local-jn

Plugin para **Sublime Text** que descarga archivos JSON desde una URL ubicada en la línea actual del editor, los formatea automáticamente y los guarda en tu proyecto local sin bloquear la interfaz.

## ✨ Características

*   Detecta automáticamente la primera URL (`http://` o `https://`) en la línea donde está el cursor.
*   Descarga el JSON en segundo plano (de forma asíncrona).
*   Formatea el contenido con indentación de 4 espacios y soporte para caracteres especiales (`UTF-8`).
*   Guarda el archivo en la carpeta `descargas_json/` dentro de la raíz de tu proyecto abierto (`resultado.json`, `resultado_1.json`, etc.) sin sobrescribir archivos existentes.
*   Abre el archivo recién descargado en una nueva pestaña.

---

## 📦 Instalación con Package Control (`Add Repository`)

Puedes instalar este plugin directamente en Sublime Text siguiendo estos pasos:

1.  Abre la paleta de comandos en Sublime Text:
    *   **Windows / Linux:** `Ctrl + Shift + P`
    *   **macOS:** `Cmd + Shift + P`
2.  Escribe **`Package Control: Add Repository`** y presiona `Enter`.
3.  Pega la URL de este repositorio en el campo inferior y presiona `Enter`:
    ```text
    [https://github.com/TU-USUARIO/local-jn](https://github.com/TU-USUARIO/local-jn)
    ```
4.  Abre nuevamente la paleta de comandos (`Ctrl + Shift + P` o `Cmd + Shift + P`).
5.  Escribe **`Package Control: Install Package`** y presiona `Enter`.
6.  Busca **`local-jn`** en la lista y selecciónalo para completar la instalación.

---

## 🚀 Cómo utilizarlo

> **Nota:** Asegúrate de tener una carpeta o proyecto abierto en Sublime Text (`File > Open Folder...`), ya que el plugin guarda las descargas en la raíz de dicho proyecto.

1.  Coloca el cursor sobre cualquier línea que contenga una URL que devuelva un JSON válido, por ejemplo:
    ```text
    [https://jsonplaceholder.typicode.com/todos/1](https://jsonplaceholder.typicode.com/todos/1)
    ```
2.  Ejecuta el comando **`local_jn`**.

### Formas de llamar al comando `local_jn`

#### Opción 1: Desde la consola de Sublime Text
1.  Abre la consola con `` Ctrl + ` `` (o `View > Show Console`).
2.  Ejecuta:
    ```python
    view.run_command("local_jn")
    ```

#### Opción 2: Con un atajo de teclado personalizado (Recomendado)
1.  Ve a **`Preferences > Key Bindings`**.
2.  Agrega la siguiente regla dentro de los corchetes `[]` de la derecha:
    ```json
    {
        "keys": ["ctrl+alt+j"],
        "command": "local_jn"
    }
    ```
3.  Guarda el archivo y presiona `Ctrl + Alt + J` cada vez que quieras descargar el JSON de una línea.

---

## 📁 Estructura de salida

Al ejecutar el comando, se creará automáticamente la siguiente estructura dentro de tu proyecto:

```text
tu-proyecto/
└── descargas_json/
    ├── resultado.json
    ├── resultado_1.json
    └── ...
