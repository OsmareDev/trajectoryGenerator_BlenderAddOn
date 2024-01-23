bl_info = \
    {
        "name" : "Generador de trayectorias",
        "author" : "Esther, Francisco, Jaime y Oscar",
        "version" : (1, 0, 0),
        "blender" : (2, 90, 1),
        "location" : "View 3D > Tool",
        "description" :
            "interpola el objeto dado, siguiendo la funcion seleccionada",
        "category" : "Interpolacion"
    }

from math import acos, asin, cos, fabs, sin
from random import random
import bpy
from bpy.types import Context
import numpy as np
from mathutils import Quaternion, Vector
from numpy.core.fromnumeric import size
from func_interpolacion import *
from crea_copias import *

#  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄   ▄▄▄▄▄▄▄ 
# █       █       █       █   ▄  █ █       █       █       █   ▄  █ █       █
# █   ▄   █    ▄  █    ▄▄▄█  █ █ █ █   ▄   █▄     ▄█   ▄   █  █ █ █ █  ▄▄▄▄▄█
# █  █ █  █   █▄█ █   █▄▄▄█   █▄▄█▄█  █▄█  █ █   █ █  █ █  █   █▄▄█▄█ █▄▄▄▄▄ 
# █  █▄█  █    ▄▄▄█    ▄▄▄█    ▄▄  █       █ █   █ █  █▄█  █    ▄▄  █▄▄▄▄▄  █
# █       █   █   █   █▄▄▄█   █  █ █   ▄   █ █   █ █       █   █  █ █▄▄▄▄▄█ █
# █▄▄▄▄▄▄▄█▄▄▄█   █▄▄▄▄▄▄▄█▄▄▄█  █▄█▄▄█ █▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄█  █▄█▄▄▄▄▄▄▄█

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀██░▄▄▄░█▄▄░▄▄██░▄▄▄░██░▀██░███░▄▄▀██░▄▄░██░████▄░▄██░▄▄▀█░▄▄▀██░▄▄▀████░█████░▄▄▄░██░▄▄▄░████░▄▄▀██░▄▄▀█▄░▄██░███░██░▄▄▄██░▄▄▀██░▄▄▄░
# ██░▄▄▀██░███░███░████░███░██░█░█░███░▀▀░██░▀▀░██░█████░███░████░▀▀░██░▀▀▄████░█████░███░██▄▄▄▀▀████░██░██░▀▀▄██░████░█░███░▄▄▄██░▀▀▄██▄▄▄▀▀
# ██░▀▀░██░▀▀▀░███░████░▀▀▀░██░██▄░███░██░██░█████░▀▀░█▀░▀██░▀▀▄█░██░██░██░████░▀▀░██░▀▀▀░██░▀▀▀░████░▀▀░██░██░█▀░▀███▄▀▄███░▀▀▀██░██░██░▀▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class MiOperador(bpy.types.Operator):
    """ Aplica los drivers al objetos seleccionado en cada coordenada
    """
    bl_idname = "op.apl_int"
    bl_label = "Aplicando interpolasao"

    # invoke
    def invoke(self, context, event):
        # context.objeto es el objeto seleccionado, el segundo parametro es cada una de las coordenadas a las que aplicar el driver
        IntegraLongitud(context.object)

        context.object.distancia_recorrida = 0
        context.object.keyframe_insert(data_path='distancia_recorrida', frame=1)

        asigna_driver_posicion(context.object, 0)
        asigna_driver_posicion(context.object, 1)
        asigna_driver_posicion(context.object, 2)

        if context.object.activa_orientacion:
            asigna_driver_orientacion(context.object, 0)
            asigna_driver_orientacion(context.object, 1)
            asigna_driver_orientacion(context.object, 2)
            asigna_driver_orientacion(context.object, 3)

        return {"FINISHED"}


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀██░▄▄▄░█▄▄░▄▄██░▄▄▄░██░▀██░████░▄▄░██░▄▄▄██░▀██░██░▄▄▄██░▄▄▀█░▄▄▀██░▄▄▀████░▄▄▀██░▄▄▄░██░▄▄░█▄░▄█░▄▄▀██░▄▄▄░
# ██░▄▄▀██░███░███░████░███░██░█░█░████░█▀▀██░▄▄▄██░█░█░██░▄▄▄██░▀▀▄█░▀▀░██░▀▀▄████░█████░███░██░▀▀░██░██░▀▀░██▄▄▄▀▀
# ██░▀▀░██░▀▀▀░███░████░▀▀▀░██░██▄░████░▀▀▄██░▀▀▀██░██▄░██░▀▀▀██░██░█░██░██░██░████░▀▀▄██░▀▀▀░██░████▀░▀█░██░██░▀▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class Copiador(bpy.types.Operator):
    """ Este operador llama a la funcion de generar las copias
        metiendolas en una coleccion, en caso de que se quiera y se haya seleccionado la opcion adecuada
        se borrara la coleccion anterior y las copias de esa coleccion
    """
    bl_idname = "op.copiador"
    bl_label = "Copiando Objeto"

    # invoke
    def invoke(self, context, event):
        # context.objeto es el objeto seleccionado
        # copy_action es lo que nos permite decirle si queremos que los keyframes de las copias sean independientes de la original
        coll = crea_copias(context.object, context, context.scene.modificaciones)

        return {"FINISHED"}


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀██░▄▄▄░█▄▄░▄▄██░▄▄▄░██░▀██░████░▄▄▀██░▄▄▄██░▄▀▄░█░▄▄▀██░▄▄░██░▄▄▄█░▄▄▀██░▄▄▀████░████░▄▄▀███▄▄░▄▄█░▄▄▀██░▄▄▀██░████░▄▄▀
# ██░▄▄▀██░███░███░████░███░██░█░█░████░▀▀▄██░▄▄▄██░█░█░█░▀▀░██░▀▀░██░▄▄▄█░▀▀░██░▀▀▄████░████░▀▀░█████░███░▀▀░██░▄▄▀██░████░▀▀░
# ██░▀▀░██░▀▀▀░███░████░▀▀▀░██░██▄░████░██░██░▀▀▀██░███░█░██░██░█████░▀▀▀█░██░██░██░████░▀▀░█░██░█████░███░██░██░▀▀░██░▀▀░█░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class Remap(bpy.types.Operator):
    """ Este operador llama a la funcion que genera la tabla de posiciones con la que se compara los frames para obtener los siguientes
    """
    bl_idname = "op.remap"
    bl_label = "updatear la tabla"

    # invoke
    def invoke(self, context, event):
        IntegraLongitud(context.object)
        return {"FINISHED"}

#  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄    ▄ ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄▄ 
# █       █       █  █  █ █       █   █   █       █
# █    ▄  █   ▄   █   █▄█ █    ▄▄▄█   █   █  ▄▄▄▄▄█
# █   █▄█ █  █▄█  █       █   █▄▄▄█   █   █ █▄▄▄▄▄ 
# █    ▄▄▄█       █  ▄    █    ▄▄▄█   █▄▄▄█▄▄▄▄▄  █
# █   █   █   ▄   █ █ █   █   █▄▄▄█       █▄▄▄▄▄█ █
# █▄▄▄█   █▄▄█ █▄▄█▄█  █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░█░▄▄▀██░▀██░██░▄▄▄██░███████░▄▄▀██░▄▄▄░██░▄▄░█▄░▄█░▄▄▀██░▄▄▄░
# ██░▀▀░█░▀▀░██░█░█░██░▄▄▄██░███████░█████░███░██░▀▀░██░██░▀▀░██▄▄▄▀▀
# ██░████░██░██░██▄░██░▀▀▀██░▀▀░████░▀▀▄██░▀▀▀░██░████▀░▀█░██░██░▀▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class CopiasPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Interpolacion"
    bl_label = "Control de Copias"

    # funcion de dibujado del panel
    def draw(self, context):
        layout = self.layout

        # comprobamos que hay un objeto seleccionado activo
        if (context.object): 
            row = layout.row() 
            row.label(text = "Copiar Objeto")
            
            row = layout.row() 
            # BOOL: TRUE: se quieren crear copias ; FALSE: no se quieren crear copias
            row.prop(context.object, 'copiar')
            # se comprueba si se quieren crear copias
            if (context.object.copiar):
                row = layout.row()
                # INT: numero de copias que se desea realizar 
                row.prop(context.object, "n_copias")
                
                row = layout.row()
                row.label(text = "posibilidad de modificar las copias")
                row = layout.row() 
                # BOOL: TRUE: se busca que las copias tengan keyframes independientes ; FALSE: Se busca que las copias sigan los cambios de los frames originales
                row.prop(context.scene, 'modificaciones')

                row = layout.row()
                row.label(text = "posibilidad de eliminar las anteriores")
                row = layout.row() 
                # BOOL: TRUE: se busca eliminar las copias anteriores al crear las nuevas ; FALSE: se busca hacer una coleccion diferente dejando la anterior
                row.prop(context.object, 'eliminar')
                
                row = layout.row()
                # OPERATOR: boton que llama a la creacion de las copias
                row.operator('op.copiador', text="generar copias")
        else:
            row = layout.row()  
            row.label(text="No existe objeto seleccionado")


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░█░▄▄▀██░▀██░██░▄▄▄██░██████░▄▄▀██░█████░▄▄▄█░▄▄▀█▄▄░▄▄██░▄▄▄░██░▄▄▀█▄░▄██░▄▄▄██░▄▄▀█░▄▄▀██░▄▄▀
# ██░▀▀░█░▀▀░██░█░█░██░▄▄▄██░██████░▀▀░██░█████░▄▄▄█░▀▀░███░████░███░██░▀▀▄██░███░▄▄▄██░██░█░▀▀░██░██░
# ██░████░██░██░██▄░██░▀▀▀██░▀▀░███░██░██░▀▀░██░▀▀▀█░██░███░████░▀▀▀░██░██░█▀░▀██░▀▀▀██░▀▀░█░██░██░▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class AleatoriedadPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Interpolacion"
    bl_label = "Control de Aleatoriedad"

    # funcion de dibujado del panel
    def draw(self, context):
        layout = self.layout

        # comprobamos que hay un objeto seleccionado activo
        if (context.object): 
            row = layout.row()
            # BOOL: TRUE: se busca que haya variacion aleatoria en el movimiento del objeto
            row.prop(context.object, 'varia')

            if context.object.varia:
                row = layout.row()
                # FLOAT: amplitud de la variacion aleatoria ; maximo de rango al que pueden llegar las variaciones
                row.prop(context.object, 'm_max')
                row = layout.row()
                # INT: frecuencia de la variacion ; determina la velocidad a la que varian aleatoriamente los objetos
                row.prop(context.object, 'frec')
        else:
            row = layout.row()  
            row.label(text="No existe objeto seleccionado")


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░█░▄▄▀██░▀██░██░▄▄▄██░██████▄░▄██░▀██░█▄▄░▄▄██░▄▄▄██░▄▄▀██░▄▄░██░▄▄▄░██░████░▄▄▀██░▄▄▀█▄░▄██░▄▄▄░██░▀██░
# ██░▀▀░█░▀▀░██░█░█░██░▄▄▄██░███████░███░█░█░███░████░▄▄▄██░▀▀▄██░▀▀░██░███░██░████░▀▀░██░█████░███░███░██░█░█░
# ██░████░██░██░██▄░██░▀▀▀██░▀▀░███▀░▀██░██▄░███░████░▀▀▀██░██░██░█████░▀▀▀░██░▀▀░█░██░██░▀▀▄█▀░▀██░▀▀▀░██░██▄░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class InterpolacionPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Interpolacion"
    bl_label = "Control de Interpolacion"

    # funcion de dibujado del panel
    def draw(self, context):
        layout = self.layout

        # comprobamos que hay un objeto seleccionado activo
        if (context.object): 
            row = layout.row()
            row.label(text = "Metodos Interpolacion Objetos")
            row = layout.row()
            # ENUM: LINEAL, HERMITE, CATMULL-ROM, BEZIER: seleccionable de los diferentes metodos de interpolacion
            row.prop(context.object, "method")
            
            # comprobar que esta seleccionado el metodo de catmull-rom para pedir el tau
            if context.object.method == "Catmull-Rom":
                row = layout.row()
                row.prop(context.object, "tau")
            # en el caso de hermite y bezier avisar al usuario de que debe usar los handlers de blender
            elif context.object.method == "Hermite" and context.object.method == "Bezier":
                row = layout.row()
                row.label(text = "se usan los handles de blender")
            
            row = layout.row()
            
            # comprobar que hay keyframes en el objeto
            if context.object.animation_data:
                # OPERATOR: boton que implanta los drivers
                row.operator('op.apl_int', text="Interpolar")
            else:
                row.label(text= "Introduce keyframes en el objeto para interpolar")
        else:
            row = layout.row()  
            row.label(text="No existe objeto seleccionado")


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░█░▄▄▀██░▀██░██░▄▄▄██░███████░▄▄▀██░▄▄▄░██░▀██░█▄▄░▄▄██░▄▄▀██░▄▄▄░██░███████░███░██░▄▄▄██░███
# ██░▀▀░█░▀▀░██░█░█░██░▄▄▄██░███████░█████░███░██░█░█░███░████░▀▀▄██░███░██░████████░█░███░▄▄▄██░███
# ██░████░██░██░██▄░██░▀▀▀██░▀▀░████░▀▀▄██░▀▀▀░██░██▄░███░████░██░██░▀▀▀░██░▀▀░█████▄▀▄███░▀▀▀██░▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class ControlPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Interpolacion"
    bl_label = "Control de Velocidad"

    # funcion de dibujado del panel
    def draw(self, context):
        layout = self.layout

        # comprobamos que hay un objeto seleccionado activo
        if (context.object): 

            row = layout.row()

            #BOOL: TRUE: se busca que que recorra la curva con la nueva version
            row.prop(context.object, 'usarNuevo')

            if context.object.usarNuevo:
                row = layout.row()
                row.prop(context.object, 'aplica_reparam')
                if not(context.object.aplica_reparam):
                    row = layout.row()
                    row.prop(context.object, 'velocidad')
                    row = layout.row()
                    row.prop(context.object, 'adaptar')

            row = layout.row()
            row.operator('op.remap', text="Update table")
        else:
            row = layout.row()  
            row.label(text="No existe objeto seleccionado")


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░█░▄▄▀██░▀██░██░▄▄▄██░███████░▄▄▄░██░▄▄▀█▄░▄██░▄▄▄██░▀██░█▄▄░▄▄█░▄▄▀██░▄▄▀█▄░▄██░▄▄▄░██░▀██░
# ██░▀▀░█░▀▀░██░█░█░██░▄▄▄██░███████░███░██░▀▀▄██░███░▄▄▄██░█░█░███░███░▀▀░██░█████░███░███░██░█░█░
# ██░████░██░██░██▄░██░▀▀▀██░▀▀░████░▀▀▀░██░██░█▀░▀██░▀▀▀██░██▄░███░███░██░██░▀▀▄█▀░▀██░▀▀▀░██░██▄░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

class OrientationPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Interpolacion"
    bl_label = "Control de la orientacion"

    # funcion de dibujado del panel
    def draw(self, context):
        layout = self.layout

        # comprobamos que hay un objeto seleccionado activo
        if (context.object): 

            row = layout.row()

            #BOOL: TRUE: se busca que se use el control de la orientacion
            row.prop(context.object, 'activa_orientacion')

            if context.object.activa_orientacion:
                row = layout.row()
                row.prop(context.object, 'eje_forward')
                row = layout.row()
                row.prop(context.object, 'eje_lateral')

                row = layout.row()
                row.prop(context.object, 'rot_giro')

                    
        else:
            row = layout.row()  
            row.label(text="No existe objeto seleccionado")

#  ▄▄▄▄▄▄▄ ▄▄▄     ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
# █       █   █   █       █       █       █
# █       █   █   █   ▄   █  ▄▄▄▄▄█  ▄▄▄▄▄█
# █     ▄▄█   █   █  █▄█  █ █▄▄▄▄▄█ █▄▄▄▄▄ 
# █    █  █   █▄▄▄█       █▄▄▄▄▄  █▄▄▄▄▄  █
# █    █▄▄█       █   ▄   █▄▄▄▄▄█ █▄▄▄▄▄█ █
# █▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

class MiPropertyGroup(bpy.types.PropertyGroup):
    tiempo: bpy.props.IntProperty(name="Frames")
    distancia: bpy.props.FloatProperty(name="distancias")


#  ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄  ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
# █  █▄█  █       █       █       █      ██       █       █
# █       █    ▄▄▄█▄     ▄█   ▄   █  ▄    █   ▄   █  ▄▄▄▄▄█
# █       █   █▄▄▄  █   █ █  █ █  █ █ █   █  █ █  █ █▄▄▄▄▄ 
# █       █    ▄▄▄█ █   █ █  █▄█  █ █▄█   █  █▄█  █▄▄▄▄▄  █
# █ ██▄██ █   █▄▄▄  █   █ █       █       █       █▄▄▄▄▄█ █
# █▄█   █▄█▄▄▄▄▄▄▄█ █▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄▄▄▄██▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

def updateMethod(self, context):
    IntegraLongitud(self)


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# █▄░▄██░▀██░█▄▄░▄▄██░▄▄▄██░▄▄░██░▄▄▀█░▄▄▀██░▄▄▀████░████░▄▄▀████░▄▄▀██░██░██░▄▄▀██░███░█░▄▄▀
# ██░███░█░█░███░████░▄▄▄██░█▀▀██░▀▀▄█░▀▀░██░▀▀▄████░████░▀▀░████░█████░██░██░▀▀▄███░█░██░▀▀░
# █▀░▀██░██▄░███░████░▀▀▀██░▀▀▄██░██░█░██░██░██░████░▀▀░█░██░████░▀▀▄██▄▀▀▄██░██░███▄▀▄██░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def IntegraLongitud (obj):
    
    estado = obj.usarNuevo

    obj.usarNuevo = False
    obj.listaCurva.clear()

    # aqui me guardo la posicion en el fotograma 1 y empiezo a construir la table
    # comienza en el primer frame porque python prefiere empezar en el 1
    pos_x = custom_pos(1, obj, 0)
    pos_y = custom_pos(1, obj, 1)
    pos_z = custom_pos(1, obj, 2)

    distanciaTotal = 0

    posicion_anterior = Vector((pos_x, pos_y, pos_z))
    primeraDistancia = obj.listaCurva.add()
    primeraDistancia.tiempo = 1
    primeraDistancia.distancia = 0

    # el for comienza en el 2 porque el primer frame ya esta guardado
    for i in range(2, int(obj.animation_data.action.fcurves[0].keyframe_points[-1].co[0])):
        nuevoPar = obj.listaCurva.add()
        nuevoPar.tiempo = i
        pos_x = custom_pos(i, obj, 0)
        pos_y = custom_pos(i, obj, 1)
        pos_z = custom_pos(i, obj, 2)
        pos = Vector((pos_x, pos_y, pos_z))
        distanciaTotal += (posicion_anterior - pos).magnitude

        nuevoPar.distancia = distanciaTotal
        posicion_anterior = pos

    obj.usarNuevo = estado

    # por algun motivo blender no updatea los caminos a no ser que le obligues con alguna funcion suya
    bpy.ops.object.paths_calculate(start_frame=1, end_frame=250)
    bpy.ops.object.paths_clear()



# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# █░▄▄▀██░█████░▄▄▄█░▄▄▀█▄▄░▄▄██░▄▄▄░██░▄▄▀█▄░▄██░▄▄▄██░▄▄▀█░▄▄▀██░▄▄▀████░▄▄▄██░▀██░████░████░▄▄▀████░▄▄▀██░██░██░▄▄▀██░███░█░▄▄▀
# █░▀▀░██░█████░▄▄▄█░▀▀░███░████░███░██░▀▀▄██░███░▄▄▄██░██░█░▀▀░██░██░████░▄▄▄██░█░█░████░████░▀▀░████░█████░██░██░▀▀▄███░█░██░▀▀░
# █░██░██░▀▀░██░▀▀▀█░██░███░████░▀▀▀░██░██░█▀░▀██░▀▀▀██░▀▀░█░██░██░▀▀░████░▀▀▀██░██▄░████░▀▀░█░██░████░▀▀▄██▄▀▀▄██░██░███▄▀▄██░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def varia_posicion(frame, obj, coord):
    """ Funcion que calcula la variacion de la posicion para el objeto en un instante dado

        frame: frame actual del objeto
        obj: objeto del cual sacaremos variables propias como la frecuencia, la amplitud, el valor aleatorio de desplazamiento y poder añadirle le valor aleatorio que sumar a cada 
                coordenada
        coord: coordenada actual para la cual se hara el calculo

        Nuestra implementacion sigue la siguiente forma:
            Primero desplaza el frame en el que se esta de manera aleatoria usando una variable propia del objeto para que cada una de las copias esten desplazadas diferentemente
                esto consigue que parezca que cada una se mueve a un ritmo diferente
            
            Cada vez que se completa un loop se cambia el valor aleatorio al que se pretende llegar dentro de un rango fijado por el usuario a traves de la interfaz

            Luego sigue una formula que busca que durante una frecuencia fijada por el usuario vaya de 0 hasta el maximo del valor aleatorio y de ahi hasta 0 de nuevo en tantos pasos 
                como dicte la frecuencia siguiendo la forma de un seno
    """

    # IMPORTANTE: no se esta modificando el frame en el que se esta sino que se esta tomando en cuenta un desplazamiento imaginario para que en el frame actual de lo que deberia 
    #               dar por ejemplo dentro de 3 frames, esto se hace para que no vayan todos los objetos a la vez 
    frame_desp = frame + int(obj.desp_rand*obj.frec)
    
    # se comprueba si ha acabado el plazo fijado por la frecuencia y debe cambiarse a un nuevo valor
    if (frame_desp % obj.frec) == 0:
        obj.rand_val[coord] = (np.random.random()-0.5)*(obj.m_max*2)
    
    # (PI / frecuencia) * (resto de frane desplazado partido la frecuencia) -> esto dara un valor entre 0 y PI para que al meterlo en el seno de valores entre 0 y 1 
    # estos valores se multiplicaran por el numero aleatorio para que vaya hasta el y vuelva de esta manera tener control sobre la frecuencia y fuerza con la que cambian los valores
    x_var = np.sin((np.pi/obj.frec) * (frame_desp % obj.frec)) * obj.rand_val[coord]
    
    return x_var


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░██░▄▄▄░██░▄▄▀██░▄▄▀██░▄▄▄██░▀██░█▄▄░▄▄█░▄▄▀█████░██░▄▄▄████░▄▄▀██░▄▄▄██░▄▄▀██░▄▄▄░██░▄▄▀██░▄▄▀█▄░▄██░▄▄▀██░▄▄▄░
# ██░▀▀░██░███░██░▀▀▄██░█████░▄▄▄██░█░█░███░███░▀▀░█████░██░▄▄▄████░▀▀▄██░▄▄▄██░█████░███░██░▀▀▄██░▀▀▄██░███░██░██░███░
# ██░█████░▀▀▀░██░██░██░▀▀▄██░▀▀▀██░██▄░███░███░██░██░▀▀░██░▀▀▀████░██░██░▀▀▀██░▀▀▄██░▀▀▀░██░██░██░██░█▀░▀██░▀▀░██░▀▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def media_tiempo(tiempo_act, tiempo_ini, tiempo_fin):
    """ Funcion que calcula la media de tiempo donde estas respecto a dos puntos en el tiempo

        tiempo_act: frame actual
        tiempo_ini: frame en el que comienza el tramo, obtenido a traves del keyframe inicial del tramo
        tiempo:fin: frame en el que finaliza el tramo, obtenido a traves del keyframe final del tramo

        Se sigue la siguiente formula:
        u = (tiempo actual - tiempo inicial) / (tiempo final - tiempo inicial)
    
    """
    u = (tiempo_act-tiempo_ini)/(tiempo_fin-tiempo_ini)
    return u


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▄██░▄▄▀█░▄▄▀██░▄▀▄░██░▄▄▄████░▄▄▄██░▄▄░██░██░█▄░▄██░███░█░▄▄▀██░█████░▄▄▄██░▀██░█▄▄░▄▄██░▄▄▄███▄▄░▄▄█░▄▄▀██░▄▄▀██░████░▄▄▀
# ██░▄▄███░▀▀▄█░▀▀░██░█░█░██░▄▄▄████░▄▄▄██░██░██░██░██░████░█░██░▀▀░██░█████░▄▄▄██░█░█░███░████░▄▄▄█████░███░▀▀░██░▄▄▀██░████░▀▀░
# ██░█████░██░█░██░██░███░██░▀▀▀████░▀▀▀██▄▄░▀██▄▀▀▄█▀░▀███▄▀▄██░██░██░▀▀░██░▀▀▀██░██▄░███░████░▀▀▀█████░███░██░██░▀▀░██░▀▀░█░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def parametro_de_longitud (lon, obj):
    """ Funcion que calcula el cambio de frame conforme la longitud deseada

        lon: longitud actual
        obj: objeto actual

        Se lee la lista por iteraciones y cada iteracion se comprueba que el objeto no esta parado, esto tambien sirve para comprobar que no es el primer frame, en caso de que asi sea 
            se evita realizar la funcion media_tiempo, que para este caso calculara en que punto entre las dos distancias se encuentra la longitud indicada para el frame, debido a que 
            se dividiria entre 0. Esto dara un valor entre 0 y 1 que servira para ver cual es el valor del tiempo para que al pasarselo a las funciones de interpolacion se encuentre en
            el punto exacto de esa longitud en la curva
    
    """
    distancia_ant = 0
    tiempo_ant = 1

    nuevoFrame = 1
    for item in obj.listaCurva:
        if lon < item.distancia:
            if item.distancia - distancia_ant == 0:
                u = 0
            else:
                u = media_tiempo(lon, distancia_ant, item.distancia)
            t = (item.tiempo - tiempo_ant) * u
            nuevoFrame = tiempo_ant + t
            break
        # en caso de que se desee ir mas alla de la trayectoria fijada por la curva parametrizada, limitarlo al ultimo frame de la curva
        # de este modo evitamos que al introducir una longitud mayor deseada que la longitud final de la curva de error y tome 0 como valor, haciendo de esta manera que simplemente se quede al final
        nuevoFrame = tiempo_ant
        distancia_ant = item.distancia
        tiempo_ant = item.tiempo

    return nuevoFrame


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▀██░██░██░██░▄▄▄██░███░██░▄▄▄░████░▄▄▄██░▄▄▀█░▄▄▀██░▄▀▄░██░▄▄▄
# ██░█░█░██░██░██░▄▄▄███░█░███░███░████░▄▄███░▀▀▄█░▀▀░██░█░█░██░▄▄▄
# ██░██▄░██▄▀▀▄██░▀▀▀███▄▀▄███░▀▀▀░████░█████░██░█░██░██░███░██░▀▀▀
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def nuevo_Frame(frame, obj):
    """ Funcion que cambia el frame dado por el nuevo para el control de velocidades en la curva

        frame: el frame actual de blender
        obj: el objeto del que se desea realizar el cambio

        Primero se comprueba si desea hacerse un cambio automatico o si se desea hacer caso a los keyframes introducidos para el control por distancias, en caso de que se desee no controlar
            por distancias el calculo se hara automaticamente, de esta manera la curva se recorrera a velocidad constante, y la velocidad por frame sera introducida por la interfaz. Luego
            en caso de querer adaptar la animacion a esta velocidad se llamara a la funcion creada para ello y por ultimo devolvera el frame recalculado

    """

    if (obj.aplica_reparam):
        lon = obj.distancia_recorrida
    else:
        # restamos 1 a los frames debido a que blender comienza las animaciones en el frame 1
        lon = (frame-1) * obj.velocidad

    nuevoFrame = parametro_de_longitud(lon, obj)

    # se comprueba tambien que no este seleccionada la opcion de control por distancias
    if obj.adaptar and not obj.aplica_reparam:
        final_ani(obj)

    return nuevoFrame


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▄█▄░▄██░▀██░█░▄▄▀██░██████░▄▄▀██░▀██░█▄░▄
# ██░▄▄███░███░█░█░█░▀▀░██░██████░▀▀░██░█░█░██░█
# ██░████▀░▀██░██▄░█░██░██░▀▀░███░██░██░██▄░█▀░▀
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def final_ani(obj):
    """ Funcion que adapta la animacion a la nueva velocidad a la que se recorre la curva

        obj: el objeto del que se desea tomar el cambio

        Se realiza el calculo del frame final tomando la ultima distancia de la lista y dividiendolo entre la velocidad para saber cuantos frames haran falta

    """

    frame_final = int(obj.listaCurva[-1].distancia/obj.velocidad)
    bpy.context.scene.frame_end = frame_final+1


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▄░██░▄▄▀█▄▄░▄▄████░▄▄▀██░██░█░▄▄▀█▄▄░▄▄██░▄▄▄██░▄▄▀██░▀██░█▄░▄██░▄▄▄░██░▀██░
# ██░███░██░▄▄▀███░██████░█████░██░█░▀▀░███░████░▄▄▄██░▀▀▄██░█░█░██░███░███░██░█░█░
# ██░▀▀▀░██░▀▀░███░██████░▀▀▄██▄▀▀▄█░██░███░████░▀▀▀██░██░██░██▄░█▀░▀██░▀▀▀░██░██▄░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def obt_cuaternion(u, v):
    """ Funcion que calcula el cuaternion que rota un vector y lo hace coincidir con otro

        u: vector original que se busca rotar
        v: vector de referencia al cual se busca imitar

        Se realiza el calculo siguiendo las diferentes formulas del tema como lo son:

            angulo = arccos(u . v)
            eje de rotacion = (u x v)/|u+v|

            quaternion = (cos(angulo/2), eje de rotacion * sen(angulo/2))

    """

    # normalizamos los vectores
    u = u.normalized()
    v = v.normalized()

    # encontramos el eje de rotación
    a = u.cross(v) 
    a = a.normalized()

    # conseguimos el angulo de rotacion, puede dar problemas si el modulo del dot es mayor que 1
    dot = u.dot(v)
    if dot >= 1:
        dot = 1
    elif dot <= -1:
        dot = -1

    theta = acos(dot)

    # calculamos el cuaternion que necesitamos
    q = Quaternion(( cos(theta/2), a[0] * sin(theta/2), a[1] * sin(theta/2), a[2] * sin(theta/2) ))
    return q


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀█░▄▄▀██░█████░▄▄▀████░▄▄▀██░██░█░▄▄▀█▄▄░▄▄██░▄▄▄██░▄▄▀██░▀██░█▄░▄██░▄▄▄░██░▀██░████░▄▄▄█▄░▄██░▀██░█░▄▄▀██░███
# ██░████░▀▀░██░█████░███████░█████░██░█░▀▀░███░████░▄▄▄██░▀▀▄██░█░█░██░███░███░██░█░█░████░▄▄███░███░█░█░█░▀▀░██░███
# ██░▀▀▄█░██░██░▀▀░██░▀▀▄████░▀▀▄██▄▀▀▄█░██░███░████░▀▀▀██░██░██░██▄░█▀░▀██░▀▀▀░██░██▄░████░████▀░▀██░██▄░█░██░██░▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def calc_cuaternion_final(obj, dir, vec, ang):
    """ Funcion que calcula el cuaternion final que se aplicara al objeto

        obj: objeto que se busca rotar
        dir: vector forward elegido para el objeto, la cara de este
        vec: tangente a la trayectoria de la curva
        ang: angulo auxiliar del que se busca realizar una rotacion final para crear un efecto de balanceo o alebeo

        Para conseguir esto rotamos primero el vector frontal para que siga la trayectoria de la curva: esto es q1
        Rotamos el vector lateral elegido por el usuario y lo rotamos con q1 para obtener el desvio que debemos arreglar, para esto
            multiplicamos vectorialmente el vector global arriba con el vector de direccion de la curva para consegui un vector paralelo al suelo
            asi es como querremos dejar nuestro vector lateral por lo que conseguimos un segundo quaternion: esto es q2
        Por ultimo queremos aplicar el alebeo por lo que generamos un quaternion que rote alrededor del eje de la curva: esto es q3

        Con estos 3 quaterniones los rotamos siguiendo el orden de la siguiente manera:
            q3 @ (q2 @ q1) o (q3 @ q2) @ q1
            Con esto obtendriamos el cuaternion final

    """

    if obj.eje_lateral == "EJE_X":
        lat = Vector((1,0,0))
    elif obj.eje_lateral == "EJE_Y":
        lat = Vector((0,1,0))
    elif obj.eje_lateral == "EJE_Z":
        lat = Vector((0,0,1))
    elif obj.eje_lateral == "EJE_-X":
        lat = Vector((-1,0,0))
    elif obj.eje_lateral == "EJE_-Y":
        lat = Vector((0,-1,0))
    else:
        lat = Vector((0,0,-1))


    front = dir
    # comp: vector que sobra de las elecciones de lateral y frontal, 
    comp = Vector((1,1,1)) - lat - front

    front = front.normalized()
    vec = vec.normalized()
    lat = lat.normalized()


    q11 = obt_cuaternion(front, vec)

    lat.rotate(q11)
 
    # alinear el lateral paralelo al suelo
    z = Vector((0,0,1))
    l = z.cross(vec)
    l = l.normalized()

    q21 = obt_cuaternion(lat, l)

    # alebeo
    q31 = Quaternion(( cos(ang/2), vec[0] * sin(ang/2), vec[1] * sin(ang/2), vec[2] * sin(ang/2) ))

    qfinal = q31 @ (q21 @ q11)

    comp.rotate(qfinal)

    return qfinal
    

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░██░▄▄▄█▄▄░▄▄████░█▀▄██░▄▄▄██░███░██░▄▄▄██░▄▄▀█░▄▄▀██░▄▀▄░██░▄▄▄████░▄▄▀██░▄▄▄██░▄▄▄██░▄▄▄██░▄▄▀██░▄▄▄██░▀██░██░▄▄▀██░▄▄▄
# ██░█▀▀██░▄▄▄███░██████░▄▀███░▄▄▄██▄▀▀▀▄██░▄▄███░▀▀▄█░▀▀░██░█░█░██░▄▄▄████░▀▀▄██░▄▄▄██░▄▄███░▄▄▄██░▀▀▄██░▄▄▄██░█░█░██░█████░▄▄▄
# ██░▀▀▄██░▀▀▀███░██████░██░██░▀▀▀████░████░█████░██░█░██░██░███░██░▀▀▀████░██░██░▀▀▀██░█████░▀▀▀██░██░██░▀▀▀██░██▄░██░▀▀▄██░▀▀▀
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def get_keyframe_reference(frame, obj, coord):
    """ Funcion recoje los parametros necesarios para llamar a las funciones de hermite, catmull-rom, etc

        frame: frame actual de la animacion
        obj: objeto que se busca rotar
        coord: eje que se desea calcular

    """

    keyframes = obj.animation_data.action.fcurves[coord].keyframe_points

    if frame <= keyframes[0].co[0]:
        i = 1
    elif frame >= keyframes[-1].co[0]:
        i = size(keyframes)-1
    else:
        i = 0
        # Averiguamos en que tramo esta el frame 
        while keyframes[i].co[0] < frame:
            i += 1 

    t_ini = keyframes[i-1].co[0]
    t_fin = keyframes[i].co[0]
    pos_ini = keyframes[i-1].co[1]
    pos_fin = keyframes[i].co[1]
    p_ant = 0
    p_post = 0
    v_ini = 0
    v_fin = 0
    
    u = media_tiempo(frame, t_ini, t_fin)

    if (obj.method == "Catmull-Rom"):
        if (i < 2):
            p_ant = pos_ini
            
            #comprobamos que haya un keyframe tras el final viendo si el array de keyframes tiene mas de 2 keyframes, si no que use el ultimo como posterior
            if (len(keyframes)-1) < 3:
                p_post = pos_fin
            else:
                p_post = keyframes[i+1].co[1]
        # para cuando este en el ultimo intervalo
        elif (i > len(keyframes)-2):
            p_ant = keyframes[i-2].co[1]
            p_post = pos_fin
        # en los demas intervalos
        else:
            p_ant = keyframes[i-2].co[1]
            p_post = keyframes[i+1].co[1]
    elif (obj.method == "Hermite"):
        v_ini = keyframes[i-1].handle_right[1] - pos_ini
        v_fin = pos_fin - keyframes[i].handle_left[1]
            

    return u, pos_ini, pos_fin, p_ant, p_post, v_ini, v_fin


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄░██░▄▄▄█▄▄░▄▄████░▄▄▀██░██░██░▄▄▄░█▄▄░▄▄██░▄▄▄░██░▄▀▄░████░▄▄░██░██░█░▄▄▀█▄▄░▄▄
# ██░█▀▀██░▄▄▄███░██████░█████░██░██▄▄▄▀▀███░████░███░██░█░█░████░██░██░██░█░▀▀░███░██
# ██░▀▀▄██░▀▀▀███░██████░▀▀▄██▄▀▀▄██░▀▀▀░███░████░▀▀▀░██░███░████▄▄░▀██▄▀▀▄█░██░███░██
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def get_custom_quat(frame, obj, coord):
    """ Driver de los angulos del objeto

        frame: frame actual de la animacion
        obj: objeto que se busca rotar
        coord: eje que se desea calcular

        Esta funcion es la que obtendra el cuaternion del objeto
    """

    method = obj.method

    if obj.usarNuevo:
        frame = nuevo_Frame(frame, obj)

    if obj.eje_forward == "EJE_X":
        dir = Vector((1,0,0))
    elif obj.eje_forward == "EJE_Y":
        dir = Vector((0,1,0))
    elif obj.eje_forward == "EJE_Z":
        dir = Vector((0,0,1))
    elif obj.eje_forward == "EJE_-X":
        dir = Vector((-1,0,0))
    elif obj.eje_forward == "EJE_-Y":
        dir = Vector((0,-1,0))
    else:
        dir = Vector((0,0,-1))

    rot = obj.rot_giro

    # obtienes todos los valores necesarios para calcular la derivada en el frame y la siguiente
    # con la derivada sacas el vector tangente y con la segunda derivada sacaremos el radio de la curvatura
    u_x, p_ini_x, p_fin_x, p_ant_x, p_post_x, v_ini_x, v_fin_x = get_keyframe_reference(frame, obj, 0)
    u_y, p_ini_y, p_fin_y, p_ant_y, p_post_y, v_ini_y, v_fin_y = get_keyframe_reference(frame, obj, 1)
    u_z, p_ini_z, p_fin_z, p_ant_z, p_post_z, v_ini_z, v_fin_z = get_keyframe_reference(frame, obj, 2)
    
    if (method == "Lineal"):
        deriv = Vector((lineal_der(p_ini_x, p_fin_x, u_x), lineal_der(p_ini_y, p_fin_y, u_z), lineal_der(p_ini_z, p_fin_z, u_z)))
        deriv2 = Vector((0,0,0))
    elif (method == "Hermite"):
        deriv = Vector((hermite_der(u_x, p_ini_x, p_fin_x, v_ini_x, v_fin_x), hermite_der(u_y, p_ini_y, p_fin_y, v_ini_y, v_fin_y), hermite_der(u_z, p_ini_z, p_fin_z, v_ini_z, v_fin_z)))
        deriv2 = Vector((hermite_der2(u_x, p_ini_x, p_fin_x, v_ini_x, v_fin_x), hermite_der2(u_y, p_ini_y, p_fin_y, v_ini_y, v_fin_y), hermite_der2(u_z, p_ini_z, p_fin_z, v_ini_z, v_fin_z)))
    elif (method == "Catmull-Rom"):
        deriv = Vector((catmull_rom_der(u_x, p_ant_x, p_ini_x, p_fin_x, p_post_x, obj.tau), catmull_rom_der(u_y, p_ant_y, p_ini_y, p_fin_y, p_post_y, obj.tau), catmull_rom_der(u_z, p_ant_z, p_ini_z, p_fin_z, p_post_z, obj.tau)))
        deriv2 = Vector((catmull_rom_der2(u_x, p_ant_x, p_ini_x, p_fin_x, p_post_x, obj.tau), catmull_rom_der2(u_y, p_ant_y, p_ini_y, p_fin_y, p_post_y, obj.tau), catmull_rom_der2(u_z, p_ant_z, p_ini_z, p_fin_z, p_post_z, obj.tau)))
    elif (method == "Bezier"):
        deriv = Vector((bezier_der(u_x, p_ini_x, v_ini_x, v_fin_x, p_fin_x), bezier_der(u_y, p_ini_y, v_ini_y, v_fin_y, p_fin_y), bezier_der(u_z, p_ini_z, v_ini_z, v_fin_z, p_fin_z)))
        deriv2 = Vector((bezier_der2(u_x, p_ini_x, v_ini_x, v_fin_x, p_fin_x), bezier_der2(u_y, p_ini_y, v_ini_y, v_fin_y, p_fin_y), bezier_der2(u_z, p_ini_z, v_ini_z, v_fin_z, p_fin_z)))

    rot = calcula_rot(obj, deriv, deriv2, rot)

    q = calc_cuaternion_final(obj, dir, deriv, rot)

    return q[coord]


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀█░▄▄▀██░█████░▄▄▀██░██░██░████░▄▄▀████░▄▄▀██░▄▄▄░█▄▄░▄▄
# ██░████░▀▀░██░█████░█████░██░██░████░▀▀░████░▀▀▄██░███░███░██
# ██░▀▀▄█░██░██░▀▀░██░▀▀▄██▄▀▀▄██░▀▀░█░██░████░██░██░▀▀▀░███░██
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def calcula_rot(obj, deriv, deriv2, rot):
    """ Funcion que calcula la rotacion para esta iteracion de la animacion

        obj: objeto que se va a rotar
        deriv: 1era derivada de la curva
        deriv2: 2a derivada de la curva
        rot: angulo de rotacion maximo
    """

    # el producto vectorial de la 1era dervida con el de la segunda da un vector que indica con su eje z si esta gira hacia derecha o izquierda
    x = deriv2.cross(deriv)
    x = x.normalized()

    # al normalizar la segunda derivada conseguimos que tenga valores que no pasen el limite -1 , 1
    deriv2 = deriv2.normalized()

    # se usa el contador brusco para llevar la cuenta de cuanto permanece en una curva y dependiendo de este numero varia la cantidad de rotacion
    # siendo el maximo el introducido por el usuario, el maximo de esta variable son 20 porque se tiene en cuenta que se actualizara 4 veces por frame
    # al ser usada por 4 drivers distintos en un mismo frame, esto podria evitarse guardando el frame actual y viendo que no se repita cuando vaya a 
    # actualizarse
    if x[2] < 0:
        obj.cont_brusco += 1
        
    elif x[2] > 0:
        obj.cont_brusco -= 1
    else:
        rot = 0

    rot = rot * obj.cont_brusco/20

    return rot
    

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▄██░██░██░▀██░██░▄▄▀█▄░▄██░▄▄▄░██░▀██░████░▄▄░██░▄▄▀█▄░▄██░▀██░██░▄▄▀█▄░▄██░▄▄░█░▄▄▀██░███
# ██░▄▄███░██░██░█░█░██░█████░███░███░██░█░█░████░▀▀░██░▀▀▄██░███░█░█░██░█████░███░▀▀░█░▀▀░██░███
# ██░█████▄▀▀▄██░██▄░██░▀▀▄█▀░▀██░▀▀▀░██░██▄░████░█████░██░█▀░▀██░██▄░██░▀▀▄█▀░▀██░████░██░██░▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def custom_pos(frame, obj, coord):
    """ FUNCION CENTRAL:

        frame:  frame actual
        obj:    objeto actual activo de las escena
        coord:  coordenada del eje: siendo estas 0: x ; 1: y ; 2: z

        Esta funcion es la que obtendra entre que par de frames esta el actual y llamara a las funciones de interpolacion dependiendo de las elecciones del usuario

    """

    # En caso de que se quiera usar el nuevo sistema implementado para la fase 2
    if obj.usarNuevo:
        frame = nuevo_Frame(frame, obj)

    # Recoger la lista de keyframes, de un determinado eje coord
    # para ello se accede al objeto y en animation_data.action.f_curves podemos elegir la coordenada la cual queremos
    # dentro de esto una vez elegida la coordenada obtenemos los keyframe points 
    keyframes = obj.animation_data.action.fcurves[coord].keyframe_points

    # recogemos el metodo seleccionado por el usuario a traves de su valor propio
    method = obj.method

    # Comprobamos si estamos antes del primer keyframe
    if frame <= keyframes[0].co[0]:
        posx = keyframes[0].co[1]
        
    # Comprobar si estamos tras el ultimo keyframe
    elif frame >= keyframes[-1].co[0]:
        posx = keyframes[-1].co[1]
    
    # Dependiendo del metodo seleccionado hacer uno u otro
    else:
        i = 0
        # Averiguamos en que tramo esta el frame 
        while keyframes[i].co[0] < frame:
            i += 1 

        # posicion inicial y final del tramo, obtenidas a partir de los keyframes
        #       Estructura del vector de keyframes
        #       keyframes[n] son todos los keyframes
        #       keyframes[n].co[0] son los tiempos (frame especifico) de cada keyframe
        #       keyframes[n].co[1] son las posiciones de cada keyframe

        pos_ini = keyframes[i-1].co[1]
        pos_fin = keyframes[i].co[1]
        t_ini = keyframes[i-1].co[0]
        t_fin = keyframes[i].co[0]
        u = media_tiempo(frame, t_ini, t_fin)

        #--------------
        #--- LINEAL ---
        #--------------
        if (method == "Lineal"):
            posx = lineal(pos_ini, pos_fin, u)

        #---------------
        #--- HERMITE ---
        #---------------
        elif (method == "Hermite"):
            # las velocidades vendran recogidas a traves de los handles de blender 
            # la velocidad inicial sera la diferencia entre la posicion del handle derecho y la posicion del keyframe inicial
            v_ini = keyframes[i-1].handle_right[1] - pos_ini
            # la velocidad final sera la diferencia entre el keyframe final y la posicion del handle izquierdo
            v_fin = pos_fin - keyframes[i].handle_left[1]

            posx = hermite(u, pos_ini, pos_fin, v_ini, v_fin)

        #-------------------
        #--- CATMULL-ROM ---
        #-------------------
        elif (method == "Catmull-Rom"):
            # Al hacer uso de un punto anterior y otro posterior al tramo debemos comprobar que estos no sean el tramo inicial ni el final
            #   de ser asi el tramo inicial debera usar el keyframe inicial como el anterior y en el caso de ser el tramo final se debera hacer uso del
            #   keyframe final como el keyframe posterior

            # para cuando este en el primer intervalo
            if (i < 2):
                p_ant = pos_ini
                
                #comprobamos que haya un keyframe tras el final viendo si el array de keyframes tiene mas de 2 keyframes, si no que use el ultimo como posterior
                if (len(keyframes)-1) < 3:
                    p_post = pos_fin
                else:
                    p_post = keyframes[i+1].co[1]
            # para cuando este en el ultimo intervalo
            elif (i > len(keyframes)-2):
                p_ant = keyframes[i-2].co[1]
                p_post = pos_fin
            # en los demas intervalos
            else:
                p_ant = keyframes[i-2].co[1]
                p_post = keyframes[i+1].co[1]
            
            # valor de la tension que sirve para ampliar o reducir la velocidad de pasada por los puntos
            # se recoje a traves de su valor propio en el objeto
            tau = obj.tau
            posx = catmull_rom(u, p_ant, pos_ini, pos_fin, p_post, tau)

        #--------------
        #--- BEZIER ---
        #--------------
        elif (method == "Bezier"):
            # como en el caso de hermite 
            # la velocidad inicial sera la diferencia entre la posicion del handle derecho y la posicion del keyframe inicial
            b_ini = keyframes[i-1].handle_right[1] - pos_ini
            # la velocidad final sera la diferencia entre el keyframe final y la posicion del handle izquierdo
            b_fin = pos_fin - keyframes[i].handle_left[1]
            posx = bezier(u, pos_ini, b_ini, b_fin, pos_fin)

    # Se devuelve la posicion calculada

    # Si el usaurio ha activado la variacion se llama a la funcion aleatoria
    if obj.varia:
        posx += varia_posicion(frame, obj, coord)

    # se devuelve la posicion calculada
    return posx


# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# █░▄▄▀██░▄▄▄░█▄░▄██░▄▄░██░▀██░█░▄▄▀██░▄▄▀████░▄▄▀██░▄▄▀█▄░▄██░███░██░▄▄▄██░▄▄▀
# █░▀▀░██▄▄▄▀▀██░███░█▀▀██░█░█░█░▀▀░██░▀▀▄████░██░██░▀▀▄██░████░█░███░▄▄▄██░▀▀▄
# █░██░██░▀▀▀░█▀░▀██░▀▀▄██░██▄░█░██░██░██░████░▀▀░██░██░█▀░▀███▄▀▄███░▀▀▀██░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def asigna_driver_posicion(obj, coord):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('location', coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"custom_pos(frame, self, {coord})"


def asigna_driver_orientacion(obj, coord):
    obj.rotation_mode = 'QUATERNION'
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('rotation_quaternion', coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_custom_quat(frame, self, {coord})"

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░▄▄▀██░▄▄▄██░▄▄░█▄░▄██░▄▄▄░█▄▄░▄▄██░▄▄▀██░▄▄▄░
# ██░▀▀▄██░▄▄▄██░█▀▀██░███▄▄▄▀▀███░████░▀▀▄██░███░
# ██░██░██░▀▀▀██░▀▀▄█▀░▀██░▀▀▀░███░████░██░██░▀▀▀░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def register():
    # --- OBJETO

    # -- INT

    # N_COPIAS: numero de copias que se realizaran del objeto
    bpy.types.Object.n_copias = bpy.props.IntProperty(name="Nº Copias", description="numero de copias que se realizaran del objeto", min=0, default=0)
    # FREC: frecuencia usada para la aleatoriedad, determina cada cuanto cambia el valor y la velocidad a la que oscila el mismo
    bpy.types.Object.frec = bpy.props.IntProperty(name="Frecuencia", description="Frecuencia de variación de valores en varia_posicion", min=2, default=10)
    # CONT_BRUSCO: contador que sirve para llevar la cuenta de cuanto se tarda en pasar de una curva a otra para evitar cambios bruscos en la rotacion
    bpy.types.Object.cont_brusco = bpy.props.IntProperty(name="cont_brusco", description="contador de cuantos saltos hay en la curva", min=-20, max=20, default=0)

    # -- FLOAT

    # TAU: tension que se le aplicara a las velocidades en catmull-rom
    bpy.types.Object.tau = bpy.props.FloatProperty(name="Tau", description="tensión catmull-rom", min=0.0, default=1.0, update=updateMethod)
    # DESP_RAND: Valor de desplazamiento del frame 
    bpy.types.Object.desp_rand = bpy.props.FloatProperty(name="Desplazamiento", description="Float con valor del desplazamiento que se va a aplicar al frame")
    # M_MAX: amplitud del valor aleatorio desplazable
    bpy.types.Object.m_max = bpy.props.FloatProperty(name="Amplitud", description="Amplitud máxima del desplamiento posible", min=0.0, default=1.0)
    # DISTANCIA_RECORRIDA: Distancia recorrida de la recta
    bpy.types.Object.distancia_recorrida = bpy.props.FloatProperty(name="Distancia Recorrida", description="Distancia recorrida de la curva", min=0.0, default=0.0)
    # VELOCIDAD: velocidad a la que pasar por la recta
    bpy.types.Object.velocidad = bpy.props.FloatProperty(name="Velocidad", description="Velocidad a la que recorre la curva", default=1.0)
    # ROTACION_GIRO: rotacion maxima que se alcanzara al girar
    bpy.types.Object.rot_giro = bpy.props.FloatProperty(name="Rotacion_Giro", description="Rotacion maxima que se alcanzara al girar", default=-1.0)
    

    # -- COLECTION PROPERTY
    bpy.utils.register_class(MiPropertyGroup)
    bpy.types.Object.listaCurva = bpy.props.CollectionProperty(type=MiPropertyGroup, name="Lista Trayectoria", description="Lista de valores de la trayectoria")

    # -- FLOAT VECTOR

    # RAND_VAL: Vector que tiene los valores aleatorios a los que desplazarse de cada coordenada
    bpy.types.Object.rand_val = bpy.props.FloatVectorProperty(name="vector aletorio",description="vector que guarda los valores aleatorios de cada eje en un momento dado", size=3, default=(0.0,0.0,0.0))

    # -- BOOL 

    # COPIAR: Booleano que activa y desactiva las copias
    bpy.types.Object.copiar = bpy.props.BoolProperty(name="Copiar", description="habilita la posibilidad de generar copias", default=False)
    # ELIMINAR: Booleano que activa o desactiva la eliminacion de la coleccion anterior
    bpy.types.Object.eliminar = bpy.props.BoolProperty(name="Elimina copia", description="habilita la eliminacion de las copias anteriores al crear nuevas", default=False)
    # VARIA: Booleano que activa o desactiva la aleatoriedad
    bpy.types.Object.varia = bpy.props.BoolProperty(name="Variación", description="Activa la variación", default=False)
    # USARNUEVO: Booleano que activa o desactiva el uso del control de velocidad en la curva
    bpy.types.Object.usarNuevo = bpy.props.BoolProperty(name="Reparametrizar curva", description="Dicta si ha de usarse el nuevo calculo de posicion o no", default=False)
    # APLICAREPARAM: Booleano que activa o desactiva el ultimo cambio de variable para la reparametrizacion
    bpy.types.Object.aplica_reparam = bpy.props.BoolProperty(name="Reparametrizar distancias", description="Activa o desactiva la ultima reparametrizacion", default=False)
    # ADAPTAR: Booleano que activa o desactiva que la animacion adapte su tiempo 
    bpy.types.Object.adaptar = bpy.props.BoolProperty(name="Adaptar animacion", description="Activa o desactiva la adaptacion de la animacion", default=False)
    # ACTIVA_ORIENTACION: Booleano que activa o desactiva el calculo de las rotaciones para la orientacion del objeto
    bpy.types.Object.activa_orientacion = bpy.props.BoolProperty(name="Activa orientacion", description="Activa o desactiva el calculo de rotacion", default=True)

    # -- ENUM

    # METHOD: metodos de interpolacion
    bpy.types.Object.method = bpy.props.EnumProperty(
        name="Interpolacion",
        description="Interpolacion de movimiento",
        items=[
            ('Lineal', 'Lineal', 'Interpola el movimiento de forma lineal'),
            ('Hermite', 'Hermite', 'Interpola usando Hermite'), 
            ('Catmull-Rom', 'Catmull-Rom', 'Interpola usando Catmull-Rom'), 
            ('Bezier', 'Bezier', 'Interpola usando Bezier')
        ],
        update=updateMethod
    )
    # EJE_FORWARD: eje que se tomara como forward
    bpy.types.Object.eje_forward = bpy.props.EnumProperty(
        name="Orientacion",
        description="Interpolacion de movimiento",
        items=[
            ('EJE_X', 'Eje x', 'Eje x como frontal'),
            ('EJE_Y', 'Eje y', 'Eje y como frontal'), 
            ('EJE_Z', 'Eje z', 'Eje z como frontal'),
            ('EJE_-X', 'Eje -x', 'Eje -x como frontal'),
            ('EJE_-Y', 'Eje -y', 'Eje -y como frontal'),
            ('EJE_-Z', 'Eje -z', 'Eje -z como frontal')
        ]
    )
    # EJE_LATERAL: eje que se tomara como lateral
    bpy.types.Object.eje_lateral = bpy.props.EnumProperty(
        name="Equilibrio",
        description="Interpolacion de movimiento",
        items=[
            ('EJE_X', 'Eje x', 'Eje x como lateral'),
            ('EJE_Y', 'Eje y', 'Eje y como lateral'), 
            ('EJE_Z', 'Eje z', 'Eje z como lateral'),
            ('EJE_-X', 'Eje -x', 'Eje -x como lateral'),
            ('EJE_-Y', 'Eje -y', 'Eje -y como lateral'),
            ('EJE_-Z', 'Eje -z', 'Eje -z como lateral')
        ]
    )
    
    # --- SCENE

    # -- BOOL

    #Modificaciones: Booleano que activa o desactiva la individualizacion de los keyframes
    bpy.types.Scene.modificaciones = bpy.props.BoolProperty(name="Modificar individualmente", description="Permite la modificación individual de las copias", default=False)
    
    # --- OPERATORS y PANELES

    bpy.utils.register_class(MiOperador)
    bpy.utils.register_class(CopiasPanel)
    bpy.utils.register_class(AleatoriedadPanel)
    bpy.utils.register_class(InterpolacionPanel)
    bpy.utils.register_class(ControlPanel)
    bpy.utils.register_class(OrientationPanel)
    bpy.utils.register_class(Copiador)
    bpy.utils.register_class(Remap)

    # --- DRIVER
    
    bpy.app.driver_namespace['custom_pos'] = custom_pos
    bpy.app.driver_namespace['get_custom_quat'] = get_custom_quat
    

# ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
# ██░██░██░▀██░██░▄▄▀██░▄▄▄██░▄▄░█▄░▄██░▄▄▄░█▄▄░▄▄██░▄▄▄██░▄▄▀
# ██░██░██░█░█░██░▀▀▄██░▄▄▄██░█▀▀██░███▄▄▄▀▀███░████░▄▄▄██░▀▀▄
# ██▄▀▀▄██░██▄░██░██░██░▀▀▀██░▀▀▄█▀░▀██░▀▀▀░███░████░▀▀▀██░██░
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

def unregister():
    bpy.utils.unregister_class(MiOperador)
    bpy.utils.unregister_class(AleatoriedadPanel)
    bpy.utils.unregister_class(InterpolacionPanel)
    bpy.utils.unregister_class(ControlPanel)
    bpy.utils.unregister_class(OrientationPanel)
    bpy.utils.unregister_class(Copiador)
    bpy.utils.unregister_class(Remap)
    bpy.utils.unregister_class(MiPropertyGroup)

    del bpy.app.driver_namespace['custom_pos']
    del bpy.app.driver_namespace['get_custom_quat']
    del bpy.types.Object.tau
    del bpy.types.Object.n_copias
    del bpy.types.Object.copiar
    del bpy.types.Object.eliminar
    del bpy.types.Scene.modificaciones
    del bpy.types.Object.method
    del bpy.types.Object.m_max
    del bpy.types.Object.frec
    del bpy.types.Object.varia
    del bpy.types.Object.rand_val
    del bpy.types.Object.desp_rand
    del bpy.types.Object.listaCurva
    del bpy.types.Object.aplica_reparam
    del bpy.types.Object.usarNuevo
    del bpy.types.Object.distancia_recorrida
    del bpy.types.Object.velocidad
    del bpy.types.Object.adaptar
    del bpy.types.Object.activa_orientacion
    del bpy.types.Object.eje_forward
    del bpy.types.Object.eje_lateral
    del bpy.types.Object.rot_giro
    del bpy.types.Object.cont_brusco
    
if __name__ == "__main__":
    register()