#BIBLIOTECAS
# ..............................................................................

import clr
import Autodesk
import System

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, ElementId, BuiltInCategory, Document, Level

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

#FUNCIONES
# ..............................................................................
def seleccion_por_nombre_categoria(nombre = None):
    """
    Uso:
        Seleccionar una categoria de Revit por nombre
    Entradas:
        Si el usuario no introduce ningún argumento extrae la lista completa
        de nombre.
        nombre <str>: Nombre de la categoría a seleccionar.
    Salida:
        Si se introduce correctamente el nombre se obtiene una categoría de
        Revit <Category>
    """
    # Se accede al listado completo de categorias y se consultan los nombres
    categorias = doc.Settings.Categories
    nombres = [cat.Name for cat in categorias]
    # Se revisa si el usuario ha introducido algún argumento
    if bool(nombre):
        # Se revisa que el argumento está dentro de la lista de nombres
        if nombre in nombres:
            # Se genera un diccionario para extraer la categoría por clave
            salida = dict(zip(nombres, categorias))[nombre]
        else:
            salida = "Revisar nombre de categoría"
    else:
        # Se extrae la lista ordenada de todos los nombres
        salida = sorted(nombres)
        
    return salida
# ..............................................................................

def seleccion_por_nombre_nivel(nombre = None, documento = doc):
    """
    Uso:
        Seleccionar el nivel de Revit por nombre
    Entradas:
        Si el usuario no introduce ningún argumento extrae la lista completa
        de nombres para que pueda elegir.
        nombre <str>: Nombre del nivel a seleccionar.
    Salida:
        Si se introduce correctamente el nombre se obtiene un nivel
        
    """
    if isinstance(documento, Document):
        # Se accede al listado completo de niveles y se consultan los nombres
        niveles = FilteredElementCollector(documento).OfClass(Level)
        nombres = [niv.Name for niv in niveles]
        # Se revisa si el usuario ha introducido algún argumento para el nivel
        if bool(nombre):
            #Se revisa que el argumento esta dentro de la lista de nombres
            if nombre in nombres:
                # Se genera un diccionario para extraer el nivel
                salida = dict(zip(nombres, niveles))[nombre]
            else:
                # Se le añade un encabezado a la lista
                salida = ['<Opciones de niveles'] + sorted(nombres)
        else:
            # Se extrae la lista ordenada con todos los nombres
            salida = sorted(nombres)
    else:
        salida = "Revisar: Se esperaba un Autodesk.Revit.DB.Document"
        
    return salida