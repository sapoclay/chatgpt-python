import openai #necesario para conectar con openai
import typer
import webbrowser # Necesario para abrir el navegador web
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de la consola
console = Console()

# Configuración de la API de OpenAI
openai.api_key = "XXXXXXXXXXXXXXXXXXXX" # La API Key se genera en https://openai.com/api
model_engine = "text-davinci-002" # El motor que vamos a utilizar

# Función para guardar la conversación en el archivo conversacion.txt, machacando el contenido anterior
def export_conversation(messages):
    with open("conversacion.txt", "w") as file:
        for message in messages:
            file.write(f"{message['role']}: {message['content']}\n")

# Función para mostrar el historial de mensajes
def show_history(messages):
    console.print("📜 Historial de mensajes:\n")
    for message in messages:
        if message["role"] == "user":
            console.print(f"{message['content']}\n")

# Función para enviar correos electrónicos
def send_email(to_address, subject, body):
    from_address = 'XXXXXX@gmail.com' # reemplazar con tu dirección de correo electrónico
    password = 'XXXXXXX' # reemplazar con tu contraseña
    smtp_server = 'smtp.gmail.com' # reemplazar con tu servidor SMTP saliente
    smtp_port = 587 # reemplazar con el puerto SMTP saliente que utiliza tu proveedor de correo electrónico

    # Crear el objeto MIME
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    # Agregar el cuerpo del correo electrónico
    message.attach(MIMEText(body, 'plain'))

    # Establecer la conexión con el servidor SMTP
    smtp_server = smtplib.SMTP(smtp_server, smtp_port)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(from_address, password)

    # Enviar el correo electrónico
    smtp_server.sendmail(from_address, to_address, message.as_string())

    # Cerrar la conexión
    smtp_server.quit()

    console.print(f"📧 El correo electrónico ha sido enviado a {to_address} 📧\n")

# Función para generar el prompt que se enviará a OpenAI
def generate_prompt(messages):
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            prompt += message["content"] + "\n"
        elif message["role"] == "user":
            prompt += f"Usuario: {message['content']}\n"
        else:
            prompt += f"{message['content']}\n"
    return prompt

# Función principal
def main():

    # Se imprime el título y se muestra una tabla con los comandos disponibles
    console.print("💬 [bold red]Una aplicación ChatGPT creada con Python[/bold red] 💬\n")
    table = Table(title="Comandos disponibles", show_header=True, header_style="bold green")
    table.add_column("Comando")
    table.add_column("Descripción")
    table.add_row("🆕 [bold]new[/bold]", "Crear una nueva conversación")
    table.add_row("🗑️ [bold]clear[/bold]", "Eliminar los mensajes de la conversación de la pantalla")
    table.add_row("✅ [bold]export[/bold]", "Exportar la conversación actual a un archivo de texto")
    table.add_row("📧 [bold]send_email[/bold]", "Enviar un correo electrónico")
    table.add_row("🔎 [bold]search[/bold]", "Buscar directamente en google")
    table.add_row("📜 [bold]history[/bold]", "Mostrar el historial de mensajes")
    table.add_row("🤖 [bold]help[/bold]", "Muestra esta tabla de comandos en cualquier momento de la conversación")
    table.add_row("👋 [bold]exit[/bold]", "Salir de la aplicación")
    console.print(table)

    # Se inicia la conversación con un mensaje del sistema
    context = {"role": "system","content": "Esto es una aplicación creada con Python."}
    messages = [context]

    # Ciclo principal que se ejecuta mientras el usuario no escriba "exit"
    while True:
        content = typer.prompt("\nEscribe tu pregunta")

        # Se añade el mensaje del usuario a la lista de mensajes
        messages.append({"role": "user", "content": content})

        # Se envía la solicitud a OpenAI
        response = openai.Completion.create(
            engine=model_engine,
            prompt=generate_prompt(messages),
            max_tokens=2048,
            temperature=1.1,
            n=1,
            stop=None,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )

        # Comandos ....

        # Si el usuario escribe "new", se crea una nueva conversación
        if content.lower() == "new":
            console.print("🆕 Se ha creado una nueva conversación 🆕\n")
            messages = [context]
            continue

        # Si el usuario escribe "exit", se le pregunta si está seguro de que quiere salir
        elif content.lower() == "exit":
            if typer.confirm("¿Estás seguro de que quieres salir?"):
                console.print("👋 ¡Hasta pronto! 👋")
                raise typer.Abort()

        # Si el usuario escribe "export", se exporta la conversación actual a un archivo de texto
        elif content.lower() == "export":
            export_conversation(messages)
            console.print("✅ Conversación exportada correctamente ✅\n")
            continue  # saltar la llamada a la API de OpenAI y la respuesta

        # Si el usuario escribe "search", se le pide qué término quiere buscar y se abre una pestaña en el navegador con los resultados
        elif content.lower() == "search":
            term = typer.prompt("¿Qué quieres buscar en google?")
            url = f"https://www.google.com/search?q={term}"
            webbrowser.open_new_tab(url)
            console.print(f"🔎 Buscando '{term}' en el navegador web 🔎\n")

        # Si el usuario escribe "clear", se eliminan todos los mensajes excepto el mensaje inicial del sistema
        elif content.lower() == "clear":
            console.clear()
            console.print("🗑️ Conversación actual eliminada 🗑️\n")
            continue

        # Si el usuario escribe "send_mail", se llama a la función send_email con los parámetros necesarios
        if content.lower() == "send_mail":
            to_address = Prompt.ask("Escribe la dirección de correo electrónico del destinatario")
            subject = Prompt.ask("Escribe el asunto del correo electrónico")
            body = Prompt.ask("Escribe el cuerpo del correo electrónico")
            send_email(to_address, subject, body)
            continue


        # Agregar un bloque de código en el bucle principal que maneje el comando "history"
        elif content.lower() == "history":
            show_history(messages)
            continue

        # Si el usuario escribe "help", se imprime una lista con los comandos disponibles
        elif content.lower() == "help":
            console.print(table)
            continue  # saltar la llamada a la API de OpenAI y la respuesta

        # Se obtiene la respuesta de OpenAI y se añade a la lista de mensajes
        response_content = response.choices[0].text
        messages.append({"role": "assistant", "content": response_content})

        # Se muestra la respuesta al usuario
        styled_text = f"\n[bold red]-> Respuesta: [/bold red][green]{response_content.replace('Asistente:', '')}[/green]\n"
        console.print(styled_text)

# Se ejecuta la función principal si se llama a este script directamente
if __name__ == "__main__":
    typer.run(main)
