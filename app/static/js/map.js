function load_map(map){
    [base_maps, overlays] = load_layer()

    L.control.layers(base_maps, overlays).addTo(map);
    L.control.mousePosition().addTo(map);
    L.control.scale().addTo(map);
    base_maps["OpenStreetMap"].addTo(map);

    add_events_to_map(map);
}

function load_layer(){
    var base_layer =  new L.TileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
   })

  var base_maps = {
      "OpenStreetMap": base_layer
   }

   var overlays = {
        "Google Спутник": new L.TileLayer('http://localhost:8282/google_map/?z={z}&x={x}&y={y}', {
            tms: true,
            maxZoom: 24
        }),
        "Серая": new L.TileLayer('http://tile.openstreetmap.bzh/br/{z}/{x}/{y}.png', {
                maxZoom: 24,
                opacity: 0.5
          }),
        "Авто": new L.TileLayer('http://localhost:8099/auto/?z={z}&x={x}&y={y}', {
            maxZoom: 24
      })
    };

   return [base_maps, overlays]
}

function add_events_to_map(map){
    map.on('zoomend', function() {
        get_bound_map(this);
    });

    map.on('moveend', function() {
        get_bound_map(this);
    });
}

function get_bound_map(map){
    let bounds = map.getBounds();
    check_boxes = $("input[type='checkbox'][name='requested_obj']");
    var classes_request = []
    for (var i = 0; i < check_boxes.length; i++) {
        if (check_boxes[i].checked){
           classes_request.push(check_boxes[i].value);
        }
    }

    $.ajax({
        url: "/polygon_object_by_lat_lng",
        type: "POST",
        data: {
            lat_min: bounds.getSouthWest().lat,
            lng_min: bounds.getSouthWest().lng,
            lat_max: bounds.getNorthEast().lat,
            lng_max: bounds.getNorthEast().lng,
            cls_obj: classes_request
        },
        success: function (response) {
            clearMap(map);
            for (var ind in response["polygons"]) {
                L.polygon(response["polygons"][ind]).addTo(map);
            }
        },
        error: function (xhr) {
            console.log("Can't send a request to get polygons")
        }
    });
}

function get_cls_request() {

}

function clearMap(map) {
    for(i in map._layers) {
        if(map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch(e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }
}
