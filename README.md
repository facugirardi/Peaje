# Sistema de Peaje

[Introduccion](#introduccion)

[Instalacion](#instalacion)

[Diagrama Entidad-Relacion](#diagrama-entidad-relacion-del-sistema)



## Introduccion
Es un sistema de gestor y control de peaje. El objetivo principal del proyecto es administrar eficientemente la recaudación de peajes en cada estación todas las rutas de la provinvia de cordoba.


## Instalacion

### Requisitos previos

Debes tener python instalado:

*input:*
```bash
    python --version
```

*output:*
```bash
    Python <numeroVersion>
```
<hr>

Debes tener algun gestor de entornos virtuales instalado, en este caso, nosotros utilizamos *__pipenv__*

*input:*
```bash
    pipenv --version
```

*output:*
```bash
    pipenv, version <numeroVersion>
```

<hr>

#### Primer paso: Creacion Entorno Virtual

Va a ser muy importante trabajar con entornos virtuales ya que nos ayudará a evitar problemas relacionados con dependencias de bibliotecas y paquetes.

```bash
    pipenv install //Creacion
    pipenv shell //Ejecucion
```

#### Segundo paso: Instalacion de los modulos requeridos para su ejecucion

Una vez que estamos dentro del entorno virtual, debemos instalar todos los paquetes que se necesitaran para desarrollar/ejecutar el proyecto

```bash
    pipenv install -r requirements.txt
```

>Una vez hayas seguido estos pasos, podrás ejecutar y/o trabajar en el proyecto sin ningún problema.

## Diagrama Entidad-Relacion del sistema
![Imagen Diagrama Entidad-Relacion](doc/imagenDiagrama.png)

