# chatgpt-python

![about-chatgpt-python](https://user-images.githubusercontent.com/6242827/224505890-7ddd267f-a6f5-4743-93a8-9ac0a70b70b9.png)

Una aplicación para chatear con ChatGPT creada con Python.

## Una breve explicación de qué hace este código

Este código es una aplicación ChatGPT creada con Python que utiliza la API de OpenAI para generar respuestas a preguntas escritas por los usuarios. A continuación, se describen las funciones principales del código:

![chatgpt-funcionando](https://user-images.githubusercontent.com/6242827/224506011-7b549d51-2993-4210-98fb-0439d6fbbae3.png)

- La biblioteca openai se importa para establecer la conexión con la API de OpenAI.
- La biblioteca typer se importa para permitir que el usuario escriba su pregunta en la terminal y se recoja como una entrada.
- La biblioteca webbrowser se importa para abrir el navegador web si el usuario selecciona la opción de búsqueda directa.
- La biblioteca rich se importa para mejorar la visualización de los mensajes en la terminal.
- La biblioteca smtplib y email.mime se importan para permitir el envío de correos electrónicos directamente desde la aplicación.
- La función export_conversation() se utiliza para guardar la conversación en un archivo de texto llamado "conversacion.txt".
- La función show_history() se utiliza para mostrar el historial de mensajes previos.
- La función send_email() se utiliza para enviar correos electrónicos a una dirección de correo electrónico especificada. Aun que esto dependerá tambień de la con figuración del servidor que utilicemos para enviar los correos.
- La función generate_prompt() se utiliza para generar el prompt que se enviará a la API de OpenAI.
- La función principal main() se ejecuta mientras el usuario no escriba "exit". En esta función, se muestra una tabla de comandos disponibles, se inicia la conversación con un mensaje del sistema, se recopila la entrada del usuario, se envía la solicitud a OpenAI, se procesa la respuesta y se muestran los resultados. Además, también se incluyen comandos para crear una nueva conversación, eliminar los mensajes de la conversación de la pantalla, exportar la conversación actual a un archivo de texto, enviar un correo electrónico, buscar directamente en Google y mostrar el historial de mensajes previos.

En resumen, este código es una aplicación de chatbot que utiliza la tecnología de OpenAI para generar respuestas a preguntas escritas por los usuarios en la terminal.
