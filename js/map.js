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
        layer.bindPopup('<b>Misión:</b> ' + feature.properties.dwc:eventID + '<br>' +
                        '<b>Fecha:</b> ' + feature.properties.dwc:eventDate + '<br>' +
                        '<b>Localidad:</b> ' + feature.properties.dwc:locality);
                        '<b>Descripción:</b> ' + feature.properties.Descrip);
                        '<b>Altura vuelo (m):</b> ' + feature.properties.altitude_(m));
                        '<b>Piloto:</b> ' + feature.properties.pilot);
                        '<b>Dron:</b> ' + feature.properties.drone);
                        '<b>Sensor:</b> ' + feature.properties.sensor);
                        '<b>Tipo de vuelo:</b> ' + feature.properties.FlightCat);
                        '<b>Departamento:</b> ' + feature.properties.Department);
                        '<b>Contacto:</b> ' + feature.properties.contact);
                    }
}).addTo(map);
