# GEOPORTAL RPAs AMAYA

Este es un proyecto web que muestra un mapa interactivo con misiones de vuelo con dron sobre Andalucía, basado en la biblioteca Leaflet y alojado en GitHub Pages.

## 📌 Características
- Visualización de mapas base: OpenStreetMap y Esri World Imagery.
- Control de zoom y navegación interactiva.
- Polígonos de vuelos con dron extraídos de un archivo GeoJSON.
- Información emergente al hacer clic en un polígono.

## 🚀 Cómo ver la web en GitHub Pages
1. Sube todos los archivos a un repositorio de GitHub.
2. Ve a **Configuración → Páginas** en tu repositorio.
3. En "Fuente", selecciona **main** (o la rama principal) y la carpeta **root**.
4. Guarda los cambios y espera unos minutos.
5. Accede a tu web en: `https://tuusuario.github.io/geoportal-rpas-amaya/`.

## 📂 Estructura del Proyecto
```
geoportal-rpas-amaya/
│── css/
│   └── styles.css
│── js/
│   ├── map.js
│   ├── Poligonos_RPAs_AMAYA.js
│── images/
│   ├── logo_derecha.png
│   ├── logo_izquierda.png
│── index.html
│── README.md
│── .gitignore
```

> **Nota:** Leaflet se carga desde un CDN y no está incluido en la carpeta `js`.

## 🛠 Tecnologías Utilizadas
- **HTML5**
- **CSS3**
- **JavaScript**
- **Leaflet.js**
- **GitHub Pages**

## 📧 Contacto
Si tienes preguntas, puedes contactarme en `tuemail@example.com`. 🚀

## 🧪 Pruebas
Antes de ejecutar la suite de tests con **pytest**, ejecuta `./setup.sh` para instalar las dependencias:

```bash
./setup.sh        # instala las dependencias
pytest
```
