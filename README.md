1. Instalar el Subsistema de Windows para Linux (WSL)

Si no lo tienes instalado, abre el PowerShell o la Símbolo del sistema de Windows como administrador y ejecuta el siguiente comando:

wsl --install

Reinicia el ordenador cuando se te solicite.
2. Abrir la terminal de WSL

Abre la aplicación de WSL o la terminal de Windows y selecciona tu distribución de Linux (por ejemplo, Ubuntu).

Navega a la carpeta donde quieras guardar el proyecto y clona el repositorio de Git.

cd /mnt/c/Users/TuUsuario/Documents
git clone https://github.com/tu_usuario/tu_repositorio.git

Ahora, entra en la carpeta del proyecto que acabas de clonar.

cd tu_repositorio

3. Navegar a la carpeta del proyecto

Usa el comando cd para navegar hasta la carpeta donde se encuentra tu proyecto. Por ejemplo:

cd /mnt/c/Users/TuUsuario/NombreDeTuProyecto
4. Instalar las librerías de Python

Primero, asegúrate de que tienes pip y venv instalados.

sudo apt update
sudo apt install python3-pip python3-venv

Ahora, instala las librerías necesarias para el proyecto. Para hacerlo, utiliza el archivo requirements.txt 

pip install -r requirements.txt

5. Crear e iniciar el entorno virtual

Es una buena práctica crear un entorno virtual para aislar las dependencias del proyecto. Esto evita conflictos con otras aplicaciones de Python.

python3 -m venv .venv

Activa el entorno virtual:

source .venv/bin/activate

Cuando el entorno esté activo, verás (.venv) al inicio de la línea de comandos.

6. Entrar en la carpeta 'src' y ejecutar la aplicación

Navega hasta la carpeta donde se encuentra tu archivo ui.py y ejecuta el comando de Streamlit.

En mi caso "cd ~/PROYECTOS/TFM/src/"

streamlit run ui.py

¡Listo! La aplicación se iniciará en tu navegador web.

https://youtu.be/jhp-T7gRaJo




