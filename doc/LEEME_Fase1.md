# Fase 1 

## Utilizacion de la herramienta
<br>

_Ventana del addon_

![Vetana Addon](https://cdn.discordapp.com/attachments/651843244761808906/901885356981489744/unknown.png) 
<br><br>

### Sección Creación de copias
En esta sección se encuentra todo lo relacionado con las copias, la creacion de un numero en especifico, modificacion individual de las copias, etc.

#### 1 - Copiar ( Checkbox ) 
Este parámetro nos permite cambiar si queremos crear.
* True (Checked): Se quiere crear una copia. Con esta opción marcada aparacerán los campos relacionados con la creación de copias.
* False (Unchecked): No se quiere crear una copia. Se ocultan los campos de creación de copias.
#### 2 - Nº Copias ( Integer ) 
Este parametro controla el número de copias que se van a generar una vez se presione el boton de generar copias.
Es importante recalcar varios puntos importantes:

* Si hay varios objetos seleccionados solo se creará copia de que esté activo (_El último seleccionado_).
* Introducir 0 equivale a borrar todas las copias con el checkbox de _Elimina copia_ equivale a borrar todas las copias.

#### 3 - Modificar individualemente ( Checkbox ) 
Este parámetro nos permite cambiar si queremos crear los nuevos objetos **por referencia** o **por valor**.
* True (Checked): Crear una copia al original que nos permita cambiar todos los valores de los objetos al mismo tiempo, perdiendo la posibilidad de modificar individualmente (_por referencia_).
* False (Unchecked): Crear copias con atributos/propiedades individuales para cada objeto (_por copia_).

#### 4 - Eliminar copia ( Checkbox ) 
Este parámetro controla si se eliminan las copias ya existentes al crear nuevas copias.
* True (Checked): Elimina todos los objetos de la colección de copias junto con la propia colección.
* False (Unchecked): Se añaden los objetos a la colección de copias sin eliminar las existentes, en caso de no existir esta colección la crea.

#### 5 - Generar copias ( Operator ) 
Lanza el invoke del operador _Copiador_ ejecutando el codigo que se encarga de crear las copias del objeto original segun los parámetros descritos anteriormente.

<br>

### Sección Aleatoriedad
En esta seccion se encuentra todo lo relacionado con la aleatoriedad de los objetos

#### 1 - Variacion ( Check-box )
Este parametro nos permite activar o desactivar la aleatoriedad añadida a la interpolacion

#### 2 - Amplitud ( Float )
Este parametro nos permite seleccionar cuanto desplazamiento maximo puede realizar esta variacion aleatoria

#### 3 -Frecuencia ( Integer )
Este parametro nos permite seleccionar cada cuanto cambiara el valor aleatorio y cuanto tardara en realizar una vuelta el mismo

<br>

### Sección Interpolación
En esta seccion se encuentra todo lo relacionado con la interpolacion y los drivers

#### 1 - Method ( Enum )
Este parametro nos permite elegir dentro de una lista controlada cual de los metodos de interpolacion queremos utilizar

#### 2 - Interpolar ( Operator )
Lanza el invoke que realiza la instalacion de los drivers en las coordenadas

<br>
<hr>

## Metodo de uso

<hr>

Una vez instalado el addon se debe antes que nada ir a la pestaña interpolacion bajo la pestaña view. Aqui y una vez seleccionado el objeto que deseamos interpolar le daremos al boton para instalar los drivers.
Tras esto ya podemos hacer uso completo de la herramienta cambiar el metodo hara que cambie en tiempo real la interpolacion, seleccionamos la variacion que deseamos y tras esto deberemos hacer las copias por este orden.
En caso contrario deberemos seleccionar eliminar en la parte de las copias y una vez elegida la variacion darle de nuevo a generar copias, cada vez que se desee cambiar la variacion o la interpolacion de las copias se deberan volver a generar para mayor velocidad.