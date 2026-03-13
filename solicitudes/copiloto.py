# =========================================================================================
# 🤖 DICCIONARIO RPA: EL COPILOTO AUTÓNOMO (SIFR + NOTARIO + ROBOT)
# =========================================================================================

import openpyxl # Comentario: Importamos la librería para que el Notario lea y escriba en Excel.
import os # Comentario: Importamos OS para manejar rutas de archivos en el sistema operativo.
import logging # Comentario: Sistema de bitácora para registrar qué hace el robot.
import time # Comentario: Librería para hacer pausas (dormir) y darle tiempo a la web de cargar.
from selenium import webdriver # Comentario: El motor principal del Robot para abrir el navegador.
from selenium.webdriver.chrome.service import Service # Comentario: Servicio para ejecutar ChromeDriver.
from selenium.webdriver.chrome.options import Options # Comentario: Opciones para configurar Chrome (ej: modo silencioso).
from selenium.webdriver.common.by import By # Comentario: Permite al robot buscar elementos (por XPath, ID, Clase).
from selenium.webdriver.common.keys import Keys # Comentario: Permite al robot presionar teclas (Enter, Flechas).
from selenium.webdriver.support.ui import WebDriverWait # Comentario: Sistema de espera inteligente del robot.
from selenium.webdriver.support import expected_conditions as EC # Comentario: Condiciones (ej: "espera hasta que el botón sea clickeable").
from django.conf import settings # Comentario: Traemos la configuración de Django para usar rutas dinámicas.

logger = logging.getLogger(__name__) # Comentario: Activamos el registro de eventos con el nombre del archivo actual.

class CopilotoCovicol: # Comentario: Definimos la clase principal de nuestro Robot.
    def __init__(self): # Comentario: Función de inicialización (lo que hace al nacer).
        self.driver = None # Comentario: Inicializamos el control del navegador vacío.
        self.libro = None # Comentario: Inicializamos el archivo Excel vacío para el Notario.
        self.hoja = None # Comentario: Inicializamos la pestaña de Excel vacía.
        
        # --- 🔧 RUTAS Y CONFIGURACIÓN ---
        self.ruta_excel = os.path.join(settings.BASE_DIR, 'CP-FT-01_V3_Requisicion.xlsx') # Comentario: Ruta oficial del formato Excel.
        self.ruta_driver = "C:/Users/seleccion/Desktop/Automático/chromedriver-win64/chromedriver.exe" # Comentario: Ruta del motor de Chrome.
        self.ruta_perfil = "C:/Users/seleccion/Desktop/Automático/Perfil_Bot" # Comentario: Ruta de las cookies para no loguearse siempre.
        
        # --- 🧠 MEMORIA TEMPORAL ---
        self.centro_costo = "SISTEMAS" # Comentario: Por defecto, se actualizará desde la web.
        self.area = "SISTEMAS" # Comentario: Por defecto, se actualizará desde la web.

    # =========================================================================
    # ✍️ CAPA 3: EL NOTARIO (ESCRITURA EN EXCEL)
    # =========================================================================
    def _escribir_excel(self, nombres, cantidades, unidades, observaciones): # Comentario: Función privada para firmar el Excel.
        try: # Comentario: Intentamos abrir el archivo.
            logger.info("✍️ NOTARIO: Abriendo plantilla Excel...") # Comentario: Registro en el log.
            self.libro = openpyxl.load_workbook(self.ruta_excel) # Comentario: El Notario abre el archivo físico.
            self.hoja = self.libro.active # Comentario: Selecciona la primera hoja activa.

            # Comentario: Bucle para recorrer la lista de productos que envió el SIFR.
            for i in range(len(nombres)): # Comentario: Repite el proceso por cada ítem en el carrito.
                fila = 8 + i # Comentario: Empieza en la fila 8, y baja a la 9, 10, etc.
                
                self.hoja[f'A{fila}'] = i + 1 # Comentario: Escribe el consecutivo (1, 2, 3) en la columna A.
                self.hoja[f'B{fila}'] = nombres[i] # Comentario: Escribe la Descripción en la columna B.
                self.hoja[f'E{fila}'] = unidades[i] # Comentario: Escribe la Unidad (UND, MTS) en la columna E.
                self.hoja[f'F{fila}'] = cantidades[i] # Comentario: Escribe la Cantidad en la columna F.
                
                # Comentario: Verificamos si hay una observación para este ítem.
                if i < len(observaciones) and observaciones[i]: # Comentario: Si existe y no está vacía...
                    self.hoja[f'G{fila}'] = observaciones[i] # Comentario: Escribe la Observación en la columna G.

            self.libro.save(self.ruta_excel) # Comentario: El Notario guarda los cambios.
            self.libro.close() # Comentario: El Notario cierra el archivo para no bloquearlo.
            logger.info("✅ NOTARIO: Excel firmado y guardado con éxito.") # Comentario: Éxito en el log.
            
        except Exception as e: # Comentario: Si algo falla (ej: archivo abierto por el usuario).
            logger.error(f"🚨 Error del Notario en Excel: {e}") # Comentario: Registra el error exacto.
            raise # Comentario: Detiene el proceso y avisa al sistema.

    # =========================================================================
    # 🤖 CAPA 2: EL ROBOT (NAVEGACIÓN EN GLPI)
    # =========================================================================
    def carga_final_glpi(self, nombres, cantidades, unidades, observaciones, titulo): # Comentario: Función principal orquestadora.
        # Paso A: El Notario hace su trabajo primero.
        self._escribir_excel(nombres, cantidades, unidades, observaciones) # Comentario: Llamamos a la función de escritura.

        # Paso B: Preparamos al Robot.
        opciones = Options() # Comentario: Creamos las configuraciones de Chrome.
        opciones.add_argument(f"user-data-dir={self.ruta_perfil}") # Comentario: Le damos su perfil guardado.
        servicio = Service(self.ruta_driver) # Comentario: Iniciamos el servicio del driver.
        self.driver = webdriver.Chrome(service=servicio, options=opciones) # Comentario: Abrimos la ventana del navegador.
        wait = WebDriverWait(self.driver, 15) # Comentario: Le decimos al robot que espere máximo 15 segundos por elemento.

        try: # Comentario: Inicia la misión en GLPI.
            logger.info("🤖 ROBOT: Iniciando misión en GLPI...") # Comentario: Aviso en el log.
            self.driver.get("https://helpdesk.covicol.com.co/front/ticket.php") # Comentario: Vamos directo a la base de operaciones.
            time.sleep(2) # Comentario: Pausa de 2 segundos para estabilizar la página.

            # Comentario: --- VALIDACIÓN DE LOGIN ---
            try: # Comentario: Intentamos ver si GLPI pide contraseña.
                user_input = self.driver.find_element(By.NAME, "login_name") # Comentario: Busca el campo de usuario.
                user_input.send_keys("yamit.blanco") # Comentario: Escribe las credenciales oficiales.
                pass_input = self.driver.find_element(By.NAME, "login_password") # Comentario: Busca el campo de contraseña.
                pass_input.send_keys("1121959681") # Comentario: Escribe la clave.
                self.driver.find_element(By.NAME, "submit").click() # Comentario: Hace clic en entrar.
                time.sleep(2) # Comentario: Espera a que cargue el dashboard.
            except: # Comentario: Si no encuentra el campo, es porque ya está logueado.
                logger.info("🤖 ROBOT: Sesión activa detectada. Saltando login.") # Comentario: Aviso de salto.

            # Comentario: --- EJECUCIÓN DE LOS 12 PASOS EXACTOS ---
            
            # Comentario: Paso 1 (Menú Lateral)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/a/span"))).click() # Comentario: Clic izquierdo.
            
            # Comentario: Paso 2 (Submenú)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/div/div[1]/button"))).click() # Comentario: Clic izquierdo.
            
            # Comentario: Paso 3 (Opción Tickets)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/div/div[1]/div/a[2]"))).click() # Comentario: Clic izquierdo.
            
            # Comentario: Paso 4 (Botón Crear Ticket [+])
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/div[1]/div/div/div/a[2]/span"))).click() # Comentario: Clic izquierdo.
            
            # Comentario: Paso 5 (Tipo de Ticket)
            tipo_sel = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[1]/div/span/span[1]/span/span[1]"))) # Comentario: Localiza el selector.
            tipo_sel.click() # Comentario: Abre el menú desplegable.
            time.sleep(0.5) # Comentario: Micro-pausa.
            webdriver.ActionChains(self.driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform() # Comentario: Flecha abajo y Enter.

            # Comentario: Paso 6 (Área / Categoría)
            area_sel = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[2]/div/div/span[1]/span[1]/span/span[1]"))) # Comentario: Localiza Categoría.
            area_sel.click() # Comentario: Clic izquierdo.
            time.sleep(0.5) # Comentario: Micro-pausa.
            webdriver.ActionChains(self.driver).send_keys(self.area).send_keys(Keys.ENTER).perform() # Comentario: Escribe el área y presiona Enter.

            # Comentario: Paso 7 (Urgencia)
            urgencia_sel = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[3]/div/span/span[1]/span/span[1]"))) # Comentario: Localiza Urgencia.
            urgencia_sel.click() # Comentario: Clic izquierdo.
            time.sleep(0.5) # Comentario: Micro-pausa.
            webdriver.ActionChains(self.driver).send_keys(Keys.UP).send_keys(Keys.ENTER).perform() # Comentario: Flecha arriba y Enter.

            # Comentario: Paso 8 (Centro de Costos / Ubicación)
            ubicacion_sel = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[6]/div/div/span[1]/span[1]/span/span[1]"))) # Comentario: Localiza Ubicación.
            ubicacion_sel.click() # Comentario: Clic izquierdo.
            time.sleep(0.5) # Comentario: Micro-pausa.
            webdriver.ActionChains(self.driver).send_keys(self.centro_costo).send_keys(Keys.ENTER).perform() # Comentario: Pega el centro de costo y da Enter.

            # Comentario: Paso 9 (Título del Caso)
            titulo_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[7]/div/input"))) # Comentario: Localiza el input de Título.
            titulo_oficial = f"{titulo} - {self.centro_costo}" # Comentario: Armamos el título final.
            titulo_input.send_keys(titulo_oficial) # Comentario: El robot escribe el título.

            # Comentario: Paso 10 (Descripción en TinyMCE / Iframe)
            logger.info("🤖 ROBOT: Entrando al editor de texto...") # Comentario: Aviso en log.
            self.driver.switch_to.frame(0) # Comentario: ⚡ MAGIA: El robot "entra" al primer iframe (el cuadro de texto enriquecido).
            cuerpo_texto = self.driver.find_element(By.XPATH, "/html/body/p") # Comentario: Busca la etiqueta <p> dentro del iframe.
            cuerpo_texto.send_keys(f"Requisición automática desde SIFR.\nTítulo: {titulo_oficial}\nVer Excel adjunto para detalles de ítems.") # Comentario: Escribe el resumen.
            self.driver.switch_to.default_content() # Comentario: ⚡ MAGIA: El robot "sale" del iframe para volver a la página principal.

            # Comentario: Paso 11 (Guardar / Enviar)
            btn_guardar = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[4]/button/span"))) # Comentario: Localiza el botón Guardar.
            btn_guardar.click() # Comentario: Clic izquierdo para crear el caso en GLPI.

            # Comentario: Paso 12 (Extraer ID del Caso)
            logger.info("🤖 ROBOT: Esperando confirmación de GLPI...") # Comentario: Aviso en log.
            # Comentario: Espera hasta que el enlace con el número de caso sea visible en pantalla.
            enlace_caso = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/div/div/div[2]/a"))) 
            caso_id = enlace_caso.get_attribute("title") # Comentario: Extrae el atributo 'title' que contiene los 5 dígitos.
            
            logger.info(f"🏆 MISIÓN CUMPLIDA: Ticket creado con ID {caso_id}") # Comentario: Celebra en el log.
            return caso_id # Comentario: Devuelve el número de caso al SIFR.

        except Exception as e: # Comentario: Si ocurre algún error en GLPI.
            logger.error(f"🚨 Error crítico en GLPI: {e}") # Comentario: Graba el error exacto.
            raise # Comentario: Detiene la ejecución.
        finally: # Comentario: Esto se ejecuta SIEMPRE, haya error o no.
            if self.driver: # Comentario: Si el navegador está abierto...
                self.driver.quit() # Comentario: Cierra el navegador para no consumir RAM del servidor.

# Comentario: Instanciamos el robot globalmente para que `views.py` lo pueda usar en segundo plano.
bot_activo = CopilotoCovicol()