import eel
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('organizador_archivos.log'),
        logging.StreamHandler()
    ]
)

# Configuración de tipos de archivos (solo documentos, imágenes, videos y música)
CATEGORIAS = {
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documentos_PDFs": [".pdf"],
    "Documentos_Word": [".doc", ".docx"],
    "Documentos_Excel": [".xls", ".xlsx", ".csv"],
    "Documentos_PowerPoint": [".ppt", ".pptx"],
    "Documentos_txt": [".txt", ".md"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Musica": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"]
}

# Extensiones que NO se deben mover (archivos comprimidos, ejecutables, etc.)
EXTENSIONES_BLOQUEADAS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
    '.exe', '.msi', '.bat', '.cmd', '.com', '.scr',
    '.dll', '.sys', '.ini', '.log'
}

class OrganizadorArchivos:
    # Archivos del sistema de Windows que no se deben mover
    ARCHIVOS_SISTEMA = {
        'desktop.ini', 'thumbs.db', 'pagefile.sys', 'hiberfil.sys',
        '$recycle.bin', 'system volume information', 'organizador_archivos.log'
    }
    
    def __init__(self):
        self.ruta_base = None
        self.estadisticas = {
            "movidos": 0,
            "errores": 0,
            "omitidos": 0
        }
    
    def es_archivo_sistema(self, archivo: Path) -> bool:
        """Verifica si un archivo es del sistema y no debe moverse"""
        nombre_lower = archivo.name.lower()
        return (
            archivo.name.startswith('.') or
            nombre_lower in self.ARCHIVOS_SISTEMA or
            archivo.name.startswith('~$')  # Archivos temporales de Office
        )
    
    def es_extension_bloqueada(self, archivo: Path) -> bool:
        """Verifica si la extensión del archivo está bloqueada"""
        return archivo.suffix.lower() in EXTENSIONES_BLOQUEADAS
    
    def establecer_ruta(self, ruta: str) -> bool:
        """Establece y valida la ruta base"""
        try:
            self.ruta_base = Path(ruta)
            if not self.ruta_base.exists():
                raise FileNotFoundError(f"La ruta no existe: {ruta}")
            if not self.ruta_base.is_dir():
                raise NotADirectoryError(f"La ruta no es un directorio: {ruta}")
            return True
        except Exception as e:
            logging.error(f"Error al establecer ruta: {e}")
            return False
    
    def crear_carpetas(self) -> Tuple[bool, str]:
        """Crea las carpetas de categorías si no existen"""
        try:
            for carpeta in CATEGORIAS.keys():
                ruta_carpeta = self.ruta_base / carpeta
                ruta_carpeta.mkdir(exist_ok=True)
                logging.info(f"Carpeta verificada/creada: {carpeta}")
            return True, "Carpetas creadas exitosamente"
        except PermissionError as e:
            msg = f"Sin permisos para crear carpetas: {e}"
            logging.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Error al crear carpetas: {e}"
            logging.error(msg)
            return False, msg
    
    def obtener_categoria(self, archivo: Path) -> str:
        """Determina la categoría de un archivo según su extensión"""
        extension = archivo.suffix.lower()
        for categoria, extensiones in CATEGORIAS.items():
            if extension in extensiones:
                return categoria
        return "Otros"
    
    def mover_archivo(self, archivo: Path, categoria: str) -> Tuple[bool, str]:
        """Mueve un archivo a su carpeta correspondiente"""
        try:
            destino = self.ruta_base / categoria / archivo.name
            
            # Si el archivo ya existe en destino, agregar número
            if destino.exists():
                contador = 1
                while destino.exists():
                    nuevo_nombre = f"{archivo.stem}_{contador}{archivo.suffix}"
                    destino = self.ruta_base / categoria / nuevo_nombre
                    contador += 1
            
            shutil.move(str(archivo), str(destino))
            self.estadisticas["movidos"] += 1
            return True, f"Movido: {archivo.name} → {categoria}"
        
        except PermissionError as e:
            self.estadisticas["errores"] += 1
            msg = f"Sin permisos para mover {archivo.name}: {e}"
            logging.error(msg)
            return False, msg
        except Exception as e:
            self.estadisticas["errores"] += 1
            msg = f"Error al mover {archivo.name}: {e}"
            logging.error(msg)
            return False, msg
    
    def organizar(self) -> Dict:
        """Organiza todos los archivos en la ruta base"""
        if not self.ruta_base:
            return {"success": False, "mensaje": "No se ha establecido una ruta"}
        
        # Reiniciar estadísticas
        self.estadisticas = {"movidos": 0, "errores": 0, "omitidos": 0}
        resultados = []
        
        # Crear carpetas
        exito, mensaje = self.crear_carpetas()
        if not exito:
            return {"success": False, "mensaje": mensaje}
        
        # Obtener lista de carpetas de categorías
        carpetas_sistema = set(CATEGORIAS.keys())
        
        try:
            # Listar archivos
            archivos = [f for f in self.ruta_base.iterdir() if f.is_file()]
            
            for archivo in archivos:
                # Omitir archivos del sistema
                if self.es_archivo_sistema(archivo):
                    self.estadisticas["omitidos"] += 1
                    logging.info(f"Archivo del sistema omitido: {archivo.name}")
                    continue
                
                # Omitir archivos con extensiones bloqueadas
                if self.es_extension_bloqueada(archivo):
                    self.estadisticas["omitidos"] += 1
                    logging.info(f"Archivo bloqueado (comprimido/ejecutable): {archivo.name}")
                    continue
                
                categoria = self.obtener_categoria(archivo)
                exito, mensaje = self.mover_archivo(archivo, categoria)
                resultados.append({"archivo": archivo.name, "categoria": categoria, "exito": exito, "mensaje": mensaje})
            
            return {
                "success": True,
                "estadisticas": self.estadisticas,
                "resultados": resultados
            }
        
        except Exception as e:
            msg = f"Error durante la organización: {e}"
            logging.error(msg)
            return {"success": False, "mensaje": msg}

# Instancia global
organizador = OrganizadorArchivos()

# Funciones expuestas a Eel
@eel.expose
def obtener_ruta_documentos():
    """Obtiene la ruta de Documentos del usuario"""
    try:
        ruta = Path.home() / "Documents"
        return str(ruta)
    except Exception as e:
        logging.error(f"Error al obtener ruta de documentos: {e}")
        return ""

@eel.expose
def establecer_ruta(ruta):
    """Establece la ruta de trabajo"""
    try:
        exito = organizador.establecer_ruta(ruta)
        return {"success": exito, "mensaje": "Ruta establecida" if exito else "Error al establecer ruta"}
    except Exception as e:
        return {"success": False, "mensaje": str(e)}

@eel.expose
def organizar_archivos():
    """Organiza los archivos en la ruta establecida"""
    try:
        resultado = organizador.organizar()
        return resultado
    except Exception as e:
        logging.error(f"Error en organizar_archivos: {e}")
        return {"success": False, "mensaje": str(e)}

@eel.expose
def obtener_vista_previa(ruta):
    """Obtiene una vista previa de los archivos a organizar"""
    try:
        ruta_path = Path(ruta)
        if not ruta_path.exists():
            return {"success": False, "mensaje": "La ruta no existe"}
        
        archivos = [f for f in ruta_path.iterdir() if f.is_file()]
        preview = {}
        omitidos = 0
        
        for archivo in archivos:
            # Omitir archivos del sistema en la vista previa
            if organizador.es_archivo_sistema(archivo):
                omitidos += 1
                continue
            
            # Omitir archivos bloqueados
            if organizador.es_extension_bloqueada(archivo):
                omitidos += 1
                continue
            
            categoria = organizador.obtener_categoria(archivo)
            if categoria not in preview:
                preview[categoria] = []
            preview[categoria].append(archivo.name)
        
        return {"success": True, "preview": preview, "omitidos": omitidos}
    except Exception as e:
        return {"success": False, "mensaje": str(e)}

@eel.expose
def actualizar_vista():
    """Actualiza la vista previa para detectar nuevos archivos"""
    try:
        if not organizador.ruta_base:
            return {"success": False, "mensaje": "No hay ruta establecida"}
        
        return obtener_vista_previa(str(organizador.ruta_base))
    except Exception as e:
        return {"success": False, "mensaje": str(e)}

def iniciar_app():
    """Inicia la aplicación Eel"""
    try:
        eel.init('web')
        eel.start('index.html', size=(900, 700), port=8080)
    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    iniciar_app()