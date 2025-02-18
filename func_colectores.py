#BIBLIOTECAS
# ..............................................................................

import clr
import Autodesk
import System

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, ElementId, BuiltInCategory

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

#FUNCIONES
# ..............................................................................

def elementos_por_categoria(cat):
    """
    Uso:
        Seleccionar todos los elementos por categoria.
    Entradas:
        cat <Autodesk.Revit.DB.Category>: Categoria.
    Salida:
        Se genera un dicionario separando instancias y tipos
    """
    if isinstance(cat, Autodesk.Revit.DB.Category):
        salida = {"instancias": [], "tipos": []}
        #Iniciamos la coleccion
        coleccion = (FilteredElementCollector(doc).
                     OfCategoryId(cat.Id).ToElements())
        # A cada elemento de la colección se le va a preguntar por el id. 
        # de su tipo. Si el elemento se trata de un tipo nos dará un -1
        # si es una instancia obtendremos un id válido.
        for ele in coleccion:
            if ele.GetTypeId() == ElementId.InvalidElementId:
                salida["tipos"] += [ele]
            else:
                salida['instancias'] += [ele]
    else:
        salida = "Introducir argumento tipo: Autodesk.Revit.DB.Category"            
    return salida
# ..............................................................................
        
def elementos_por_categoria_vista(cat, vista = None):
    """
    Uso:
        Seleccionar todos los elementos por categoria.
    Entradas:
        cat <Autodesk.Revit.DB.Category>: Categoria.
        vista <Autodesk.Revit.DB.View>: El argumento por defecto es un nulo
    Salida:
        Si no se introduce una vista se genera un diccionario separando 
        instancias y tipos. En caso contrario se obtiene una lista de 
        instancias.
    """
    if isinstance(cat, Autodesk.Revit.DB.Category):
        #Se revisa si el usuario ha introducido el argumento de la vista
        if vista is None:
            #Se crea el diccionario y se inicia la colección
            salida = {"instancias": [], "tipos": []}
            #Iniciamos la coleccion
            coleccion = (FilteredElementCollector(doc).
                         OfCategoryId(cat.Id).ToElements())
            # A cada elemento de la colección se le va a preguntar por el id. 
            # de su tipo. Si el elemento se trata de un tipo nos dará un -1
            # si es una instancia obtendremos un id válido.
            for ele in coleccion:
                if ele.GetTypeId() == ElementId.InvalidElementId:
                    salida["tipos"] += [ele]
                else:
                    salida['instancias'] += [ele]
        else:
            #Se revisa el tipo de dato antes de colectar
            if isinstance(vista, Autodesk.Revit.DB.View):
                coleccion = (FilteredElementCollector(doc, vista.Id).OfCategoryId(cat.Id).
                             WhereElementIsNotElementType().ToElements())
                salida = coleccion
            else:
                salida = "Introducir argumento tipo: Autodesk.Revit.DB.View"
    else:
        salida = "Introducir argumento tipo: Autodesk.Revit.DB.Category" 
        
    return salida
# ..............................................................................

def elementos_por_nombre_bic(arg = None):
    """
    Uso:
        Seleccionar todos los elementos por nombre de categoría BuiltIn.
    Entradas:
        arg <str>: Nombre de la categoría BuiltIn.
    Salida:
        Se genera un diccionario separando por instancias y tipos
    """
    #Se accede a la información de las bic
    enumNombres = System.Enum.GetNames(BuiltInCategory)
    enumValores = System.Enum.GetValues(BuiltInCategory)
    # Se revisa si el usuario ha introducido algún argumento
    if bool(arg):
        # Existen varios escenarios posibles
        # Se revisa que el argumento esté dentro de la lista de nombres
        if arg in enumNombres:
            # Escenario 1: El escenario perfecto
            for n, v in zip(enumNombres, enumValores):
                if arg == n:
                    bic = v
            #Iniciamos la colección
            coleccion = (FilteredElementCollector(doc).OfCategory(bic).ToElements())
            # Se consulta el id de su tipo para filtrar instancias y tipos
            # A cada elemento de la colección se le pregunta por su id
            salida = {"instancias": [], "tipos": []}
            for ele in coleccion:
                if ele.GetTypeId() == ElementId.InvalidElementId:
                    salida["tipos"] += [ele]
                else:
                    salida['instancias'] += [ele]
        else:
            """
            No se ha encontrado el argumento introducido, por lo tanto se revisa que
            exista alguna coincidencia parcial. Se evita diferencias entre mayusculas
            y minusculas, pasando todo a minusculas
            """
            # Se almacenan todas las coincidencias
            coincidencias = []
            for nombre in enumNombres:
                if arg.lower() == nombre.lower():
                    coincidencias.append(nombre)
            #Escenario 2: Se encuentran varias coincidencias
            mensaje1 = ("Con el argumento introducido \n"
                        " se han encontrado algunas \n"
                        "opciones. Revisar el listado \n"
                        "de coincidencias.")
            #Escenario 3: No se ha encontrado nada
            mensaje2 = ("Se sugiere revisar el listado de \n"
                        "nombres de categorias built-in. \n"
                        "Con ese argumento no se ha encontrado \n"
                        "nada.")
            if bool(coincidencias):
                #Sacamos las coincidencias ordenadas
                salida = [mensaje1, sorted(coincidencias)]
            else:
                salida = mensaje2
    else:
        #Escenario 4: El usuario no ha introducido ningún argumento
        #Se extrae la lista ordenada de nombres built-in
        salida = sorted(enumNombres)
    
    return salida
# ..............................................................................       


