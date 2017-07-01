function drawMap(toasts) {
  var mymap = L.map('mapid').setView([49.012588, 8.403000], 13)
  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
    maxZoom: 18
  }).addTo(mymap)

  var photoLayer = L.photo(toasts)
  photoLayer.addLayer(toasts)
  photoLayer.addTo(mymap);
}

