import bpy
import numpy as np


def crea_copias(obj, context, copy_action):
    """ Crea varias copias de un objeto y elimina las fcurves de posición

    Devuelve: colección con las copias creadas
    """

    scene = bpy.context.scene
    n = obj.n_copias

    base_collection = scene.collection

    # En lugar de dejar los objetos nuevos directamente en la colección básica,
    # creamos una. Esto facilitará el trabajo posterior
    # Si ya existe, creará otra.
    # Puede ser interesante eliminar los objetos que se crearon la última vez
    collection_name = "Copias de "+obj.name

    # en caso de querer eliminar la coleccion anterior
    if obj.eliminar:
        # se busca denrtro de las colecciones
        for collection in context.scene.collection.children[:]:
            # se comprueba si alguna tiene el mismo nombre que la que deseamos crear
            if collection.name == collection_name:
                col = base_collection.children.get(collection_name)
                # iteramos por todos los objetos para borrarlos y que no se queden en memoria
                for object in col.objects:
                    bpy.data.objects.remove(object)
                
                # por ultimo borramos la coleccion
                bpy.data.collections.remove(col)
                

    copies_collection = bpy.data.collections.new(collection_name)
    base_collection.children.link(copies_collection)
    original_action = obj.animation_data.action

    for i in range (n):
        pass
        # Creamos una copia del objeto obj
        # Hay que añadirlo a la colección. De lo contrario no
        # lo veremos en la escena

        new_obj = obj.copy()
        # cuando se crea una nueva copia se le implementa un desplazamiento aleatorio para la hora de la variacion vayan desacompasados
        new_obj.desp_rand = np.random.random()
        copies_collection.objects.link(new_obj)
        
        # La acción (con los fotogramas clave) no se copia. Se crea
        # una referencia. Si modificamos los fotogramas clave de
        # una copia, cambiarán todos, incluído el original
        # Si no queremos que ocurra esto, copiamos la acción, creando
        # una nueva
        if copy_action:
            new_obj.animation_data.action = original_action.copy()
        #
    #

    return copies_collection
#

if __name__ == "__main__":

    obj_a_copiar = bpy.context.object
    obj_a_copiar.n_copias = 2

    # Cuando lo llamemos desde un operador, le pasamos el context
    # que recibe el método invoke/execute
    crea_copias(obj_a_copiar,bpy.context)

#
