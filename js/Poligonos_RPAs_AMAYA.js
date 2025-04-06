// Poligonos_RPAs_AMAYA.js

fetch('Poligonos_RPAS.json')
  .then(response => response.json())
  .then(data => {
    const coloresRelleno = {
      "Cauces": "#215F9A",
      "Oficina de Proyectos": "#FFFF00",
      "Oficina Técnica": "#D86ECC",
      "Laboratorio Huelva": "#FF0000",
      "IDI": "#3B7D23",
      "UGC": "#747474",
      "OP Sevilla": "#C04F15"
    };

    L.geoJSON(data, {
      onEachFeature: function(feature, layer) {
        const props = feature.properties;
        const colorRelleno = coloresRelleno[props.Departamento] || "#00B0F0";

        let popup = `<div style="display:flex; flex-wrap:wrap;">
          <div style="min-width:240px; padding-right:10px;">
            <b>Nombre:</b> ${props.Nombre || '—'}<br>
            <b>Fecha:</b> ${props.Fecha || '—'}<br>
            <b>Localidad:</b> ${props.Localidad || '—'}<br>
            <b>Descripción:</b> ${props.Descripcion || '—'}<br>
            <b>Taxón:</b> ${props.Taxon || '—'}<br>
            <b>Departamento:</b> ${props.Departamento || '—'}<br>
            <b>Tipo de Vuelo:</b> ${props.Tipo_Vuelo || '—'}<br>
            <b>Piloto:</b> ${props.Piloto || '—'}<br>
            <b>Dron:</b> ${props.Dron || '—'}<br>
            <b>Sensor:</b> ${props.Sensor || '—'}<br>
            <b>Altura Vuelo:</b> ${props.Altura_Vuelo || '—'} m<br>
            <b>GSD:</b> ${props.GSD || '—'} cm/px<br>
            <b>Contacto:</b> ${props.Contacto || '—'}
          </div>`;

        if (props.Imagen && props.Imagen.startsWith("http")) {
          popup += `<div>
            <img src="${props.Imagen}" 
                 style="width:120px; cursor:pointer; border-radius:6px;"
                 onclick="abrirImagen('${props.Imagen}')"
                 onerror="this.style.display='none'" />
          </div>`;
        }

        popup += `</div>`;

        if (feature.geometry.type === "Polygon") {
          const coords = feature.geometry.coordinates[0];
          const center = coords.reduce((acc, curr) => [acc[0] + curr[0], acc[1] + curr[1]], [0, 0])
            .map(x => x / coords.length);

          L.circleMarker([center[1], center[0]], {
            radius: 5,
            fillColor: colorRelleno,
            color: "#FF0000",
            weight: 1,
            opacity: 1,
            fillOpacity: 1,
            pane: "puntosPane" // Asegura que el punto reciba clics
          })
          .bindPopup(popup)
          .addTo(mapa);
        }
      },
      style: function(feature) {
        const depto = feature.properties.Departamento;
        return {
          color: "#FF0000",
          fillColor: coloresRelleno[depto] || "#00B0F0",
          fillOpacity: 0.2,
          weight: 2
        };
      }
    }).addTo(mapa);
  })
  .catch(error => {
    console.error('Error al cargar el GeoJSON:', error);
  });

function abrirImagen(url) {
  const modal = document.createElement("div");
  modal.id = "visorImagen";
  modal.style = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center;
    z-index: 10000;
  `;
  modal.innerHTML = `
    <div style="position: relative;">
      <img src="${url}" style="max-width: 90vw; max-height: 90vh; border: 3px solid white; border-radius: 6px;" />
      <span onclick="document.body.removeChild(visorImagen)" style="
        position: absolute; top: -10px; right: -10px; background: white; border-radius: 50%;
        padding: 5px; cursor: pointer; font-weight: bold;">&#10006;</span>
    </div>`;
  document.body.appendChild(modal);
}
