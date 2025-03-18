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
var polygonsLayer = L.geoJSON(poligonosRPAs, {
    filter: function (feature) {
        return feature.geometry.type === "Polygon";
    },
    style: function (feature) {
        return {
            color: "red",
            fillColor: "blue",
            fillOpacity: 0.4
        };
    }
}).addTo(map);

// Añadir los puntos con ventanas emergentes
var pointsLayer = L.geoJSON(poligonosRPAs, {
    filter: function (feature) {
        return feature.geometry.type === "Point";
    },
    onEachFeature: function (feature, layer) {
        let props = feature.properties || {};
        let popupContent = `<b>Misión:</b> ${props.mision || "No disponible"}<br>
                            <b>Fecha:</b> ${props.fecha || "No disponible"}<br>
                            <b>Localidad:</b> ${props.localidad || "No disponible"}<br>
                            <b>Descripción:</b> ${props.descripcion || "No disponible"}<br>
                            <b>Operador:</b> ${props.operador || "No disponible"}<br>
                            <b>Departamento:</b> ${props.departamento || "No disponible"}<br>
                            <b>Tipo de vuelo:</b> ${props.tipo_vuelo || "No disponible"}<br>
                            <b>Piloto:</b> ${props.piloto || "No disponible"}<br>
                            <b>Aeronave:</b> ${props.aeronave || "No disponible"}<br>
                            <b>Sensor:</b> ${props.sensor || "No disponible"}<br>
                            <b>Altura (m):</b> ${props.altura || "No disponible"}<br>
                            <b>GSD (cm/px):</b> ${props.gsd || "No disponible"}<br>
                            <b>Contacto:</b> ${props.contacto || "No disponible"}`;
        layer.bindPopup(popupContent);
    }
}).addTo(map);
