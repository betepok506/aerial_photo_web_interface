function load_map() {

    var mapOptions = {
        center: [46.1874, 48.4088],
        zoom: 8,
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        minZoom: 1,
        maxZoom: 24
    }

    var map = new L.map('map', mapOptions); // Creating a map object
    map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.


    [base_maps, overlays] = load_layer(map)

    // create the sidebar instance and add it to the map
    var sidebar = L.control.sidebar({
        autopan: true,
        closeButton: true,
        position: 'left',
        container: 'sidebar'
    }).addTo(map);


    L.control.layers(base_maps, overlays).addTo(map);
    L.control.mousePosition().addTo(map);
    L.control.scale().addTo(map);
    base_maps["OpenStreetMap"].addTo(map);

    add_events_to_map(map);
}

function load_layer(map) {
    L.TileLayer.DynamicParams = L.TileLayer.extend({
        getTileUrl: function(coords) {
            return generateTileUrl(this._url, coords);
        }
    });
    
    var base_layer = new L.TileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
    })
    var google_layer = new L.tileLayer('http://{s}.google.com/vt?lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    })

    var base_maps = {
        "OpenStreetMap": base_layer,
        "Google спутник": google_layer
    }

    // L.TileLayer.DynamicParams = L.TileLayer.extend({
    //     getTileUrl: function(coords) {
    //         return generateTileUrl(this._url, coords);
    //     }
    // });

    const tileUrl = 'http://localhost:8001/api/v1/tile/get_tiles_by_coordinates/?z={z}&x={x}&y={y}';

    overlayLayer = new L.TileLayer.DynamicParams(tileUrl, {
        tms: true,
        maxZoom: 12,
        getTileUrl: function(coords) {
            return generateTileUrl(tileUrl, coords);
        }
    })

    var overlays = {
        "Обнаруженные объекты": overlayLayer
    }

    // var overlays = {
    //     "Google спутник": new L.tileLayer('http://{s}.google.com/vt?lyrs=s&x={x}&y={y}&z={z}', {
    //         maxZoom: 20,
    //         subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    //     }),

    //     // "Серая": new L.TileLayer('http://tile.openstreetmap.bzh/br/{z}/{x}/{y}.png', {
    //     //     maxZoom: 24,
    //     //     opacity: 0.5
    //     // }),
    //     "Landsat 8": new L.TileLayer('http://localhost:8001/api/v1/tile/get_tiles_by_coordinates/?z={z}&x={x}&y={y}', {
    //         tms: true,
    //         // minZoom: 9,
    //         maxZoom: 12,
    //     }),

    //     "Landsat dinamic": new L.TileLayer.DynamicParams(tileUrl, {
    //         tms: true,
    //         // minZoom: 9,
    //         maxZoom: 12,
    //         // tileUrlFunction: function(coords) {
    //         //     return generateTileUrl(tileUrl, coords);
    //         // },
    //         getTileUrl: function(coords) {
    //             return generateTileUrl(tileUrl, coords);
    //         }
    //     }),
    // };
    map.addLayer(overlayLayer);
    return [base_maps, overlays]
}

function generateTileUrl(tileUrl, coords) {
    // console.log(coords);
    
    const type_obj = getDynamicParams();
    const { x, y, z } = coords;
    let url = tileUrl
        .replace('{z}', z)
        .replace('{x}', x)
        .replace('{y}', y);

    // Создаем URL объект для удобного добавления параметров
    const urlObj = new URL(url, window.location.origin);
    // const url = new URL(tileUrl);
    urlObj.searchParams.append('type_obj', type_obj);
    // url.searchParams.append('timestamp', dynamicParams.timestamp);
    console.log(urlObj.toString())
    return urlObj.toString();

}

function getDynamicParams() {
    var divsFiltered = document.getElementById('sidebar-object-filter').querySelectorAll('input.form-check-input')
    var type_obj = null;
    divsFiltered.forEach(div => {
        console.log(div.id + div.checked);
        if (div.checked) {
            type_obj = div.id;
        }
    });
    return type_obj;
}

function add_events_to_map(map) {
    map.on('zoomend', function () {
        // get_bound_map(this);
    });

    map.on('moveend', function () {
        // get_bound_map(this);
    });
}


function clearMap(map) {
    for (i in map._layers) {
        if (map._layers[i]._path != undefined) {
            try {
                map.removeLayer(map._layers[i]);
            }
            catch (e) {
                console.log("problem with " + e + map._layers[i]);
            }
        }
    }
}
