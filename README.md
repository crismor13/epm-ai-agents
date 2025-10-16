# Agente IA para Consultas de EPM 💧

Este proyecto es una solución de inteligencia artificial diseñada para responder preguntas de los usuarios sobre las interrupciones del servicio de agua de EPM y otras consultas generales, utilizando información en tiempo real y una base de conocimiento documental.

## 🎯 Problema

La información sobre las interrupciones del servicio de agua publicada en el sitio web de EPM, aunque disponible, no es fácil de filtrar o consultar. Esto obliga a los usuarios a revisar manualmente largas listas, generando confusión y llamadas innecesarias al servicio de atención al cliente.

## ✨ Solución

Se ha desarrollado un agente conversacional que utiliza un Modelo de Lenguaje Grande (LLM) para:

1. **Extraer y procesar** la información actualizada de la página de EPM en tiempo real.
2. **Consultar una base de conocimiento** con guías y documentos internos para responder preguntas frecuentes.
3. **Entender y responder** preguntas formuladas en lenguaje natural, proporcionando respuestas claras, rápidas y contextualizadas.

---

## 🚀 Características Principales

- **Scraping en Tiempo Real**: El agente consulta la página oficial de EPM al momento de la pregunta para obtener los datos más recientes sobre cortes de agua.
- **Filtrado Inteligente**: Filtra automáticamente las interrupciones pasadas para mostrar solo los eventos programados desde el día actual en adelante.
- **Base de Conocimiento (RAG)**: Utiliza Retrieval-Augmented Generation para responder preguntas que no están relacionadas con los cortes de agua, basándose en una colección de documentos PDF.
- **Memoria Conversacional**: El agente recuerda el historial de la conversación actual, permitiendo preguntas de seguimiento y un diálogo más natural.
- **Interfaz de Usuario Amigable**: Incluye una aplicación web creada con Streamlit para una interacción fácil e intuitiva.
- **API Robusta**: Cuenta con un backend de FastAPI para poder integrar el agente con otros sistemas.

---

## 🏗️ Arquitectura del Sistema

El flujo de trabajo de la aplicación sigue la siguiente arquitectura:

```
Usuario
   │
   ▼
[Interfaz de Usuario (Streamlit) / API (FastAPI)]
   │
   ▼
[Agente de LangChain con Memoria]
   ├──> [Herramienta 1: Web Scraper] → (Consulta página de EPM)
   ├──> [Herramienta 2: Buscador RAG] → (Consulta Vector Store - FAISS)
   │
   ▼
[LLM (OpenAI GPT-4o)] → (Genera la respuesta con el contexto obtenido)
   │
   ▼
Respuesta al Usuario
```

---

## 🛠️ Stack Tecnológico

- **Lenguaje**: 🐍 Python 3.11+
- **Orquestación de IA**: 🔗 LangChain
- **Modelo de Lenguaje**: 🤖 OpenAI (GPT-4o)
- **Embeddings & Vector Store**: 🧠 OpenAI Embeddings & FAISS
- **Web Scraping**: 🍲 Beautiful Soup
- **Interfaz de Usuario**: 🎈 Streamlit
- **Backend API**: 🚀 FastAPI
- **Gestión de Entorno**: 📦 venv, python-dotenv

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd epm-agents
```

### 2. Crear y Activar el Entorno Virtual

```bash
# Crear el entorno
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto.  
Puedes copiar el contenido de `.env.example` (si existe) o añadir la siguiente línea:

```bash
# .env
OPENAI_API_KEY="sk-..."
```

Reemplaza `sk-...` con tu clave de API de OpenAI.

### 5. Preparar la Base de Conocimiento (RAG)

Coloca todos los documentos PDF de las guías de EPM dentro de la carpeta `docs/`.

Ejecuta el script de ingestión para procesar los documentos y crear la base de datos vectorial:

```bash
python -m src.rag.ingest_rag_data
```

Este comando creará una carpeta `faiss_index` en la raíz del proyecto.

---

## ▶️ Cómo Ejecutar la Aplicación

Tienes dos formas de interactuar con el agente:

### 1. A través de la Interfaz de Usuario (Recomendado)

Ejecuta la aplicación de Streamlit con el siguiente comando:

```bash
streamlit run ui.py
```

Abre tu navegador y ve a: [http://localhost:8501](http://localhost:8501)

### 2. A través de la API

Ejecuta el servidor de FastAPI:

```bash
uvicorn src.api.main:app --reload
```

Abre tu navegador y ve a: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
para acceder a la documentación interactiva de la API y hacer pruebas.

---

## 📁 Estructura del Proyecto

```bash
epm-agents/
├── .env                  # Archivo de secretos (API Keys) - NO SUBIR A GIT
├── .gitignore            # Archivos a ignorar por Git
├── requirements.txt      # Dependencias de Python
├── ui.py                 # Interfaz de usuario con Streamlit
├── docs/                 # Carpeta para los PDFs de las guías (RAG)
└── src/
    ├── agent/            # Lógica del agente de LangChain
    │   ├── agent_creator.py
    │   └── tools.py
    ├── api/              # Backend con FastAPI
    │   └── main.py
    ├── core/             # Configuración central
    │   └── config.py
    ├── rag/              # Lógica para RAG
    │   └── ingest_rag_data.py
    └── scraping/         # Lógica de Web Scraping
        ├── scraper.py
        └── parser.py
```
