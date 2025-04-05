// Poligonos_RPAs_AMAYA.js

// Carga dinámicamente el archivo GeoJSON generado
fetch('../Poligonos_RPAS.geojson')
  .then(response => response.json())
  .then(data => {
    // Agrega los polígonos y puntos al mapa
    L.geoJSON(data, {
      onEachFeature: function(feature, layer) {
        var contenidoPopup = `
          <div style="display:flex;">
            <div style="padding-right:10px;">
              <b>Nombre:</b> ${feature.properties.Nombre}<br>
              <b>Fecha:</b> ${feature.properties.Fecha}<br>
              <b>Localidad:</b> ${feature.properties.Localidad}<br>
              <b>Descripción:</b> ${feature.properties.Descripcion}<br>
              <b>Taxón:</b> ${feature.properties.Taxon}<br>
              <b>Departamento:</b> ${feature.properties.Departamento}<br>
              <b>Tipo de Vuelo:</b> ${feature.properties.Tipo_Vuelo}<br>
              <b>Piloto:</b> ${feature.properties.Piloto}<br>
              <b>Dron:</b> ${feature.properties.Dron}<br>
              <b>Sensor:</b> ${feature.properties.Sensor}<br>
              <b>Altura Vuelo:</b> ${feature.properties.Altura_Vuelo} m<br>
              <b>GSD:</b> ${feature.properties.GSD} cm/px<br>
              <b>Contacto:</b> ${feature.properties.Contacto}
            </div>
            <div>
              <a href="${feature.properties.Imagen}" target="_blank">
                <img src="${feature.properties.Imagen}" style="width:120px; height:auto;"/>
              </a>
            </div>
          </div>`;
        layer.bindPopup(contenidoPopup);
      },
      style: {
        color: "#0078FF",
        weight: 2,
        fillColor: "#0078FF",
        fillOpacity: 0.2
      },
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, {
          radius: 6,
          fillColor: "#FF0000",
          color: "#FFFFFF",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.9
        });
      }
    }).addTo(mapa);
  })
  .catch(error => {
    console.error('Error al cargar el GeoJSON:', error);
  });
