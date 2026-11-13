# 🎓 Asistente Virtual de la Clase

Asistente académico en formato chat, desarrollado con **Python 3.11** y **Streamlit**. Utiliza el modelo `openai/gpt-oss-20b` a través de la **API de Groq**.

## Funcionalidades

- Preguntas en lenguaje natural y respuestas generadas por el modelo.
- Interfaz de chat con mensajes del usuario y del asistente.
- Historial de la conversación durante la sesión, enviado al modelo en cada consulta para conservar el contexto.
- Clave de API cargada desde `st.secrets["LLAVE_PROFESOR"]`.
- Mensajes de error claros para problemas de configuración o conexión.
- Interfaz completamente en español.

## Estructura del proyecto

```
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml      # lo creas tú (no se sube a Git)
```

## Requisitos previos

- Python 3.11
- Una clave de API de Groq: <https://console.groq.com/keys>

## Ejecución local

1. Crea y activa un entorno virtual:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Crea la carpeta `.streamlit/` y copia dentro la plantilla `secrets.toml`:

   ```bash
   mkdir .streamlit
   cp secrets.toml .streamlit/secrets.toml
   ```

4. Edita `.streamlit/secrets.toml` y coloca tu clave real:

   ```toml
   LLAVE_PROFESOR = "gsk_xxxxxxxxxxxxxxxxxxxx"
   ```

5. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

   Se abrirá en <http://localhost:8501>.

> Importante: la plantilla `secrets.toml` de la raíz solo contiene un valor de ejemplo. El archivo con tu clave real debe estar en `.streamlit/secrets.toml`, que está excluido por `.gitignore`.

## Publicación en Streamlit Community Cloud

1. Sube el proyecto a un repositorio de GitHub (sin `.streamlit/secrets.toml`).
2. Entra a <https://share.streamlit.io> e inicia sesión con GitHub.
3. Pulsa **Create app** y selecciona el repositorio, la rama y el archivo principal `app.py`.
4. En **Advanced settings**:
   - Elige **Python 3.11**.
   - En **Secrets**, pega:

     ```toml
     LLAVE_PROFESOR = "gsk_tu_clave_real"
     ```
5. Pulsa **Deploy**.

## Solución de problemas

| Mensaje | Causa probable |
|---|---|
| No se encontró la clave de API | Falta `.streamlit/secrets.toml` o los Secrets en la nube. |
| La clave de API no es válida | Clave incorrecta, vencida o revocada. |
| Límite de solicitudes | Demasiadas consultas en poco tiempo; espera unos segundos. |
| No se pudo conectar con la API | Sin conexión a internet o servicio temporalmente caído. |

## Seguridad

- No escribas la clave de API dentro del código.
- No subas `.streamlit/secrets.toml` a GitHub.
- Si expones una clave por error, revócala y genera otra en la consola de Groq.
