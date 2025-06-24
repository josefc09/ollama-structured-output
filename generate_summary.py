import ollama
import json

# Cargar la gramática GBNF
try:
    with open('summary_grammar.gbnf', 'r') as f:
        grammar = f.read()
except FileNotFoundError:
    print("Error: El archivo 'summary_grammar.gbnf' no fue encontrado.")
    exit()

# Artículo
article_text = """
La inteligencia artificial (IA) está transformando rápidamente el mundo. Desde asistentes de voz hasta coches autónomos, la IA está en todas partes. Uno de los campos más prometedores es el aprendizaje automático, que permite a las máquinas aprender de los datos sin ser programadas explícitamente. Sin embargo, también hay desafíos éticos y de seguridad importantes que deben abordarse, como la privacidad de los datos y el sesgo algorítmico. Es fundamental desarrollar la IA de manera responsable para maximizar sus beneficios y minimizar los riesgos.
"""

prompt = f"""
Genera únicamente una respuesta JSON para el siguiente artículo. La respuesta JSON debe contener tres campos: "title" (cadena de texto para el título), "summary" (cadena de texto para un resumen conciso) y "keywords" (un array de cadenas de texto para las palabras clave más importantes). No incluyas ningún texto adicional, explicaciones o formato Markdown fuera del objeto JSON.

Artículo:
{article_text}
"""

# Solicitud a Ollama con la gramática
print("Generando resumen con Ollama (esto puede tardar unos segundos)...")
try:
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[{'role': 'user', 'content': prompt}],
        options={
            'format': 'json', # Indica el tipo de formato
            'grammar': grammar # Pasamos nuestra gramática GBNF
        }
    )

    generated_json_string = response['message']['content']

    print("\n--- Respuesta del Modelo (JSON Crudo) ---")
    print(generated_json_string)

    summary_data = None
    try:
        # Intenta parsear directamente
        summary_data = json.loads(generated_json_string)
    except json.JSONDecodeError as e:
        # Si falla, intenta limpiar la cadena
        print(f"\nError inicial al decodificar JSON: {e}")
        print("Intentando limpiar la cadena JSON...")

        cleaned_json_string = generated_json_string.strip()

        # Primero, intenta remover bloques de markdown si existen
        if cleaned_json_string.startswith("```json"):
            cleaned_json_string = cleaned_json_string.removeprefix("```json").removesuffix("```")
            cleaned_json_string = cleaned_json_string.strip()

        # Si aún falla, busca el último '}' y recorta la cadena
        if cleaned_json_string.endswith('}"') or cleaned_json_string.endswith('}""'): # Para el caso de un " extra
             last_brace_index = cleaned_json_string.rfind('}')
             if last_brace_index != -1:
                 cleaned_json_string = cleaned_json_string[:last_brace_index + 1]
                 print(f"Cadena JSON recortada: {cleaned_json_string}")
                 try:
                     summary_data = json.loads(cleaned_json_string)
                 except json.JSONDecodeError as inner_e:
                     print(f"Error al decodificar JSON después de recortar: {inner_e}")
                     print("El modelo no devolvió un JSON válido a pesar de la gramática y el prompt estricto.")
                     print("Asegúrate de que no haya texto adicional o formato no deseado.")
             else:
                 print("No se encontró un '}' de cierre válido para recortar.")
        elif cleaned_json_string.endswith('}'): # Si ya termina en } pero el error fue por otra cosa
             try:
                 summary_data = json.loads(cleaned_json_string)
             except json.JSONDecodeError as inner_e:
                 print(f"Error al decodificar JSON después de limpiar: {inner_e}")
                 print("El modelo no devolvió un JSON válido a pesar de la gramática y el prompt estricto.")
                 print("Asegúrate de que no haya texto adicional o formato no deseado.")
        else:
            print("La cadena JSON no termina en '}' o '}\"' como se esperaba. No se pudo limpiar automáticamente.")


    if summary_data:
        print("\n--- Datos del Resumen (Python Dictionary) ---")
        print(f"Título: {summary_data.get('title', 'N/A')}")
        print(f"Resumen: {summary_data.get('summary', 'N/A')}")
        print(f"Palabras Clave: {', '.join(summary_data.get('keywords', ['N/A']))}")
    else:
        print("\nNo se pudo obtener el resumen en formato JSON válido.")


except Exception as e:
    print(f"\nOcurrió un error al comunicarse con Ollama: {e}")
    print("Asegúrate de que Ollama esté corriendo y el modelo especificado esté descargado.")
