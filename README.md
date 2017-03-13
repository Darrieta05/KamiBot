# KamiBot
Kami es un Bot que muestra, ejecuta, aprende comandos guardados en una base de datos Mongo en la nube

Funciona mediante un micro-framework Flask que usa Python como lenguaje de programación.
El API funciona dependiendo de las solicitudes que se realizan a las rutas definidas por el servidor y los métodos HTTP que se realizan en dichas solicitudes.

La lista de comandos disponibles está almacenada en la Nube utilizando el servicio MLab. Se guardan en una base de datos Mongo sin esquema definido, lo cual permite guardar el documento JSON de manera más simple y dejando la lógica al servidor.

La base de datos está diseñada para almacenar documentos JSON, que contienen datos establecidos:
- name: Es el nombre del comando, el cual se va a utilizar de nuevo cuando se vaya a ejecutar el comando mediante un método POST
- doc: Se refiere a la documentación del comando, explica de manera breve la funcionalidad del comando y supone los datos que deberá enviar como parámetros
- code: Almacena el código python que se ejecutará a la hora de la solicitud POST, este deberá incluir a su vez varias variables establecidas para que funcione correctamente:
 - llenar la variable "Resultado" con los datos que deberá devolver el comando para que puedan ser enviados en formato JSON
 - el código no puede aceptar más de 3 variables.
 - cada variable deberá nombrarse "parametro#" cambiando el # por el número de la variable, esto para que sean reemplazadas a la hora de ser ejectutadas.
 - cada sentencia de código python deberá empezar con \n para que a la hora de ejecutarse se leea un salto de línea y por consiguiente otra sentencia de código.





# Ejecución del servicio
Para ejecutar el programa se deben realizar varios comandos:

- Activar el entorno virtual: es la carpeta /venv mediante el comando
  $ . venv/bin/activate

- Ejecutar el kamibot.py mediante el comando
  venv/kamibot/kamibot$ python kamibot.py

  Se cargará el servidor en localhost donde realizaremos las consultas mediante el programa Postman

# Manual de uso
## Inicio
 la ruta de inicio es localhost:5000/api
  Esta ruta muestra un mensaje de bienvenida y los comandos utilizables por el usuario:

  >Hola, mi nombre es Kami

   >para acceder a mi lista de comandos ingresa a  /api/comandos

   >para ejecutar un comando ingresa a  /api/ejecuta

   >para agregar un comando nuevo ingresa a /api/agrega

   >para acceder al Log File ingresa a /api/log

## Comandos

  la ruta /api/comandos permite acceder a una lista en formato JSON de todos los comandos con su nombre y su documentación.

## Ejecuta

  la ruta /api/ejecuta/ recibe una variable "nombre" justo después de la ruta, esta variable se remplaza por el nombre del comando que se debe ejecutar. Esta ruta funciona unicamente mediante método POST

  los comandos usualmente reciben parámetros. el "key" de estos parámetros es:

  >parametro1

  >parametro2

  >parametro3

  si se envía más de un parámetro el comando funcionará de manera usual. Si falta un parámetro en la solicitud, el comando mostrará un error y se deberá realizar la solicitud nuevamente con la cantidad de comandos correcta.

  no se deberán enviar parámetros con "value" vacío porque devolverá un error.

  *NOTA! si el comando no está hecho para recibir parámetros, igualmente se ingresa el parámetro1 con valor de 1 para que se de el funcionamiento correcto, de lo contrario se enviará un mensaje de error*

## Agrega

  la ruta /api/agrega funciona mediante un método POST unicamente. La ruta no involucra el envío de parámetros.

  Funciona unicamente si se envía un elemento JSON con las siguientes características:

  {
   "nombre": "(nombre del comando)",
   "doc": "(documentacion acerca del funcionamiento del comando y sus parámetros)",
   "codigo": "(código python debidamente identado según la documentación anterior)"
  }

  si el código es aceptado correctamente por el server entonces devolverá el objeto JSON con la informacíon que ingresó menos la parte del código la cual permanecerá oculta

## Borra

  Elimina el comando mediante la ruta /api/borrar/(nombre del comando) utilizando un método DELETE

## Actualiza

  Funciona mediante la ruta /api/actualiza/(nombre del comando)

  Utiliza método GET o POST

  recibe dos parámetros:
  - el primero es el nombre del campo que vas a actualizar
  - el segundo es el valor nuevo del campo a actualzar.
