function draw_map(jsonstr) {
    // TODO: Generate random colors
    var colorArray = ["#000000", "#ff0000", "#00ff00", "#0000ff", "#770077", "#007777"];

    var mymap = L.map('mapid').setView([49.012588, 8.403000], 13);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(mymap);
}