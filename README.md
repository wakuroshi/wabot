Wabot es un bot de Discord **open-source**, desarrollado desde cero, cuyo objetivo es facilitar la **gestión de proyectos directamente desde Discord** de forma simple, clara y accesible para todos los miembros del servidor.

Está pensado especialmente para comunidades técnicas, clubes, equipos de desarrollo o study groups que trabajan con proyectos colaborativos.

---

# Características

- Creación y gestión de proyectos desde Discord
- Sistema de **lead por proyecto**
- Creación y gestión de **hilos por proyecto**
- Estados del proyecto (Activo, Testing, Completado)
- Registro de lenguajes utilizados
- Enlace a repositorios GitHub
- Canal de información centralizado
- Encuestas y utilidades generales (TODO: agregar mas utilidades)
- Control de permisos por roles (staff / lead / owner)
- Sistema de archivado de proyectos

---

## 🛠️ Requisitos

- Python **3.10+**
- Un bot de Discord creado en el Developer Portal
- Permisos para crear canales, hilos y mensajes fijados

---

## 📦 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/wabot.git
cd wabot
```

### Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### Instalar dependencias y configurar 
```bash
pip install -r requirements.txt
```
Copia el archivo de ejemplo y rellena los valores:
```bash
cp .env.example .env
```
---

Este codigo es totalmente abierto, modificable y replicable. Por favor sugiere modificaciones para mejorarlo o incluso refactorizaciones de codigo si hacen falta.
