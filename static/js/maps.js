'use strict';
//allows users to have a birds eye view of the zipcode where they consider investing
function initMap() {
  const sfCoords = {
    lat: 37.787994,
    lng: -122.407437,
  };
    const map = new google.maps.Map(document.querySelector('#ggmap'),
    {center: sfCoords,
      zoom: 15,
    });
    const btn = document.querySelector('#btn-search');
btn.addEventListener('click', (e) => {
  e.preventDefault();
  const input = document.querySelector('#ggm-btn');
  // https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/search_event
  const userAddress = input.value;
  console.log(userAddress);
  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({address: userAddress}, (results, status) =>{
    if(status==='OK'){
      
      const userLocation = results[0].geometry.location;
      const markers = new google.maps.Marker({
        position: userLocation,
        map,
      });
      markers.setVisible(true);
      map.setCenter(userLocation);
      map.setZoom(15);
    } else { 
      alert(`Location was not found for the following reason: ${status}`)
    }
  });
});
 }
  