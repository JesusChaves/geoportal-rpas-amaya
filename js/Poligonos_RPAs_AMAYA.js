fetch('../Poligonos_RPAS.json')
  .then(response => response.json())
  .then(data => {
    const puntosPane = map.createPane("puntosPane");
    puntosPane.style.zIndex = 650;

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

    // Añadir polígonos
    const geojsonLayer = L.geoJSON(data, {
      style: function (feature) {
        const dep = feature.properties.Departamento || "RESTO";
        return {
          color: "#FF0000",
          weight: 2,
          fillColor: fillColors[dep] || fillColors["RESTO"],
          fillOpacity: 0.2
        };
      }
    }).addTo(map);

    // Añadir puntos (centroide) + popups
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

      const p = feature.properties;

      const popupContent = `
        <div style="display:flex; flex-direction:row;">
          <div style="padding-right:10px;">
            <b>Nombre:</b> ${p.Nombre}<br>
            <b>Fecha:</b> ${p.Fecha}<br>
            <b>Localidad:</b> ${p.Localidad}<br>
            <b>Descripción:</b> ${p.Descripcion}<br>
            <b>Taxón:</b> ${p.Taxon}<br>
            <b>Departamento:</b> ${p.Departamento}<br>
            <b>Tipo de Vuelo:</b> ${p.Tipo_Vuelo}<br>
            <b>Piloto:</b> ${p.Piloto}<br>
            <b>Dron:</b> ${p.Dron}<br>
            <b>Sensor:</b> ${p.Sensor}<br>
            <b>Altura Vuelo:</b> ${p.Altura_Vuelo} m<br>
            <b>GSD:</b> ${p.GSD} cm/px<br>
            <b>Contacto:</b> ${p.Contacto}<br>
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

// Función para mostrar imagen ampliada en pantalla
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
