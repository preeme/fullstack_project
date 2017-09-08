function initAutocomplete(data) {
        var current = {lat: data.coords.latitude, lng: data.coords.longitude};
        let map = new google.maps.Map(document.getElementById('map'), {
        center: current,
        zoom: 15,
        mapTypeId: 'roadmap',
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU}
    });
    map.addListener('click', function(event) {
        addMarker(event.latLng, map);
    });
    // Adds a marker to the map.
    function addMarker(location, map) {
    // Add the marker at the clicked location, and add the next-available label
    // from the array of alphabetical characters.
        marker = new google.maps.Marker({
        position: location,
        map: map
        });
        var currentId = document.getElementById('user-id').value
        $.ajax({
            method: "POST",
            url: `/users/${currentId}/locations/`,
            data: {
                lat: marker.getPosition().lng(),
                lng: marker.getPosition().lat()
            }
        }).then(function(response){
            console.log(response);
        })
    }
}

navigator.geolocation.getCurrentPosition(function(data){
    localStorage.setItem('result', JSON.stringify(data))
    initAutocomplete(data)
})
