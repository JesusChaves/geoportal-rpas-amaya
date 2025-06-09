// map.js

const mapa = L.map('map', {
  center: [37.5, -4.8], // Centrado en Andalucía
  zoom: 7,
  zoomControl: true
});

// Panel para los puntos (más arriba que los polígonos)
mapa.createPane("puntosPane");
mapa.getPane("puntosPane").style.zIndex = 650;

// Mapas base
const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(mapa);

const satelite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles © Esri'
});

L.control.layers({
  "Mapa": osm,
  "Satélite": satelite
}).addTo(mapa);
