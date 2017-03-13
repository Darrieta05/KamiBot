# KamiBot
API Bot that responds and learns commands.

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
  
