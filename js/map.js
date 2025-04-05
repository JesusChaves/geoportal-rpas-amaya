// map.js

// Crea el mapa centrado en Andalucía
var mapa = L.map('map').setView([37.5, -5.8], 8);

// Capa base OpenStreetMap
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapa);

// Capa base Esri World Imagery
var esri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri'
});

// Selector de capas base
var baseMaps = {
  "OpenStreetMap": osm,
  "Esri World Imagery": esri
};

L.control.layers(baseMaps).addTo(mapa);

// Controles de zoom
L.control.zoom({ position: 'topright' }).addTo(mapa);
