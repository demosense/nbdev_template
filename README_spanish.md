# Proyecto de analítica con NBDEV

Este repositorio está enfocado a mostrar cómo funciona un proyecto de analítica utilizado la herramienta de _nbdev_ y a enseñar cómo crear un proyecto desde cero. Para ello, se explicará para qué sirve _nbdev_ y qué ventajas nos ofrece y se mostrará cómo utilizar en un proyecto de analítica.

Detallar que esta forma de trabajar con _nbdev_ en proyectos de analítica es una metodología propia de Taidy Cloud probada y validada en mulitud de proyectos centrados en datos.

## Introducción

`nbdev` es una librería que permite desarrollar una librería/paquete o un proyecto de Python utilizando únicmanete [Jupyter Notebooks](https://jupyter.org/). Nos permite tener todo el código, tests y documentación en un mismo lugar tan solo trabajando sobre los notebooks.

_**Nota:** la librería ha sido testeada en los sistemas operativos de macOS y Linux, pero no ha sido testeada en Windows y es posible que no todas las funciones funcionen correctamente._

### **Características principales de Nbdev**

- **Generación automática de documentación** desde los Jupyter notebooks. Esta documentación se genera con un buscador inteligente y se vincula automáticamente con hipervínculos las diferentes páginas y secciones de la documentación que hacen que sea fácil de navegar.

- Funcionalidades para **publicar automáticamente paquetes de python en pypi y conda** incluyendo la gestión del versionado de los paquetes.

- Sólida **sincronización bidireccional entre los notebooks y el código fuente**, que permite usar un IDE para navegar por el código o realizar ediciones rápidas sin problemas. Desarrollando solamente en los notebooks y atomáticamente se sincronizarán con el código fuente del paquete que se cree.

- **Control para ocultar/mostrar celdas en la documentación**: puedes optar por ocultar celdas enteras, solo la salida o solo la entrada.

- Capacidad para **escribir tests directamente en notebooks** sin tener que aprender APIs especiales. Estos tests se ejecutan en paralelo con un solo comando CLI. Incluso se puede definir ciertos grupos de tests para que no se tengan que ejecutar siempre pruebas de ejecución prolongada.

- Herramientas para **combinar/resolver conflictos** con notebooks en un **formato legible por humanos**.

- Crea módulos de Python siguiendo **mejores prácticas, como definir automáticamente `__all__`** ([más detalles](http://xion.io/post/code/python-all-wild-imports.html)) con funciones, clases y variables exportadas.

- Compatibilidad con **ecuaciones matemáticas con LaTeX**.

## Creación de un proyecto nuevo

Para crear un proyecto nuevo lo primero que tenemos que hacer es clonar un repositorio de GitHub, el cual es una plantilla de un proyecto de analítica que tiene integrado _nbdev_, este repositorio es el punto de partida para empezar un nuevo proyecto. Puedes clonar este [repositorio](https://github.com/demosense/nbdev_template) o puedes hacer click aquí: [nbdev template](https://github.com/demosense/nbdev_template/generate). Este repositorio es un _fork_ realizado por Taidy Cloud desde el repositorio original de _nbdev_, en el que se incluyen algunas mejoras para trabajar de forma más cómoda.

_**Nota:** el nombre que le establezcas al repositorio que clones será el nombre del paquete de Python que se generará por nbdev. Por esta razón, es una buena ideá escoger un nombre corto, todo en minúsculas y sin guiones entre palabras (se permiten guiones bajos)._

### Estructura del proyecto con nbdev

Cuando clones el respositorio, verás multitud de ficheros y carpetas de configuración. Los ficheros y carpetas más importantes son las siguientes:

- `settings.ini`: este fichero contiene la información sobre el paquete que se creará, fuera de la configuración específica durante el desarrollo, puede modificar solo estos campos:
  - `versión` valor cuando hagamos _releases_ del paquete
  - `lib_name` el nombre del paquete
  - `usuario` el nombre del usuario de GitHub/GitLab
  - `descripción` una breve descripción del paquete
  - `palabras clave` algunas palabras clave
  - `autor` el nombre del usuario que administra el paquete
  - `author_email` el correo que quien gestiona el paquete
  - `copyright` su nombre o el nombre de la empresa que gestiona el paquete
  - `branch` la rama predeterminada de su repositorio (generalmente `master` o `main`)
  - `requirements` el archivo donde están todas las dependencias (`requirements.txt` por defecto)
  - `nbs_path` carpeta que contiene los notebooks de Jupyter (`src` por defecto)
- `docs`: carpeta que contendrá la documentación generada automáticamente.
- `src`: esta carpeta será el directorio principal que contendrá los notebooks de Jupyter que luego se transformarán en un paquete de python dentro de una carpeta con el mismo nombre de la librería `<lib_name>`. Esta carpeta `src` contiene 4 archivos _.py_ predeterminados que se usarán en cualquier proyecto:
  - _`index.py`:_ documentación usada para crear el README del proyecto.
  - _`paths.py`:_ contiene las direcciones/rutas del datalake que apuntan a cada uno de los datasets o activos a utilizar en las ETLs.
  - _`elt_scripts.py`_: todas las ETLs desarrolladas estará aquí. Estas importan los paquetes correspondientes y orquestan la carga, ejecución y serialización de la transformación de datos.
  - _`utils.py`_: funciones comunes y útiles compartidas con todo el proyecto. \*_Contiene scripts útiles para interactuar con sistemas de archivos y otros aspectos misceláneos del código_.\*
- `build.sh`: un script de Shell que recopila los comandos de desarrollo necesarios para crear y desarrollar un proyecto. Comandos como ejecutar una ETL manualmente, lanzar una nueva versión del paquete, construir el módulo del proyecto, etc. Todos los comandos se detallan más adelante.
- `requirements.txt`: las dependencias de python necesarias en el proyecto. Incluir aquí todas las dependencias de python que necesite.
- `requirements-dev.txt`: las dependencias de python necesarias para desarrollar el proyecto. Incluir aquí todas las dependencias de python que necesite.

### Cambios y modificaciones de Taidy Cloud

El equipo de Taidy ha anañdido 2 nuevas características principales al repositorio de plantillas de _nbdev_ para trabajar más cómodamente:

- _`jupytext`:_ una extensión para Jupyter que permite convertir notebooks en ficheros de Python (.py) de forma sencilla. De esta forma, los notebooks no son necesarios de incluir en los commits del repositorio para evitar conflitos con el versionado del código. Solo se trabaja con ficheros .py autogenerados desde los notebooks usando la librería de _jupytext_.<br><br>

  Jupytext automáticamente convierte el código de los notebooks en ficheros _.py_, así que lo único que debe de preocuparnos es registrar en _jupytext_ un nuevo notebook cuando lo creamos ejecutando el siguiente comando `./build.sh pair-notebooks` en una terminal.<br><br>

  Otro punto que debemos saber es cómo converter los ficheros _.py_, solo usa el comando `./build.sh sync-notebooks` y todos los ficheros _.py_ en la carpeta `src` serán convertido en notebooks (si el norebooks existe, éste es actualizado). Esto es perfecto para compartir el trabajo realizado con nuestro equipo y compañeros de trabajo del proyecto.<br><br>

- `build.sh`: este es el script princiapl para desarrollar el proyecto. Con este script puedes ejecutar los siguientes comandos::
  - `./build.sh build` para generar todo el paquete de python del proyecto.
  - `./build.sh pair-notebooks` para registrar un nuevo notebook en _jupytext_.
  - `./build.sh sync-notebooks` para sincronizar o crear los notebooks desde los ficheros _.py_.
  - `./build.sh run --name <etl_name>` para ejecutar cualquier ETL de forma manual.
    <span style="color: red;">
  - `AWS_PROFILE=<aws profile> ./build.sh release` to release a new version of the package into cloud (AWS).
    </span>

## Puesta en marcha del proyecto

Después de clonar el respositorio de _nbdev_ como se ha detallado arriba, estos son los pasos a seguir:

1. **Configuración**: configurar algunos ficheros del proyecto:

   1. En el fichero `settings.ini` modificar los campos que están entre llaves, e.g: `{lib_name}`
   2. En el fichero `build.sh` modificar todos los `<lib_name>` que aparezcan con el valor que se ha usado en `settings.ini` para el campo `lib_name`
   3. En el fichero `.gitignore` modificar `{lib_name}` por el valor que se ha usado en `settings.ini` en el campo `lib_name`
   4. En el fichero `docs/sidebar.json` modificar `{lib_name}` por el valor que se ha usado en `settings.ini` en el campo `lib_name`

2. **Entorno Virtual de Python**: Crear un _venv_ para trabajar de forma aislada en un entorno virual de python:

```bash
python3 -m venv venv
```

3. **Dependencias**: Activa el _venv_ y instala todas las dependencias del proyecto. Incluye todas las dependencia en los ficheros _requirements.txt_ y _requirements-dev.txt_ sin son solo depeendencia para el desarrollo y no para el proyecto:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

_**Nota**: como has podido observar en el fichero requirements-dev.txt están los paquetes de python básicos para empezar a trabajar, estos son `nbdev` , `jupyterlab` y `jupytext` ._

4. **Sincronizar notebooks**: Sincronizar/crear desde los ficheros que hay en `src/_.py_` los notebooks. Como los notebooks no están incluidos en los commits del repositorio para evitar conflictos, estos se deben crear al principipio desde los ficheros _.py_. Solo se trabaja con archivos _.py_ generados automáticamente desde los notebooks usando la librería _jupytext_. Después de ejecutar el siguente comando, podrás ver en la carpeta `src` los notebooks relacionados con `index.py`, `paths.py`, `etl_scripts.py` y `utils.py`, en estos notebooks verás `{ lib_name}` donde se usa el paquete, cámbialo con el `lib_name` establecido en `settings.ini`.

```bash
./build.sh sync-notebooks
```

5. **Generar módulos y paquete**: para crear el paquete de python del proyecto usa el siguiente comando en una terminal en cualquier lugar dentro de la carpeta del proyecto. Cuando ejecutes el comando veras una nueva carpeta con el nombre de `lib_name` con todo el código de tu paquete de Python generado desde los notebooks que están en la carpeta de `src`.

```bash
./build.sh build
```

6. **Instala el paquete en local**: como hemos cambiado los notebooks de la carpeta `src`, para usar el paquete en local, debes instalarlo en tu máquina/entorno en local. Para ello, instala el paquete en modo editable, esto permitirá usar `importar <lib_name>` en cualqueir notebook para importar dependencias de otros notebooks. Al instalarlo en modo editable, este comando solo tendrás que ejecutarlo al principio, y cuando se cambie el código de los notebooks estos se detectarán automáticamente. Ejecuta el siguiente comando en la raíz del proyecto:

```bash
python -m pip install -e .
```

## Como trabajar en los notebooks y Nbdev

Usamos _nbdev_ para transladar código implementado en los notebooks a ficheros _.py_, crear atomáticamente documentación y crear la estructura de un paquete de python instalable. Esto se hace solamente **usando comentarios específicos en la primera línea de las celdas de los notebooks**. Están disponibles los siguientes comentarios:

### **default_exp**

Usa el comentario `# default_exp`en la primera celda de los notebooks para decirle a nbdev la ruta del módulo que se generará a partir del código que se escriba en ese notebook

### **export**

Usa el comentario `# export` en una celda para incluir el código de esta celda en el módulo que se generará. El código exportado también se incluye en la lista de `__all__`. Esto se utiliza para funciones ETL (i.e.: `get_bronze_something`).

### **exporti**

Usa el comentario `# exporti` en una celda para incluir el código de esta celda en el módulo que se generará. Este es usado para constantes u otras funciones internas/auxiliares (i.e.: `default_unit = "kW"`).

### **hide**

Usa el comentario `# hide` en una celda para ignorar esta celda. Esto generalmente se usa para celdas que cargan datos de ejemplo para probar la funcionalidad del cuaderno.

### **hide_input**

Usa el comentario `# hide_input` en una celda para generar la documentación sin mostrar el código de la celda pero renderizando la salida.

## Desarrollo

### **Crear un notebook nuevo**

Cada vez que creemos un notebook nuevo tenemos que realizar las siguientes acciones:

1. Sincronizar el notebook con un fichero _.py_ usando jupytext:

`./build.sh pair-notebooks`

2. Usar git para añadir el fichero _.py_. (Notebooks (ficheros .ipynb) son ignorados por git).

### **Crear el paquete de python**

Usa el comando `./build.sh build` o `nbdev_build_lib` para generar el paqeute de python del proyecto, ejecuta el comando en una terminal en la raiz del proyecto. Luego podrás abrir un intérprete de python y usar `import <lib_name>` para probar el código implementado.

### **Crear la documentación**

_nbdev_ genera una web estática utilizando los notebooks. Usa el comando `make docs_serve` para generar la documentación desde los notebooks y servir un servidor web para ver la documentación.

El _sidebar_ lateral ubicado en el lado izquierdo se crea a partir de `docs/sidebar.json`. Si desea que aparezcan páginas html creadas a partir de nuevos notebooks, debe editar este archivo **antes** de ejecutar `make docs_serve`. Es un archivo json con una sola clave, nombre `{libname}`_,_ y como valor otro json, cuyas claves son el texto en la barra lateral (índices) y los valores son rutas a archivos html autogenerados dentro de la carpeta `docs` (use rutas relativas a la carpeta `docs`). Además, si desea usar índices contraíbles, puede usar una clave vacía (índice) y como valor un json como si fuera la estructura básica nuevamente. Por ejemplo:

```jsx
{
  "{libname}": {
    "Overview": "/",
    "": {
      "raw": {
        "Raw 1": "raw_1.html",
        "Raw 2": "raw_2.html"
      },
      "bronze": {
        "Bronze 1": "bronze_1.html",
        "Bronze 2": "bronze_2.html"
      }
    }
  }
}
```

### Establecer la ruta de los datos

Podemos usar una variable de entorno `DATA_PATH` para controlar dónde se encuentran los datos (carpeta raíz). Tenemos que definirlo cuando estamos trabajando en el cuaderno antes de iniciar jupyterlab, por ejemplo: `DATA_PATH=<path_to_data> python -m jupyterlab` y tenemos que definirlo cuando ejecutamos un ETL, por ejemplo: `DATA_PATH=<path_to_data> . /build.sh ejecutar --name <nombre_etl>`

<span style="color: red;">
### **Releases**

The package is published to a private pypi repository in AWS CodeArtifact service. Each time we want to make a new release we need to do the following steps.

### **Repository creation on AWS (just once)**

The repository must be created in the AWS account. The steps to do that are:

1. Go to AWS CodeArtifact service (use the Console)
2. Create a domain:
   - Name: `{lib_name}`
3. Create a repository:
   - Name: `{lib_name}`
   - Public upstream repositories: select pypi-store
   - Select the `{lib_name}` domain (it is this aws account)
   - Create repository
4. Optionally edit the domain and repository policies to allow access for every AWS account of interest (crossaccount):
   1. Domain policy:

```jsx
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ContributorPolicy",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::XXXXXXXXXXXX:root",
                ]
            },
            "Action": [
                "codeartifact:DescribeDomain",
                "codeartifact:GetAuthorizationToken",
                "codeartifact:GetDomainPermissionsPolicy",
                "codeartifact:ListRepositoriesInDomain",
                "sts:GetServiceBearerToken"
            ],
            "Resource": "*"
        }
    ]
}
```

b. Repository policy:

```jsx
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::XXXXXXXXXXXX:root",
                ]
            },
            "Action": [
                "codeartifact:DescribePackageVersion",
                "codeartifact:DescribeRepository",
                "codeartifact:GetPackageVersionReadme",
                "codeartifact:GetRepositoryEndpoint",
                "codeartifact:ListPackageVersionAssets",
                "codeartifact:ListPackageVersionDependencies",
                "codeartifact:ListPackageVersions",
                "codeartifact:ListPackages",
                "codeartifact:ReadFromRepository"
            ],
            "Resource": "*"
        }
    ]
}
```

### **New release**

1. Edit file `settings.ini` and bump version field using [semantic versioning](https://semver.org/).
2. There are two modes:
   1. Manual: run the command `AWS_PROFILE=<aws profile> ./build.sh release`. This will upload the package to CodeArtifact in the account determined by `<aws profile>`.
   2. Automatic: Commit and push. Once the commit is in origin master, CI/CD will make the release to CodeArtifact. In this case you need to configure a proper CI/CD environment to run the manual command described before.

## External documentation and useful links

### NBDEV Official page

[Welcome to nbdev](https://nbdev.fast.ai/)

### NBDEV GitHub

[https://github.com/fastai/nbdev](https://github.com/fastai/nbdev)
</span>
