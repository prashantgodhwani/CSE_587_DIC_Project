// Setting up the mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoicGdvZGh3YW4iLCJhIjoiY2xnYjh1cjd5MW96NjNmbzhnZGNza3dycCJ9.yHzDlveagH2d0ibjgpDHPQ';

// Initializing the mapbox library
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/pgodhwan/clgmt46g5002f01qs9ik47dbn',
    center: [-102.4194, 37.7749],
    zoom: 4
});

// Creating a custom marker for user location
var el = document.createElement('div');
el.className = 'marker';
el.style.backgroundImage = 'url(https://upload.wikimedia.org/wikipedia/commons/4/41/Red_circle.gif)';
el.style.backgroundSize = 'cover';
el.style.backgroundPosition = 'center';
el.style.width = '30px';
el.style.height = '30px';

// Defining variables for user marker and location
var userMarker = null;
var userLocation;

// Getting current location and setting a marker on the map
navigator.geolocation.getCurrentPosition(loc => {
    userLocation = [loc.coords.longitude, loc.coords.latitude];
    userMarker = new mapboxgl.Marker(el)
        .setLngLat(userLocation)
        .addTo(map);
    locQS = `?lat=${userLocation[1]}&long=${userLocation[0]}`;
});


// Checking if any cuisine is selected, then hiding the relevant buttons
if (localStorage.getItem('cuisines') != null && localStorage.getItem('cuisines').length > 0) {
    document.getElementById('best-nearby').style.display = "none";
    document.getElementById('feeling-lucky').style.display = "none";
}


// Setting userIDs from localStorage
let userId = '';
if (localStorage.getItem('userId') != null) {
    userId = localStorage.getItem('userId');
}


// Getting the search box
const searchBox = document.getElementById("search-box");

//host URL for the API
const HOST_URL = 'http://127.0.0.1:8000';
var restaurantMarker = null;

// Adding event listeners to the various buttons and search box
document.getElementById('best-nearby').addEventListener('click', function () {
    searchBox.style.display = "none";
    fetchRestaurants(`${HOST_URL}/api/best-nearby`, plotMap);
});
document.getElementById('explore-beyond').addEventListener('click', function () {
    searchBox.style.display = "block";
});

const searchIcon = document.querySelector('.search-icon');
const loaderIcon = document.querySelector('.loader-icon');

//call the explore beyond API on enter click
document.getElementById('query').addEventListener('keypress', function (event) {
    if (event.keyCode === 13) { // check if Enter key was pressed
        searchIcon.style.display = 'none';
        loaderIcon.style.display = 'block';
        let query = document.getElementById('query').value;
        console.log(query)
        fetchRestaurants(`${HOST_URL}/api/explore-beyond?query=${query}`, plotMap);
    }
});

document.getElementById('top-places').addEventListener('click', function () {
    searchBox.style.display = "none";
    fetchRestaurants(`${HOST_URL}/api/top-places`, plotMap, (localStorage.getItem('cuisines') == null) ? "" : localStorage.getItem('cuisines'));
});
document.getElementById('feeling-lucky').addEventListener('click', function () {
    searchBox.style.display = "none";
    fetchRestaurants(`${HOST_URL}/api/feeling-lucky`, plotMap);
});

//on map load call the topPlaces API and pass cuisines if stored in localStorage
map.on('load', () => fetchRestaurants(`${HOST_URL}/api/top-places`, plotMap, (localStorage.getItem('cuisines') == null) ? "" : localStorage.getItem('cuisines')));

currentMarkers = [];

// function to take in an array of restaurant data and plot them as markers on the map.
var plotMap = (data) => {
    // First, remove all existing markers from the map.
    if (currentMarkers.length > 0) {
        for (var i = currentMarkers.length - 1; i >= 0; i--) {
            currentMarkers[i].remove();
        }
        currentMarkers = [];
    }

    // Create a new map bounds object to fit all the markers within.
    var bounds = new mapboxgl.LngLatBounds();

    // Add a user marker to the map at the user's location.
    userMarker = new mapboxgl.Marker(el)
        .setLngLat(userLocation)
        .addTo(map);
    currentMarkers.push(userMarker);

    // Loop through each restaurant in the data array and add a marker for it.
    data.forEach(restaurant => {
        var marker = new mapboxgl.Marker()
            .setLngLat([restaurant.longitude, restaurant.latitude])
            .setPopup(new mapboxgl.Popup({
                className: 'card pad'
            })
                .setHTML(`
            <h6>${restaurant.name}</h6>
            ${restaurant.tags ? `<p class="tags">${restaurant.tags.split(';').map(tag => `<span class="badge bg-gradient-dark">${tag}</span>`).join('')}</p>` : ""}
            ${restaurant.scores ? `<p style='font-size:12px; color:red'><b><i class="fa fa-star"></i> &nbsp; ${restaurant.scores} % match</b></p>` : ""}

            ${restaurant.distance ? `<p style='font-size:12px'><b>Distance:</b> ${restaurant.distance.toFixed(2)} miles</p>` : ""}
            <div class="rating-container">
              <p style='font-size:12px'><b>Rating:</b></p>
              <div class="rating-stars">
                <select name="rating" id="rating-${restaurant.business_id}">
                    <option value="0">Select a rating</option>
                    <option value="1">1 star</option>
                    <option value="2">2 stars</option>
                    <option value="3">3 stars</option>
                    <option value="4">4 stars</option>
                    <option value="5">5 stars</option>
                </select>
              </div>
              <input type="hidden" name="rating" id="rating-${restaurant.business_id}" value="0">
            </div>
            <div class="form-group">
              <textarea class="form-control" name="review" id="review-${restaurant.business_id}" placeholder="Write a review..."></textarea>
            </div>
            <button class="btn btn-primary" onclick="submitReview('${restaurant.business_id}')">Submit Review</button>
          `))
            .addTo(map);
        currentMarkers.push(marker);

        // Extend the map bounds to include this new marker.
        bounds.extend(marker.getLngLat());
    });

    // Fit the map to the new bounds, with a padding of 100 pixels around the edges. This is to adjust map zoom level for all points to get in the view
    map.fitBounds(bounds, { padding: 100 });
}

//function to submit a review for a given business ID to the API.
submitReview = (business_id) => {
    const rating = document.getElementById(`rating-${business_id}`).value;
    const reviewText = document.getElementById(`review-${business_id}`).value;

    // Call API with business_id, rating, and reviewText as parameters
    fetch(`${HOST_URL}/api/feedback/submit-review?rating=${rating}&review=${reviewText}&businessId=${business_id}&userId=${userId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById(`rating-${business_id}`).value = 0;
            document.getElementById(`review-${business_id}`).value = "";
            alert('Feedback recorded.');
        });

}


// This function takes a URL, a plotMap function, and an optional cuisine parameter as inputs
var fetchRestaurants = (url, plotMap, cuisine = "") => {
    // Append the location query string to the URL
    let urlWithQs = url + locQS;
    // If a cuisine parameter is provided, append it to the query string
    if (cuisine.length > 0) {
        urlWithQs += `&cuisines=${cuisine}`;
    }
    // If a userId is available, append it to the query string
    if (userId.length > 0) {
        urlWithQs += `&userId=${userId}`;
    }
    // Fetch data from the API using the constructed URL with query strings
    fetch(urlWithQs)
        .then(response => response.json())
        // After the data is returned, hide the loader icon and display the search icon, then plot the data on the map using the plotMap function
        .then(data => {
            searchIcon.style.display = 'block';
            loaderIcon.style.display = 'none';
            plotMap(data.restaurants);
        });
}


