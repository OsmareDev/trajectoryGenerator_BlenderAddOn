# Fase 3
 
La fase 3 consiste en la adaptación de la orientación de nuestro objeto a la curva, Para ello calcularemos diferentes cuaterniones usando las diferentes funciones de interpolación y las fórmulas vistas en clase consiguiendo así que nuestro objeto gire mirando a la curva y también se incline siguiéndola.
 
 
## Utilización de la herramienta
<br>
 
_Ventana del addon_
 
![Vetana Addon](https://cdn.discordapp.com/attachments/651843244761808906/935250851382034493/unknown.png)
<br><br>
 
### Control de la orientación
En esta sección se encuentra todo lo relacionado con la tercera fase.
 
#### 1 - Activa orientación ( Checkbox )
Este parámetro nos permite activar la orientación para el objeto
* True (Checked): Se quiere usar el uso de la orientación
* False (Unchecked): No se quiere usar el uso de la orientación
 
#### 2 - Orientación ( Enum )
Este parámetro nos permite seleccionar el vector frontal de nuestro objeto entre los diferentes ejes
* Eje x
* Eje y
* Eje z
* Eje -x
* Eje -y
* Eje -z
 
#### 3 - Equilibrio ( Enum )
Este parametro nos permite seleccionar el vector lateral de nuestro objeto entre los diferentes ejes
* Eje x
* Eje y
* Eje z
* Eje -x
* Eje -y
* Eje -z
 
#### 4 - Rotación Giro ( Float )
Este parámetro nos permite seleccionar cuánto cómo de máximo se inclinara el objeto a la hora de girar
 
## Método de uso
 
<hr>
 
Una vez tenemos el objeto con los keyframes y la curva que deseamos reparametrizar activaremos el primer checkbox, luego simplemente seleccionamos el eje frontal y el eje lateral y la rotacion maxima de alabeo
