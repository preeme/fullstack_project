function initAutocomplete(data) {
    var current = {lat: data.coords.latitude, lng: data.coords.longitude};
    let map = new google.maps.Map(document.getElementById('map'), {
        center: current,
        zoom: 15,
        mapTypeId: 'roadmap',
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU}
    });

      var currentId = document.getElementById('user-id').value
      $.get(`/users/${currentId}/locations/data`).then(function(response){
        for (let data of response) {
          // Add the circle for this city to the map.
          var Circle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: {
                lat: data.lat,
                lng: data.lng
            },
            radius: 50
          });
      }
    })
}
navigator.geolocation.getCurrentPosition(function(data){
    localStorage.setItem('result', JSON.stringify(data))
    initAutocomplete(data)
  })
