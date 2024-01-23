# Fase 2
 
La fase 2 consiste en la reparametrizacion de la curva interpolada para poder tener un mejor control de la velocidad. Para ello la recorremos entera guardándose en una tabla que nos servirá para realizar el cambio de parámetro. Con el nuevo parámetro podremos recorrer la curva a velocidad constante. Podremos seleccionar un segundo cambio de parámetro para poder seleccionar en qué punto y cuando estamos de la curva añadiendo keyframes de distancia al objeto.
 
 
## Utilización de la herramienta
<br>
 
_Ventana del addon_
 
![Vetana Addon](https://cdn.discordapp.com/attachments/651843244761808906/935234193573695568/unknown.png)
<br><br>
 
### Control de la velocidad
En esta sección se encuentra todo lo relacionado con la segunda fase.
 
#### 1 - Parametrización de la curva ( Checkbox )
Este parámetro nos permite seleccionar si queremos hacer uso del cambio de parámetro a velocidad o no
* True (Checked): Se quiere usar el cambio de parámetro a velocidad
* False (Unchecked): No se quiere usar el cambio de parámetro
 
#### 2 - Parametrización distancias ( Checkbox )
Este parámetro nos permite hacer el segundo cambio de parámetro y usar los keyframes de distancia
* True (Checked): Se quiere usar el cambio de parámetro a distancia
* False (Unchecked): No se quiere usar el segundo cambio de parámetro
 
#### 3 - Velocidad ( Float )
Este parámetro nos permite seleccionar la velocidad a la que va a recorrer la curva, en caso de que esté seleccionado el segundo cambio de parámetro este parámetro desaparecerá
 
#### 4 - Adaptar animacion ( Checkbox )
Este parametro nos permite adaptar los frames de la timeline al frame justo donde acaba de recorrer la curva
* True (Checked): Se quiere adaptar la timeline automáticamente
* False (Unchecked): No se quiere adaptar la timeline automáticamente
 
#### 5 - Update table ( Operator )
Este botón se encarga de forzar la actualización de la tabla de valores de la curva por si fallara la actualización automática al cambiar los parámetros de la misma
 
## Método de uso
 
<hr>
 
Una vez tenemos el objeto con los keyframes y la curva que deseamos reparametrizar activaremos el primer checkbox, luego seleccionamos la velocidad a la que queremos recorrer la curva, luego seleccionamos si deseamos adaptar la animación al recorrido de la curva o si queremos reparametrizar a distancias, en ese caso seleccionamos el checkbox de adaptar animación, y luego desde la pestaña de graph editor y incluimos keyframes de distancia y modificamos dicho parámetro
