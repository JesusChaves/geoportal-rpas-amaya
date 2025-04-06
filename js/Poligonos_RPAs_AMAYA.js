// Poligonos_RPAs_AMAYA.js

fetch('Poligonos_RPAS.json')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      onEachFeature: function(feature, layer) {
        let props = feature.properties;
        let popup = `
          <div style="display:flex; flex-wrap: wrap;">
            <div style="min-width: 240px; padding-right:10px;">
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
              <b>Contacto:</b> ${props.Contacto}
            </div>`;

        if (props.Imagen && props.Imagen.startsWith('http')) {
          popup += `
            <div>
              <a href="${props.Imagen}" target="_blank" title="Ver imagen grande">
                <img src="${props.Imagen}" style="width:120px; height:auto; border-radius: 4px; box-shadow: 0 0 6px #aaa;" />
              </a>
            </div>`;
        }

        popup += `</div>`;
        layer.bindPopup(popup);
      },
      style: {
        color: "#0078FF",
        weight: 2,
        fillColor: "#0078FF",
        fillOpacity: 0.2
      }
    }).addTo(mapa);
  })
  .catch(error => {
    console.error('Error al cargar el GeoJSON:', error);
  });
