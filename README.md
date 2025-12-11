# 📁 Organizador de Archivos - Aplicación de Escritorio

Aplicación de escritorio moderna para organizar archivos automáticamente por categorías usando Flask y Eel.

## 🚀 Características

- **Interfaz de escritorio moderna** con Eel (HTML/CSS/JS)
- **Manejo robusto de excepciones** en todas las operaciones
- **Uso de pathlib** para rutas multiplataforma
- **Organización automática** por tipo de archivo
- **Vista previa** antes de organizar
- **Estadísticas detalladas** de la operación
- **Logging completo** de todas las operaciones
- **Manejo de archivos duplicados** (renombrado automático)

## 📦 Categorías Soportadas

- **Imágenes**: jpg, jpeg, png, gif, bmp, svg, webp, ico
- **PDFs**: pdf
- **Documentos Word**: doc, docx
- **Documentos Excel**: xls, xlsx, csv
- **Documentos PowerPoint**: ppt, pptx
- **Documentos de texto**: txt, md, log
- **Videos**: mp4, avi, mkv, mov, wmv, flv, webm
- **Música**: mp3, wav, flac, aac, ogg, m4a
- **Comprimidos**: zip, rar, 7z, tar, gz
- **Ejecutables**: exe, msi, bat, cmd
- **Otros**: archivos no categorizados

## 🛠️ Instalación

1. Instalar las dependencias:
```cmd
pip install -r requirements.txt
```

## ▶️ Uso

1. Ejecutar la aplicación:
```cmd
python script_ordenar_archivos.py
```

2. La aplicación se abrirá en una ventana de escritorio

3. Seleccionar la carpeta a organizar:
   - Clic en "Documentos" para usar tu carpeta de documentos
   - O hacer doble clic en el campo de texto para escribir una ruta personalizada

4. Revisar la vista previa de archivos

5. Clic en "Organizar Archivos" para ejecutar

## 🔒 Seguridad

- Manejo de permisos de archivos
- Validación de rutas
- Confirmación antes de mover archivos
- Logging de todas las operaciones en `organizador_archivos.log`
- Renombrado automático de archivos duplicados

## 📝 Logs

Todos los eventos se registran en `organizador_archivos.log` con:
- Timestamp
- Nivel de log (INFO, ERROR)
- Mensaje descriptivo

## 🎨 Interfaz

- Diseño moderno con gradientes
- Animaciones suaves
- Responsive
- Feedback visual de todas las operaciones
- Estadísticas en tiempo real

## ⚠️ Notas

- Los archivos ocultos (que empiezan con `.`) se omiten
- Si un archivo ya existe en destino, se renombra automáticamente
- Las carpetas de categorías se crean automáticamente si no existen