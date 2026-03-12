# =========================================================================================
# 🤖 DICCIONARIO RPA: EL COPILOTO AUTÓNOMO (Versión 12 Pasos - Alta Velocidad)
# =========================================================================================

import openpyxl
import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings

logger = logging.getLogger(__name__)

class CopilotoCovicol:
    def __init__(self):
        self.driver = None
        self.libro = None
        self.hoja = None
        
        # --- 🔧 RUTAS Y CONFIGURACIÓN ---
        self.ruta_excel = os.path.join(settings.BASE_DIR, 'CP-FT-01_V3_Requisicion.xlsx')
        self.ruta_driver = "C:/Users/seleccion/Desktop/Automático/chromedriver-win64/chromedriver.exe"
        self.ruta_perfil = "C:/Users/seleccion/Desktop/Automático/Perfil_Bot"
        
        # --- 🧠 MEMORIA TEMPORAL (Datos capturados en Django) ---
        self.centro_costo = None
        self.tipo_rq = None
        self.area = None

    def iniciar_mision(self):
        """ FASE: ARRANQUE INMEDIATO (Sin Sleep) """
        try:
            # 1. Cargar Excel
            self.libro = openpyxl.load_workbook(self.ruta_excel)
            self.hoja = self.libro.active
            
            # 2. Iniciar Chrome
            opciones = Options()
            opciones.add_argument(f"--user-data-dir={self.ruta_perfil}")
            opciones.add_experimental_option("detach", True)
            
            servicio = Service(executable_path=self.ruta_driver)
            self.driver = webdriver.Chrome(service=servicio, options=opciones)
            self.driver.maximize_window()
            
            # 3. Ir a GLPI e iniciar navegación inicial (Pasos 1 al 4)
            self.driver.get("https://helpdesk.covicol.com.co/front/ticket.php")
            self.ejecutar_pasos_iniciales()
            
        except Exception as e:
            logger.error(f"🚨 ERROR EN INICIO: {str(e)}")
            raise e

    def ejecutar_pasos_iniciales(self):
        """ PASOS 1 AL 4: NAVEGACIÓN POR EL MENÚ LATERAL """
        try:
            wait = WebDriverWait(self.driver, 10) # Sensor de espera dinámica
            
            # Paso 1: Clic Menú Lateral (Span)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/a/span"))).click()
            # Paso 2: Clic Botón principal
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/div/div[1]/button"))).click()
            # Paso 3: Clic Enlace secundario
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/aside/div/div[1]/div/div[1]/div/div/div[1]/div/a[2]"))).click()
            # Paso 4: Clic Crear Nuevo (Span)
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/div[1]/div/div/div/a[2]/span"))).click()
            
            logger.info("✅ Bot posicionado en el formulario de creación.")
        except Exception as e:
            logger.error(f"❌ Error en pasos iniciales: {e}")

    def preparar_datos_basicos(self, centro_costo, tipo_rq, area):
        """ MEMORIZACIÓN: Guarda los datos de la web y marca el Excel """
        self.centro_costo = centro_costo
        self.tipo_rq = tipo_rq
        self.area = area
        
        # --- Marcación en Excel (Celda C5 y Tipo) ---
        self.hoja['C5'] = centro_costo
        if tipo_rq == 'BIEN':
            self.hoja['H3'], self.hoja['J3'] = 'X', ''
        else:
            self.hoja['J3'], self.hoja['H3'] = 'X', ''
        
        self.libro.save(self.ruta_excel)
        logger.info(f"📝 Excel preparado: {centro_costo} | {tipo_rq}")

    def carga_final_glpi(self, nombres, cantidades, unidades, titulo):
        """ PASOS 5 AL 12: EL GRAN FINAL """
        try:
            # --- 📊 FASE EXCEL: LLENAR TABLA DE ÍTEMS ---
            fila = 8
            for i, (nom, cant, uni) in enumerate(zip(nombres, cantidades, unidades), start=1):
                self.hoja.cell(row=fila, column=1, value=i)
                self.hoja.cell(row=fila, column=2, value=nom)
                self.hoja.cell(row=fila, column=5, value=uni)
                self.hoja.cell(row=fila, column=6, value=cant)
                fila += 1
            self.libro.save(self.ruta_excel)

            # --- 🌐 FASE WEB: RELLENAR FORMULARIO GLPI ---
            wait = WebDriverWait(self.driver, 10)

            # Paso 5: Tipo (Clic + Flecha Abajo + Enter)
            p5 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[1]/div/span/span[1]/span/span[1]")
            p5.click()
            self.driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

            # Paso 6: Área (Categoría) + Enter
            p6 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[2]/div/div/span[1]/span[1]/span/span[1]")
            p6.click()
            self.driver.switch_to.active_element.send_keys(self.area, Keys.ENTER)

            # Paso 7: Prioridad ALTA (Clic + Flecha Arriba + Enter)
            p7 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[3]/div/span/span[1]/span/span[1]")
            p7.click()
            self.driver.switch_to.active_element.send_keys(Keys.ARROW_UP, Keys.ENTER)

            # Paso 8: Pegar Centro de Costo
            p8 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[6]/div/div/span[1]/span[1]/span/span[1]")
            p8.click()
            self.driver.switch_to.active_element.send_keys(self.centro_costo, Keys.ENTER)

            # Paso 9: Título
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[3]/div/div[7]/div/input").send_keys(titulo)

            # Paso 10: Descripción (Iframe check)
            # Nota: Si /html/body/p no funciona, es porque hay que entrar al iframe del editor.
            try:
                self.driver.find_element(By.XPATH, "/html/body/p").send_keys(f"Requisición: {titulo}")
            except:
                # Si falla, intenta buscar el primer iframe disponible
                self.driver.switch_to.frame(0)
                self.driver.find_element(By.TAG_NAME, "body").send_keys(f"Requisición: {titulo}")
                self.driver.switch_to.default_content()

            # Paso 11: Clic en Guardar/Crear
            self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/main/div/form/div/div[4]/button/span").click()

            # Paso 12: Captura ID (5 dígitos)
            # Esperamos a que la página cargue el nuevo ticket
            id_selector = wait.until(EC.presence_of_element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/main/div/div/div/div[2]/a")))
            caso_id = id_selector.get_attribute("title")
            logger.info(f"🏆 CASO CREADO EXITOSAMENTE: #{caso_id}")
            
            return caso_id

        except Exception as e:
            logger.error(f"🚨 Error en carga final: {e}")
            raise e

    def cancelar_mision(self):
        """ ABORTO: Cierra Chrome sin guardar nada """
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("🛑 Bot: Navegador cerrado y misión cancelada.")

bot_activo = CopilotoCovicol()