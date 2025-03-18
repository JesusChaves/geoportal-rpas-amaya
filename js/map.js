var map = L.map('map').setView([37.5, -4.5], 7); // Centrado en Andalucía

// Capas base
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var esri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri & contributors'
});

// Control de capas
var baseMaps = {
    "OpenStreetMap": osm,
    "Esri World Imagery": esri
};
L.control.layers(baseMaps).addTo(map);

// Control de zoom
L.control.zoom({ position: 'topright' }).addTo(map);

// Añadir los polígonos
L.geoJSON(poligonosRPAs, {
    style: function (feature) {
        return {
            color: "red",
            fillColor: "blue",
            fillOpacity: 0.4
        };
    },
    onEachFeature: function (feature, layer) {
        let props = feature.properties || {};
        let mision = props.mision ? props.mision : "No disponible";
        let fecha = props.fecha ? props.fecha : "No disponible";
        let descripcion = props.descripcion ? props.descripcion : "No disponible";
    
        let popupContent = `<b>Misión:</b> ${mision}<br>
                            <b>Fecha:</b> ${fecha}<br>
                            <b>Descripción:</b> ${descripcion}`;
        
        layer.bindPopup(popupContent);
    }
    }).addTo(map);
