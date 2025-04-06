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

        // Punto definido por el usuario desde el Sheet
        const lat = parseFloat(props.LATITUD);
        const lng = parseFloat(props.LONGITUD);
        if (!isNaN(lat) && !isNaN(lng)) {
          let popup = `
            <div style="display:flex; flex-wrap:wrap;">
              <div style="min-width:240px; padding-right:10px;">
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

          // Miniatura y popup modal si imagen válida
          if (props.Imagen && props.Imagen.startsWith("http") && props.Imagen.includes("googleusercontent.com")) {
            popup += `
              <div>
                <img src="${props.Imagen}" style="width:120px; cursor:pointer; border-radius:6px;" onclick="abrirImagen('${props.Imagen}')" />
              </div>`;
          }

          popup += `</div>`;

          L.circleMarker([lat, lng], {
            radius: 5,
            fillColor: colorRelleno,
            color: "#FF0000",
            weight: 1,
            opacity: 1,
            fillOpacity: 1
          }).bindPopup(popup).addTo(mapa);
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

// Visor de imagen ampliada
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
