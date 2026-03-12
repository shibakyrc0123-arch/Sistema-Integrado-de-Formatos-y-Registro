# =========================================================================
# 📍 DICCIONARIO DE RUTAS: solicitudes/urls.py (Versión Sincronizada)
# =========================================================================
from django.urls import path # Comentario: Importa la función path para mapear las URLs.
from . import views # Comentario: Importa el Cerebro (views.py) para conectar las funciones.

urlpatterns = [
    
    # Comentario: La ruta vacía ('') será la página de bienvenida (El Login).
    path('', views.login_sistema, name='login_sistema'), 
    
    # Comentario: Esta es la ruta del "Ignitor". Despierta al bot y redirige.
    path('solicitud/', views.iniciar_solicitud, name='inicio_solicitud'),

    # ⚡ LA PIEZA FALTANTE: Ruta para la vista rápida del Paso 1 (Sin bloqueo)
    # Comentario: Permite que el botón 'Volver' y el redirect funcionen al instante.
    path('solicitud/paso1/', views.mostrar_paso1, name='paso1_visual'),

    # --- 🗺️ NAVEGACIÓN DE PASOS (NUEVO ORDEN) ---
    # Comentario: Ruta para el Paso Consolidado (Área, Líder y Localización).
    path('solicitud/paso2/', views.vista_paso2, name='paso2'), 
    
    # Comentario: Ruta del Gatillo (Selección de Bien o Servicio).
    path('solicitud/paso3/', views.vista_paso3, name='paso3'), 
    
    # Comentario: Ruta para el Carrito de ítems (Punto de No Retorno).
    path('solicitud/paso5/', views.vista_paso5, name='paso5'), 
    
    # --- 🔍 BUSCADOR DINÁMICO (HTMX) ---
    # Comentario: Ruta que alimenta el buscador Fuzzy.
    path('solicitud/buscar-items/', views.buscar_items, name='buscar_items'),
    
    # Comentario: Ruta que añade el fragmento de HTML al apilado.
    path('solicitud/añadir-item-lista/<int:item_id>/', views.vista_añadir_item_lista, name='add_item_list'),
    
    # Comentario: Crear ítem nuevo desde cero dinámicamente.
    path('solicitud/crear-y-añadir/', views.crear_y_añadir, name='crear_y_añadir'),
    
    # --- 🏁 CIERRE Y ABORTO ---
    # Comentario: Cierre del proceso (Carga final en GLPI y Excel).
    path('solicitud/confirmar-final/', views.confirmar_final, name='confirmar_final'),
    
    # Comentario: El Botón Rojo para abortar la misión.
    path('solicitud/cancelar/', views.cancelar_solicitud, name='cancelar_solicitud'), 
]