# =========================================================================
# 🗄️ DICCIONARIO DE MODELOS: ESTRUCTURA DE LA BASE DE DATOS
# =========================================================================

# Comentario: Importamos el módulo de base de datos de Django.
from django.db import models

# Comentario: Creamos la tabla principal para las solicitudes de compras.
class RequisicionInterna(models.Model): 
    
    # Comentario: Tupla de opciones para los Centros de Costos de Covicol.
    CENTROS_COSTO = [
        ('ACUEDUCTO VISTA HERMOSA', 'Acueducto Vista Hermosa'), # Comentario: Formato (Valor interno, Valor mostrado)
        ('CLUB LLANEROS', 'Club Llaneros'), 
        ('COVICOL OFICINA ESPERANZA', 'Covicol Oficina Esperanza'),
        ('COVICOL OFICINA MOLINO', 'Covicol Oficina Molino'), 
        ('COVICOL OFICINA PRIMAVERA', 'Covicol Oficina Primavera'),
        ('FINCA LA SARITA', 'Finca La Sarita'),
        ('IE RUBIALES', 'IE Rubiales'),
        ('IMAGENES DIAGNOSTICAS HDG', 'Imágenes Diagnósticas HDG'),
        ('IMÁGENES VITAL HDV', 'Imágenes Vital HDV'),
        ('MANTENIMIENTO BIOMEDICO', 'Mantenimiento Biomédico'),
        ('MANTENIMIENTO HOSPITALARIO HDV', 'Mantenimiento Hospitalario HDV'),
        ('OBRA CLINICA VITAL GRANADA', 'Obra Clínica Vital Granada'),
        ('OBRA UNILLANOS', 'Obra Unillanos'),
        ('OBRA LLANEROS', 'Obra Llaneros'),
        ('OBRA PRIMAVERA', 'Obra Primavera'),
        ('OFICINA COVICOL HDG', 'Oficina Covicol HDG'),
        ('PARQUES VILLAVICENCIO', 'Parques Villavicencio'),
        ('PTAP', 'PTAP'),
        ('SUB ESTACION ELECTRICA', 'Sub Estación Eléctrica'),
        ('ADECUACIONES HDG', 'Adecuaciones HDG')
    ]

    # Comentario: Opciones para elegir si se pide un Bien o un Servicio.
    TIPO_OPCIONES = [
        ('BIEN', 'Bien'), # Comentario: Bien físico (ej. UPS, Cámaras).
        ('SERVICIO', 'Servicio') # Comentario: Servicio (ej. Instalación, Fusiones).
    ]
    
    # Comentario: Opciones de urgencia del caso para GLPI.
    PRIORIDAD_OPCIONES = [
        ('BAJA', 'Baja'), 
        ('MEDIA', 'Media'), 
        ('ALTA', 'Alta') # Comentario: Esta será la opción por defecto.
    ]

    # Comentario: Columna para el tipo de RQ, usando las opciones definidas arriba.
    tipo_rq = models.CharField(max_length=10, choices=TIPO_OPCIONES)
    
    # Comentario: Columna para el Centro de Costos seleccionado.
    centro_costo = models.CharField(max_length=100, choices=CENTROS_COSTO)
    
    # Comentario: Columna para la prioridad, predeterminada en 'ALTA'.
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_OPCIONES, default='ALTA')
    
    # Comentario: Columna para el título breve del caso (ej. 'Falla UPS').
    titulo_caso = models.CharField(max_length=255)
    
    # Comentario: Columna de texto largo para las justificaciones u observaciones (puede estar en blanco).
    observaciones_generales = models.TextField(blank=True, null=True)
    
    # Comentario: Columna que guarda la fecha exacta automáticamente al momento de crear la solicitud.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Comentario: Método mágico para que Django muestre el título en lugar de "Objeto 1".
    def __str__(self):
        return self.titulo_caso # Comentario: Retorna el título como cadena de texto.

# Comentario: Creamos la tabla independiente para el diccionario dinámico de ítems.
class DiccionarioItems(models.Model): 
    
    # Comentario: Columna para el nombre del producto. 'unique=True' evita repetidos.
    descripcion = models.CharField(max_length=255, unique=True)
    
    # Comentario: Columna para saber cómo se mide (UND, METROS, PAQUETE).
    unidad_medida = models.CharField(max_length=50)
    
    # Comentario: Método mágico de visualización del ítem.
    def __str__(self): 
        return f"{self.descripcion} ({self.unidad_medida})" # Comentario: Ej. "Cable FTP exterior (METROS)".