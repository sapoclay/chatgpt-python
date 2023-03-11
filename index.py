import openai
import typer
import webbrowser
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from rich.table import Table
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de la consola
console = Console()

def main():

    openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # La API Key se genera en https://platform.openai.com

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

    # Contexto del asistente
    context = {"role": "system", "content": "Esto es una aplicación Python."}
    messages = [context]

    while True:

        content = __prompt()

        # Comandos ....

        # Si el usuario escribe "new", se crea una nueva conversación
        if content.lower() == "new":
            print("🆕 Se ha creado una nueva conversación 🆕")
            messages = [context]
            content = __prompt()
            continue

        # Si el usuario escribe export, se exporta la conversación actual a un archivo de texto
        elif content.lower() == "export":
            export_conversation(messages)
            console.print("✅ Conversación exportada correctamente ✅\n")
            continue

        # Si el usuario escribe "search", se le pide qué término quiere buscar y se abre una pestaña en el navegador con los resultados
        elif content.lower() == "search":
            term = typer.prompt("¿Qué quieres buscar en google?")
            url = f"https://www.google.com/search?q={term}"
            webbrowser.open_new_tab(url)
            console.print(f"🔎 Buscando '{term}' en el navegador web 🔎\n")
            continue

        # Si el usuario escribe "clear", se eliminan todos los mensajes excepto el mensaje inicial del sistema
        elif content.lower() == "clear":
            console.clear()
            console.print("🗑️ Conversación actual eliminada 🗑️\n")
            continue

        # Si el usuario escribe "send_mail", se llama a la función send_email con los parámetros necesarios
        elif content.lower() == "send_email":
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

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # El motor que vamos a utilizar, podríamos cambiarlo por text-davinci-002
            messages=messages,
            max_tokens=2048,
            temperature=1,
            n=1,
            stop=None,
            presence_penalty=0.5,
            frequency_penalty=0.5,)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold red]> [/bold red] [green]{response_content}[/green]")

# Función para guardar la conversación en el archivo conversacion.txt, machacando el contenido anterior
def export_conversation(messages):
    with open("conversacion.txt", "w") as file:
        for message in messages:
            file.write(f"{message['role']}: {message['content']}\n")

# Función para mostrar el historial de mensajes
def show_history(messages):
    console.print("\nHistorial de mensajes:")
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            console.print(f"[bold blue]{role}:[/bold blue] {content}")
        elif role == "user":
            console.print(f"[bold green]{role}:[/bold green] {content}")
        else:
            console.print(f"[bold red]{role}:[/bold red] {content}")
    console.print()

# Función para enviar correos electrónicos
def send_email(to_address, subject, body):
    from_address = 'XXXXXXXX'
    password = 'XXXXXXXX'
    smtp_server = 'XXXXXXXX'
    smtp_port = 465

    # Crear el objeto MIME
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    # Agregar el cuerpo del correo electrónico
    message.attach(MIMEText(body, 'plain'))

    # Establecer la conexión con el servidor SMTP
    smtp_server = SMTP(smtp_server, smtp_port)
    smtp_server.starttls()
    smtp_server.login(from_address, password)

    # Enviar el correo electrónico
    smtp_server.send_message(message)

    # Cerrar la conexión
    smtp_server.quit()

    console.print(f"📧 El correo electrónico ha sido enviado a {to_address} 📧\n")
    continue

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


def __prompt() -> str:
    prompt = typer.prompt("\nEscribe tu pregunta")

    if prompt == "exit":
        exit = typer.confirm("¿Estás seguro de que quieres salir?")
        if exit:
            print("👋 ¡Hasta pronto! ✋")
            raise typer.Abort()

        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)
