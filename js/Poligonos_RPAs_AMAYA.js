const Poligonos_RPAs_AMAYA = {
    "type": "FeatureCollection",
    "features": []
  };
  
  // Cargar los datos dinámicamente desde archivo externo JSON
  fetch("../Poligonos_RPAS.json")
    .then((response) => response.json())
    .then((data) => {
      L.geoJSON(data, {
        onEachFeature: function (feature, layer) {
          // Generar contenido del popup
          const props = feature.properties;
  
          // Transformar enlace de Drive (si es necesario)
          let imagenMini = "";
          if (props.Imagen && props.Imagen.includes("drive.google.com")) {
            const match = props.Imagen.match(/[-\w]{25,}/);
            if (match) {
              const fileId = match[0];
              const thumbnailURL = `https://drive.google.com/thumbnail?id=${fileId}`;
              imagenMini = `
                <div style="text-align:center;">
                  <img src="${thumbnailURL}" style="width:140px; margin-top:8px;" alt="Miniatura"><br>
                  <span style="font-size:12px;">Click derecho → Abrir imagen</span>
                </div>`;
            }
          }
  
          const contenidoPopup = `
            <div style="font-size:14px;">
              <b>Nombre:</b> ${props.Nombre}<br>
              <b>Fecha:</b> ${props.Fecha}<br>
              <b>Localidad:</b> ${props.Localidad}<br>
              <b>Descripción:</b> ${props.Descripcion}<br>
              <b>Taxón:</b> ${props.Taxon}<br>
              <b>Departamento:</b> ${props.Departamento}<br>
              <b>Tipo de Vuelo:</b> ${props.Tipo_Vuelo}<br>
              <b>Piloto:</b> ${props.Piloto}<br>
              <b>Dron:</b> ${props.Dron}<br>
              <b>Sensor:</b> ${props.Sensor}<br>
              <b>Altura Vuelo:</b> ${props.Altura_Vuelo} m<br>
              <b>GSD:</b> ${props.GSD} cm/px<br>
              <b>Contacto:</b> ${props.Contacto}<br>
              ${imagenMini}
            </div>
          `;
  
          // Estilo del polígono según Departamento
          const fillColors = {
            "Cauces": "#215F9A",
            "Oficina de Proyectos": "#FFFF00",
            "Oficina Técnica": "#D86ECC",
            "Laboratorio Huelva": "#FF0000",
            "IDI": "#3B7D23",
            "UGC": "#747474",
            "OP Sevilla": "#C04F15",
          };
          const fillColor = fillColors[props.Departamento] || "#00B0F0";
  
          const polygon = L.geoJSON(feature.geometry, {
            style: {
              color: "#FF0000",
              weight: 2,
              fillColor: fillColor,
              fillOpacity: 0.2,
            }
          }).addTo(map);
  
          // Punto central (centroide) del polígono
          const bounds = polygon.getBounds();
          const center = bounds.getCenter();
  
          const marker = L.circleMarker(center, {
            radius: 5,
            fillColor: "#000",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map);
  
          marker.bindPopup(contenidoPopup);
        }
      });
    })
    .catch((err) => {
      console.error("Error al cargar el GeoJSON:", err);
    });
  