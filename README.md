# Práctica 1: Web Scraping

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de la web _todostuslibros_ y generar un _dataset_ que contenga información sobre los libros más vendidos en la actualidad.

## Miembros del equipo

La actividad ha sido realizada por **Marta Coll Pol** y **Manuel de Blas Pino**.

## Ficheros del código fuente

src/main.py - Fichero que lee los parámetros de entrada y ejecuta un web scraping, rapido y simple, lento pero completo y descarga las imagenes de las portadas de los libros, en función de los parámetros de entrada utilizados.

src/scraper.py - Fichero que contiene la clase _FastBookScraper_ donde se definen los métodos que permiten realizar un Web Scraping rápido (~2 min), generar y guardar un conjunto de datos que contiene la información más relevante sobre los libros más vendidos y descargar las imagenes de las portadas de los libros.

src/scrape_each_book.py - Fichero que contiene la clase _BookScraper_ donde se definen los métodos que permiten realizar un Web Scraping exhaustivo, y por lo tanto más lento (~20 min), generar y gurardar un conjunto de datos con toda la información disponible sobre los libros más vendidos y descargar las imagenes de las portadas de los libros.

## Set-up:

El proyecto se ha realizado usando Python 3.10.3.

En cuanto a las librerias utilizadas, se pueden encontrar en el archivo requirements.txt, y podemos instalarlas con el siguiente comando:

`pip3 install -r requirements.txt`

## Uso:

### Parametros:
Disponemos de tres parámetros posibles de entrada:

-f o --fast : De ser _TRUE_, utiliza la versión rápida para realizar el Web Scraping, que obtiene un conjunto de datos con la información más relevante de los libros más vendidos en la actualidad. De ser _FALSE_, se utiliza la versión lenta que genera un conjunto de datos más completo. Por defecto es igual a _TRUE_.

-o o --output_filepath : Se utiliza para indicar el path hacia el fichero de salida del conjunto de datos. Por defecto tiene un valor de _output/Bestsellers.csv_.

-d o --download: Se utiliza para indicar el path de la carpeta donde se almacenaran las imagenes de las portadas de los libros. Si esta opción se deja vacia "", no se descargaran las imagenes. Si se proporciona un directorio donde almacenar las imagenes, estas se descargaran y su nombre corresponderá al ID que identifica el libro en el conjunto de datos. El valor por defecto es vacío, por lo que no se descargaran las imagenes a menos que se proporcione el Path a un directorio. 


### Ejemplo de ejecución:

Para ejecutar el programa se usa el siguiente comando:

`python3 main.py -f TRUE -o output_filepath -d output_folder`

O de forma equivalente:

`python3 main.py --fast TRUE --output_filepath output_filepath --download output_folder`

## Recursos

Para resolver dudas puntuales de programación se ha usado la conocida plataforma Stack Overflow.
En cuanto a dudas más concretas sobre Web Scraping, nos hemos basado en los recursos proporcionados por la asignatura.
