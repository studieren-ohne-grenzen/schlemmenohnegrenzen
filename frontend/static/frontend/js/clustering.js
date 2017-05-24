function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

function draw_map(jsonstr) {
    var mymap = L.map('mapid').setView([49.012588, 8.403000], 13);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(mymap);

    var numOfClusters = jsonstr.length / 9;

    for (i = 0; i < numOfClusters; i++) {
        currColor = getRandomColor();
        var currList = []
        for (j = 0; j < jsonstr.length; j++) {
            if (jsonstr[j].cluster == i) {
                currList.push([jsonstr[j].latitude, jsonstr[j].longitude]);
                L.circle([jsonstr[j].latitude, jsonstr[j].longitude], {color: currColor, fillColor: currColor, fillOpacity: 0.5, radius: 40}).bindPopup(jsonstr[j].name1 + "<br>" + jsonstr[j].name2 + "<br>" + jsonstr[j].street + "<br>Cluster: " + jsonstr[j].cluster).addTo(mymap);
            }
        }
        console.log(getRandomColor())
        L.polygon(currList, {color: currColor}).addTo(mymap);
    }
}
