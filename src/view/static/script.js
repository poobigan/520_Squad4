var selected = false;
var sourceFixed = false;
var destFixed = false;

var sourceCoordinates = "";
var destinationCoordinates = "";

var manualSourceAddress = "";
var manualDestinationAddress = "";

var limitingPercent = 0;

var shortestPathDist = 0;
var elenaPathDistance = 0;

function roundOff(number) {
    const roundedNumber = Math.round(number * 10000) / 10000;
    return roundedNumber;
  }
  

function setMapMarker(type, event) {
    const roundedLat = roundOff(event.lngLat["lat"]);
    const roundedLng = roundOff(event.lngLat["lng"]);
    
    if (type === "source") {
      const sourceElement = document.getElementById("source");
      sourceElement.innerHTML = roundedLat + "," + roundedLng;
      
      const sourceMarker = new mapboxgl.Marker({ color: "green" }).setLngLat(event.lngLat);
      sourceMarker.addTo(map);
      
      return sourceMarker;
    } else {
      const destinationElement = document.getElementById("destination");
      destinationElement.innerHTML = roundedLat + "," + roundedLng;
      
      const destinationMarker = new mapboxgl.Marker({ color: "red" }).setLngLat(event.lngLat);
      destinationMarker.addTo(map);
      
      return destinationMarker;
    }
  }
  

function enableManualAddressFields() {
    const sourceElement = document.getElementById("source_manual");
    const destinationElement = document.getElementById("desti_manual");
  
    sourceElement.classList.add("visible");
    destinationElement.classList.add("visible");
  }
  

function disableManualAddressFields() {
    const sourceElement = document.getElementById("source_manual");
    const destinationElement = document.getElementById("desti_manual");
  
    sourceElement.classList.remove("visible");
    destinationElement.classList.remove("visible");
  }
  

function enableMapAddressFields() {
    const sourceField = document.getElementById("source_map");
    const destinationField = document.getElementById("desti_map");
  
    sourceField.classList.add("visible");
    destinationField.classList.add("visible");
  }
  

function disableMapAddressFields() {
    const sourceField = document.getElementById("source_map");
    const destinationField = document.getElementById("desti_map");
  
    sourceField.classList.remove("visible");
    destinationField.classList.remove("visible");
  };

  function resetParameters() {
    selected = false;
    sourceFixed = false;
    destFixed = false;
    sourceCoordinates = "";
    destinationCoordinates = "";
    manualSourceAddress = "";
    manualDestinationAddress = "";
    limitingPercent = 0;
  
    marks = turf.featureCollection([]);
    map.getSource('circleData').setData(marks);
  
    if (sourceMarker) {
      sourceMarker.remove();
    }
    if (destMarker) {
      destMarker.remove();
    }
    document.getElementById("manualSourceAddress").value = "";
    document.getElementById("manualDestinationAddress").value = "";
  
    document.getElementById("limitingPercent").value = 0;
  
    document.getElementById("shortestPathDist").textContent = "";
    document.getElementById("shortestPathGain").textContent = "";
  
    document.getElementById("elenaPathDistance").textContent = "";
    document.getElementById("elenaPathGain").textContent = "";
  
    document.getElementById("source").textContent = "";
    document.getElementById("destination").textContent = "";
  
    disableManualAddressFields();
    disableMapAddressFields();
  
    resetOutputs();
  }
  
  

  function resetOutputs() {
    elenaPathDistance = 0;
    shortestPathDist = 0;
  
    const shortestRouteLayer = map.getLayer("shortest_route");
    if (shortestRouteLayer) {
      map.removeLayer("shortest_route");
    }
  
    const shortestRouteSource = map.getSource("shortest_route");
    if (shortestRouteSource) {
      map.removeSource("shortest_route");
    }
  
    const eleRouteLayer = map.getLayer("ele_route");
    if (eleRouteLayer) {
      map.removeLayer("ele_route");
    }
  
    const eleRouteSource = map.getSource("ele_route");
    if (eleRouteSource) {
      map.removeSource("ele_route");
    }
  }
  

document.getElementById("manual").onclick = function(){
    disableMapAddressFields();
    enableManualAddressFields();
    selected = false;
};

document.getElementById("mapselect").onclick = function(){
    disableManualAddressFields();
    enableMapAddressFields();
    selected = true;
};

document.getElementById("reset").onclick = function(){
    resetParameters();
};

document.getElementById("submit").onclick = function() {
  var algo = document.querySelector('input[name="algo"]:checked').value;
  var minimumMaximum = document.querySelector('input[name="minimumMaximum"]:checked').value;

  limitingPercent = parseFloat(document.getElementById("limitingPercent").value);

  if (limitingPercent < 0) {
    alert("Invalid input. Please input positive values.");
    return;
  }

  if (selected) {
    var submitData = {
      source_coordinates: sourceCoordinates,
      destination_coordinates: destinationCoordinates,
      minimum_maximum: minimumMaximum.toString(),
      algo: algo.toString(),
      limiting_percent: limitingPercent
    };

    submitData = JSON.stringify(submitData);

    fetch("/path_via_pointers", {
      method: "POST",
      body: submitData,
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        plotRoute(data, "select");
        calcValues(data);
      })
      .catch(function(error) {
        console.error("Error:", error);
      });

  } else {
    manualSourceAddress = document.getElementById("manualSourceAddress").value.toString();
    manualDestinationAddress = document.getElementById("manualDestinationAddress").value.toString();

    if (manualDestinationAddress.length === 0 || manualSourceAddress.length === 0) {
      window.alert("Enter valid Source and Destination Addresses!");
      return;
    }

    var submitData = {
      manual_source_address: manualSourceAddress,
      manual_destination_address: manualDestinationAddress,
      minimum_maximum: minimumMaximum.toString(),
      algo: algo.toString(),
      limiting_percent: limitingPercent
    };

    submitData = JSON.stringify(submitData);

    fetch("/path_via_address", {
      method: "POST",
      body: submitData,
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        plotRoute(data, "address");
        calcValues(data);
      })
      .catch(function(error) {
        console.error("Error:", error);
      });
  }
};


function plotRoute(data, endpoint) {
    if(data["bool_pop"] == 0 || data["bool_pop"] == 1) {
        return;
    }

    if (data["bool_pop"] === -1) {
        if (sourceMarker) {
            sourceMarker.remove();
        }
        if (destMarker) {
            destMarker.remove();
        }
        resetOutputs();
        return;
    }

    map.addSource("ele_route", {
        "type": "geojson",
        "data": data["elev_path_route"]
    });

    map.addLayer({
        "id": "ele_route",
        "type": "line",
        "source": "ele_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "Blue",
            "line-width": 4.5,
        }
    });

    map.addSource("shortest_route", {
        "type": "geojson",
        "data": data["shortest_route"]
    });

    map.addLayer({
        "id": "shortest_route",
        "type": "line",
        "source": "shortest_route",
        "layout": {
            "line-join": "round",
            "line-cap": "round"
        },
        "paint": {
            "line-color": "White",
            "line-width": 1.5
        }
    });

    calcValues(data);
}

function calcValues(data) {
    document.getElementById("shortestPathDist").innerHTML = data["shortDist"].toFixed(4) + " meters";
    document.getElementById("elenaPathDistance").innerHTML = data["elev_path_dist"].toFixed(4) + " meters";
    document.getElementById("shortestPathGain").innerHTML = data["gainShort"].toFixed(4) + " meters";
    document.getElementById("elenaPathGain").innerHTML = data["elev_path_gain"].toFixed(4) + " meters";
}

mapboxgl.accessToken = access_key;
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/navigation-night-v1',
    center: [-72.5286912, 42.3559168],
    zoom: 12,
});
var sourceMarker, destMarker;
marks = turf.featureCollection([]);

map.on("load" , function(){
    map.addSource('circleData', {
        type: 'geojson',
        data: {
        type: 'FeatureCollection',
        features: [],
        },
    });
    map.addLayer({
        id: 'data',
        type: 'circle',
        source: 'circleData',
        paint: {
        'circle-opacity' : 0.1,
        'circle-radius': 300,
        'circle-stroke-width': 2,
        'circle-stroke-color': '#333',
        },
    });
});

map.on('click', function(e){
    if(selected) {
        lngLat = new Array(e.lngLat.lng, e.lngLat.lat);
        if(!sourceFixed) {
            sourceMarker = setMapMarker('source', e);
            sourceCoordinates = JSON.stringify(e.lngLat);
            sourceFixed = true;
            map.flyTo({center: lngLat});
        } else if (!destFixed){
            destMarker = setMapMarker('destination', e);
            destinationCoordinates = JSON.stringify(e.lngLat);
            destFixed = true;
            map.flyTo({center: lngLat});
        }

    }
});
