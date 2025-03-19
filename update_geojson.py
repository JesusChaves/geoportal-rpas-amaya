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
        let imageHtml = props.imagen ? `<br><a href='${props.imagen}' target='_blank'><img src='${props.imagen}' width='100' style='border: 1px solid #ccc; cursor: pointer;' onclick='expandImage(event, "${props.imagen}")'></a>` : "";
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
                            <b>Altura de vuelo (m):</b> ${props.altura || "No disponible"}<br>
                            <b>GSD (cm/px):</b> ${props.gsd || "No disponible"}<br>
                            <b>Contacto:</b> ${props.contacto || "No disponible"}${imageHtml}`;
        layer.bindPopup(popupContent);
    }
}).addTo(map);

// Función para ampliar la imagen
function expandImage(event, imageUrl) {
    event.preventDefault();
    let overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.background = 'rgba(0, 0, 0, 0.8)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '1000';
    
    let img = document.createElement('img');
    img.src = imageUrl;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';
    img.style.border = '5px solid white';
    img.style.boxShadow = '0px 0px 15px rgba(255, 255, 255, 0.5)';
    
    let closeBtn = document.createElement('div');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '20px';
    closeBtn.style.right = '30px';
    closeBtn.style.fontSize = '40px';
    closeBtn.style.color = 'white';
    closeBtn.style.cursor = 'pointer';
    closeBtn.addEventListener('click', function() {
        document.body.removeChild(overlay);
    });
    
    overlay.appendChild(img);
    overlay.appendChild(closeBtn);
    document.body.appendChild(overlay);
}
