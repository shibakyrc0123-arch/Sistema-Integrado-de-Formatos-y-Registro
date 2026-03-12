# =========================================================================
# 🐍 DICCIONARIO DE VISTAS: solicitudes/views.py (Versión de Alto Rendimiento)
# =========================================================================
from django.shortcuts import render, redirect # Comentario: Herramientas para mostrar páginas y redirigir URLs.
from .models import DiccionarioItems # Comentario: Modelo de la base de datos de productos.
from django.db.models import Q # Comentario: Permite hacer búsquedas complejas en la DB.
from thefuzz import process # Comentario: Librería para lógica difusa (errores de ortografía).
import logging # Comentario: Sistema de registro de eventos (logs).
import os # Comentario: Manejo de carpetas y rutas del sistema.
import threading # Comentario: ⚡ CLAVE: Ejecuta el bot en paralelo para no congelar la web.
from .copiloto import bot_activo # Comentario: Importamos la instancia del Robot RPA.
from django.contrib.auth import authenticate, login # Comentario: Manejo de seguridad y sesiones de usuario.
from django.http import HttpResponse # Comentario: Respuesta básica de texto para errores o HTMX.

# --- CONFIGURACIÓN DE AUDITORÍA (DEBUGGING) ---
if not os.path.exists('logs_covicol'): # Comentario: Si no existe la carpeta de logs, la crea.
    os.makedirs('logs_covicol')

logging.basicConfig( # Comentario: Define dónde y cómo se grabarán los logs.
    filename='logs_covicol/sistema_vibras.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__) # Comentario: Inicializa el grabador de este archivo.

# =========================================================================
# 🧠 EL CEREBRO RELACIONAL
# =========================================================================
ESTRUCTURA_AREAS = { # Comentario: Diccionario maestro que vincula Áreas con sus Líderes.
    "SISTEMAS": {
        "lider": "HARDY DAVID POLO CASTRO",
        "cargo": "INGENIERO DE SISTEMAS"
    },
}

# =========================================================================
# 🚪 FLUJO DE AUTENTICACIÓN Y DESPEGUE (Optimizado)
# =========================================================================

def login_sistema(request): # Comentario: Gestiona el acceso inicial.
    if request.method == 'POST': # Comentario: Si el usuario envía el formulario de login.
        user = request.POST.get('username') # Comentario: Atrapa el nombre digitado.
        passw = request.POST.get('password') # Comentario: Atrapa la clave digitada.
        usuario_valido = authenticate(request, username=user, password=passw) # Comentario: Valida en DB.
        if usuario_valido: # Comentario: Si las credenciales coinciden.
            login(request, usuario_valido) # Comentario: Crea la sesión del usuario.
            logger.info(f"👤 Usuario {user} ingresó al sistema.") # Comentario: Anota en el log.
            return redirect('inicio_solicitud') # Comentario: Salta al disparador del bot.
        else: # Comentario: Si los datos son erróneos.
            return render(request, 'solicitudes/bienvenida.html', {'error': 'Credenciales inválidas'})
    return render(request, 'solicitudes/bienvenida.html') # Comentario: Muestra el login por defecto.

def iniciar_solicitud(request): # Comentario: EL IGNITOR. Lanza el bot y sigue adelante.
    # Comentario: Ejecutamos el arranque de Chrome en un hilo (Thread) para que la web no cargue 30s.
    hilo_bot = threading.Thread(target=bot_activo.iniciar_mision, daemon=True)
    hilo_bot.start() 
    
    logger.info("🤖 Hilo del bot lanzado. El usuario entra sin esperas.")
    return redirect('paso1_visual') # Comentario: Redirige a la vista rápida del Paso 1.

def mostrar_paso1(request): # Comentario: Renderiza el formulario inicial de formato.
    return render(request, 'solicitudes/formulario_step.html')

# =========================================================================
# 🛋️ PASOS INTERMEDIOS (UX Consolidada)
# =========================================================================

def vista_paso2(request): # Comentario: Procesa la elección de sede y área.
    if request.method == 'POST': # Comentario: Si viene del Paso 1.
        request.session['formato'] = request.POST.get('formato') # Comentario: Guarda el formato en sesión.
    
    localizaciones = [ # Comentario: Lista de sedes para el buscador del Paso 2.
        "OFICINA CENTRAL", "OBRA NORTE", "PROYECTO ESPECIAL", "MANTENIMIENTO", "PTAP"
    ]
    
    contexto = { # Comentario: Datos que viajan a la pantalla del Paso 2.
        'areas_data': ESTRUCTURA_AREAS, 
        'localizaciones': localizaciones
    }
    return render(request, 'solicitudes/pasos/paso2.html', contexto)

def vista_paso3(request): # Comentario: Recibe área/sede y muestra Bien/Servicio.
    if request.method == 'POST': # Comentario: Si el usuario dio clic en "Continuar" en el Paso 2.
        # Comentario: Atrapamos y guardamos todo en la memoria de Django (Sesión).
        request.session['area'] = request.POST.get('area')
        request.session['lider'] = request.POST.get('lider')
        request.session['cargo'] = request.POST.get('cargo')
        request.session['centro_costo'] = request.POST.get('localizacion')
    
    # Comentario: Enviamos tanto Sede como Área al contexto para el resumen superior.
    contexto = {
        'resumen_centro': request.session.get('centro_costo'),
        'resumen_area': request.session.get('area')
    }
    return render(request, 'solicitudes/pasos/paso3.html', contexto)

def vista_paso5(request): # Comentario: Salto al buscador de ítems.
    if request.method == 'POST': # Comentario: Captura el Tipo (Bien/Servicio) del Paso 3.
        tipo_rq = request.POST.get('tipo_rq') 
        request.session['tipo_rq'] = tipo_rq
        
        # ⚡ CAMBIO MÍNIMO E INDISPENSABLE: Blindaje de Sincronización.
        cc = request.session.get('centro_costo')
        area = request.session.get('area')
        
        try:
            # Comentario: Intentamos sincronizar con el bot. 
            # Si el bot aún no está listo, el 'try' evita que la web se bloquee.
            bot_activo.preparar_datos_basicos(cc, tipo_rq, area)
            logger.info(f"🚀 Bot sincronizado con CC: {cc}")
        except Exception as e:
            # Comentario: Si falla (porque el Excel aún carga o está abierto), lo registramos pero seguimos.
            logger.warning(f"⚠️ El bot no pudo marcar el Excel todavía: {e}")

    # Comentario: Contexto completo para el resumen azul del Paso 5.
    contexto = { 
        'resumen_centro': request.session.get('centro_costo'),
        'resumen_area': request.session.get('area'), 
        'resumen_tipo': request.session.get('tipo_rq')
    }
    return render(request, 'solicitudes/pasos/paso5.html', contexto)

# =========================================================================
# 🔍 MOTORES DINÁMICOS (Buscador HTMX)
# =========================================================================

def buscar_items(request): # Comentario: Buscador inteligente con lógica Fuzzy.
    query = request.GET.get('q', '').strip().upper() # Comentario: Limpia y normaliza el texto.
    if len(query) > 2: # Comentario: Solo busca si el usuario escribió más de 2 letras.
        exactos = DiccionarioItems.objects.filter(descripcion__icontains=query)[:5]
        todos = DiccionarioItems.objects.all()
        choices = {i.id: i.descripcion for i in todos}
        fuzzy_results = process.extract(query, choices, limit=5)
        ids_fuzzy = [res[2] for res in fuzzy_results if res[1] > 65]
        resultados = (exactos | DiccionarioItems.objects.filter(id__in=ids_fuzzy)).distinct()
    else:
        resultados = []
    return render(request, 'solicitudes/pasos/resultados_busqueda.html', {'resultados': resultados, 'query': query})

def vista_añadir_item_lista(request, item_id): # Comentario: Retorna una fila HTML.
    try:
        item = DiccionarioItems.objects.get(id=item_id)
        return render(request, 'solicitudes/pasos/item_fila.html', {'item': item})
    except DiccionarioItems.DoesNotExist:
        return HttpResponse("No existe el ítem.", status=404)

def crear_y_añadir(request): # Comentario: Registra un producto nuevo.
    if request.method == 'POST':
        nombre = request.POST.get('nuevo_nombre').upper() 
        unidad = request.POST.get('nueva_unidad', 'UND') 
        item, _ = DiccionarioItems.objects.get_or_create(descripcion=nombre, defaults={'unidad_medida': unidad})
        logger.info(f"✨ Ítem Creado: '{nombre}'")
        return render(request, 'solicitudes/pasos/item_fila.html', {'item': item})

# =========================================================================
# 🏁 CIERRE Y CANCELACIÓN
# =========================================================================

def confirmar_final(request): # Comentario: Carga final en GLPI y Excel.
    if request.method == 'POST':
        nombres = request.POST.getlist('nombres_items[]')
        cantidades = request.POST.getlist('cantidades[]')
        unidades = request.POST.getlist('unidades[]')
        titulo = request.session.get('formato')

        try:
            bot_activo.carga_final_glpi(nombres, cantidades, unidades, titulo)
            logger.info(f"✅ ÉXITO FINAL: Caso generado.")
            return render(request, 'solicitudes/pasos/exito_final.html')
        except Exception as e:
            logger.error(f"🚨 Fallo en carga final: {e}")
            return HttpResponse(f"Error técnico en el robot: {e}", status=500)

def cancelar_solicitud(request): # Comentario: Aborto y limpieza.
    bot_activo.cancelar_mision()
    request.session.flush()
    logger.info("🛑 Misión cancelada.")
    return redirect('login_sistema')