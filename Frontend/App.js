document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([51.505, -0.09], 13); // Initial coordinates and zoom level for the map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    var dot = L.circleMarker([51.505, -0.09], {
        radius: 10,
        fillColor: "#ff7800",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    }).addTo(map);

    var speed = 1e-6; // Initial speed factor for movement

    function moveDot(e) {
        var currentPos = dot.getLatLng();
        switch (e.key) {
            case "ArrowUp":    currentPos.lat += speed; break;
            case "ArrowDown":  currentPos.lat -= speed; break;
            case "ArrowLeft":  currentPos.lng -= speed; break;
            case "ArrowRight": currentPos.lng += speed; break;
            case "w": case "W": // Increase speed
                speed = Math.min(1e-3, speed + 5e-6);
                break;
            case "s": case "S": // Decrease speed
                speed = Math.max(0.0001, speed -5e-6);
                break;
            default: return; // Exit this handler for other keys
        }
        dot.setLatLng(currentPos);
        map.panTo(currentPos);
    }

    document.addEventListener('keydown', moveDot);
});
