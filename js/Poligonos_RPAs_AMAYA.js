fetch('../Poligonos_RPAS.json')
  .then(response => response.json())
  .then(data => {
    const puntosPane = map.createPane("puntosPane");
    puntosPane.style.zIndex = 650; // Más alto que los polígonos

    L.geoJSON(data, {
      style: function (feature) {
        const departamento = feature.properties.Departamento || "RESTO";

        const fillColors = {
          "Cauces": "#215F9A",
          "Oficina de Proyectos": "#FFFF00",
          "Oficina Técnica": "#D86ECC",
          "Laboratorio Huelva": "#FF0000",
          "IDI": "#3B7D23",
          "UGC": "#747474",
          "OP Sevilla": "#C04F15",
          "RESTO": "#00B0F0"
        };

        return {
          color: "#FF0000", // borde siempre rojo
          weight: 2,
          fillColor: fillColors[departamento] || fillColors["RESTO"],
          fillOpacity: 0.2
        };
      },
      onEachFeature: function (feature, layer) {
        // Formatear URL imagen de Google Drive si es necesario
        let url = feature.properties.Imagen || "";
        if (url.includes("drive.google.com/open?id=")) {
          const id = url.split("id=")[1];
          url = `https://drive.google.com/uc?id=${id}`;
        }

        let popupContent = `
          <div style="display:flex; flex-direction:row;">
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
              <b>Contacto:</b> ${feature.properties.Contacto}<br>
            </div>
            <div>
              <img src="${url}" style="width:120px; height:auto; cursor:pointer; border:1px solid #ccc;" onclick="abrirImagen('${url}')" />
            </div>
          </div>
        `;
        layer.bindPopup(popupContent);
      },
      pointToLayer: function (feature, latlng) {
        // No usado aquí
        return null;
      }
    }).addTo(map);

    // Añadir puntos (centroides)
    data.features.forEach(feature => {
      const coords = feature.geometry.coordinates[0];
      const lats = coords.map(c => c[1]);
      const lngs = coords.map(c => c[0]);
      const centroide = [
        lats.reduce((a, b) => a + b, 0) / lats.length,
        lngs.reduce((a, b) => a + b, 0) / lngs.length
      ];

      let url = feature.properties.Imagen || "";
      if (url.includes("drive.google.com/open?id=")) {
        const id = url.split("id=")[1];
        url = `https://drive.google.com/uc?id=${id}`;
      }

      let popupContent = `
        <div style="display:flex; flex-direction:row;">
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
            <b>Contacto:</b> ${feature.properties.Contacto}<br>
          </div>
          <div>
            <img src="${url}" style="width:120px; height:auto; cursor:pointer; border:1px solid #ccc;" onclick="abrirImagen('${url}')" />
          </div>
        </div>
      `;

      L.circleMarker(centroide, {
        radius: 4,
        fillColor: "#0000FF",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 1,
        pane: "puntosPane"
      })
      .bindPopup(popupContent)
      .addTo(map);
    });
  });

// Modal imagen en pantalla
function abrirImagen(url) {
  const overlay = document.createElement("div");
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100vw";
  overlay.style.height = "100vh";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.zIndex = "9999";

  const img = document.createElement("img");
  img.src = url;
  img.style.maxWidth = "90%";
  img.style.maxHeight = "90%";
  img.style.border = "4px solid white";
  img.style.boxShadow = "0 0 30px black";

  overlay.appendChild(img);
  document.body.appendChild(overlay);

  overlay.addEventListener("click", () => {
    document.body.removeChild(overlay);
  });
}
