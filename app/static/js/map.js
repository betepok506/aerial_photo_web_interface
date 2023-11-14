function initial_map() {
    var mapOptions = {
        center: [54.187558, 45.177761],
        zoom: 14,
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        minZoom: 9,
        maxZoom: 18
    }

    var map = new L.map('map', mapOptions); // Creating a map object
    add_events_to_map(map);
    get_events_within_map_visibility(map);
    map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

    // create the sidebar instance and add it to the map
    var sidebar = L.control.sidebar({
        autopan: true,
        closeButton: true,
        position: 'left',
        container: 'sidebar'
    }).addTo(map);

    // var sidebarDiv = document.getElementById('sidebar');
    base_maps = load_layer()
    L.control.mousePosition().addTo(map);
    base_maps["OpenStreetMap"].addTo(map);

    // Обработчики событий для открытия и закрытия sidebar'а
    adding_buttons_handler_to_map(sidebar);

    // Обработчик добавления маркеров на карту
    function get_events_within_map_visibility(map) {
        // Получаем границы видимой области карты
        let bounds = map.getBounds();
        var ne = bounds.getNorthEast(); // Верхний правый угол
        var sw = bounds.getSouthWest(); // Нижний левый угол

        var markersLayer = L.featureGroup().addTo(map);

        var icon = L.icon({
            iconUrl: '/static/css/images/marker-red.png',
            // shadowUrl: '/static/css/images/marker.png',

            iconSize: [48, 48], // size of the icon
            // shadowSize: [50, 64], // size of the shadow-->
            // iconAnchor: [22, 94], // point of the icon which will correspond to marker's location-->
            // shadowAnchor: [4, 62],  // the same for the shadow-->
            popupAnchor: [0, -36] // point from which the popup should open relative to the iconAnchor
        });

        // Очищаем текущие маркеры
        markersLayer.clearLayers();

        // Загружаем новые данные и добавляем маркеры
        fetch('/getMarkers?neLat=' + ne.lat + '&neLng=' + ne.lng + '&swLat=' + sw.lat + '&swLng=' + sw.lng)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok, status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // console.log('Data received:', data);
                data.forEach(markerData => {

                    var marker = L.marker([markerData.lat, markerData.lng], { icon: icon }).addTo(markersLayer);

                    marker.bindPopup(`
                <div class='custom-popup'>
                  <div class='left-content'>
                    <div class='place-name'>${markerData.name}</div>
                    <div class='place-type'>${markerData.type}</div>
                    <div class='address'>${markerData.address}</div>
                    <div class='rating'>Rating: ${markerData.rating} (${markerData.reviews} reviews)</div>
                    <div class='working-hours'>Working Hours: ${markerData.workingHours}</div>
                    <div class='buttons-container'>
                      <button class='button'>Маршрут</button>
                      <button class='button'>Сайт</button>
                      <button class='button'>Телефон</button>
                    </div>
                  </div>
                  <div class='right-content'>
                     <img src='${markerData.imageUrl}' onerror="this.src='https://via.placeholder.com/300'" alt='Image'>
                  </div>
                </div>`,
                        { maxWidth: "auto" });

                    // Добавляем события при наведении на маркер
                    marker.on('mouseover', function (e) {
                        this.openPopup();
                    });

                    marker.on('mouseout', function (e) {
                        this.closePopup();
                    });

                });
            })
            .catch(error => console.error('Error fetching markers:', error));

        markersLayer.on("click", function (event) {
            sidebar.open('sidebar-map');
        });
    }

    function add_events_to_map(map) {
        /* Добавляем события на карту */

        // Событие изменения масштаба карты
        map.on('zoomend', function () {
            get_events_within_map_visibility(this);
        });

        // События перемещения по карте
        map.on('moveend', function () {
            get_events_within_map_visibility(this);
        });
    }

}

function adding_buttons_handler_to_map(sidebar) {
    // Обработчики событий для открытия и закрытия sidebar'а
    sidebar.on('opening', function (ev) {
        // var filterButtonsContainer = document.getElementById('filter-buttons-container');
        // filterButtonsContainer.classList.add('sidebar-open');
    });

    sidebar.on('closing', function (ev) {
        // var filterButtonsContainer = document.getElementById('filter-buttons-container');
        // filterButtonsContainer.classList.remove('sidebar-open');

    });
}

function load_layer() {
    let myFilter = [
        'hue:180deg',
        'invert:100%',
    ];

    var base_layer = new L.tileLayer.colorFilter('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        filter: myFilter
    })

    var base_maps = {
        "OpenStreetMap": base_layer
    }

    return base_maps;
}

// function add_events_to_map(map) {
//     /* Добавляем события на карту */

//     // Событие изменения масштаба карты
//     map.on('zoomend', function () {
//         get_events_within_map_visibility(this);
//     });

//     // События перемещения по карте
//     map.on('moveend', function () {
//         get_events_within_map_visibility(this);
//     });
// }

// function get_events_within_map_visibility(map) {
//     // Получаем границы видимой области карты
//     let bounds = map.getBounds();
//     var ne = bounds.getNorthEast(); // Верхний правый угол
//     var sw = bounds.getSouthWest(); // Нижний левый угол

//     var markersLayer = L.featureGroup().addTo(map);

//     var icon = L.icon({
//         iconUrl: '/static/css/images/marker-red.png',
//         // shadowUrl: '/static/css/images/marker.png',

//         iconSize: [48, 48], // size of the icon
//         // shadowSize: [50, 64], // size of the shadow-->
//         // iconAnchor: [22, 94], // point of the icon which will correspond to marker's location-->
//         // shadowAnchor: [4, 62],  // the same for the shadow-->
//         popupAnchor: [0, -36] // point from which the popup should open relative to the iconAnchor
//     });

//     // Очищаем текущие маркеры
//     markersLayer.clearLayers();
//     // Загружаем новые данные и добавляем маркеры
//     fetch('/getMarkers?neLat=' + ne.lat + '&neLng=' + ne.lng + '&swLat=' + sw.lat + '&swLng=' + sw.lng)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`Network response was not ok, status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('Data received:', data);
//             data.forEach(markerData => {

//                 var marker = L.marker([markerData.lat, markerData.lng], { icon: icon }).addTo(markersLayer);

//                 marker.bindPopup(`
//             <div class='custom-popup'>
//               <div class='left-content'>
//                 <div class='place-name'>${markerData.name}</div>
//                 <div class='place-type'>${markerData.type}</div>
//                 <div class='address'>${markerData.address}</div>
//                 <div class='rating'>Rating: ${markerData.rating} (${markerData.reviews} reviews)</div>
//                 <div class='working-hours'>Working Hours: ${markerData.workingHours}</div>
//                 <div class='buttons-container'>
//                   <button class='button'>Маршрут</button>
//                   <button class='button'>Сайт</button>
//                   <button class='button'>Телефон</button>
//                 </div>
//               </div>
//               <div class='right-content'>
//                  <img src='${markerData.imageUrl}' onerror="this.src='https://via.placeholder.com/300'" alt='Image'>
//               </div>
//             </div>`,
//                     { maxWidth: "auto" });

//                 // Добавляем события при наведении на маркер
//                 marker.on('mouseover', function (e) {
//                     this.openPopup();
//                 });

//                 marker.on('mouseout', function (e) {
//                     this.closePopup();
//                 });

//             });
//         })
//         .catch(error => console.error('Error fetching markers:', error));

//         markersLayer.on("click", function (event) {
//             sidebar.open('home');
//         });
//     //     url: "/polygon_object_by_lat_lng",
//     //     type: "POST",
//     //     data: {
//     //         lat_min: bounds.getSouthWest().lat,
//     //         lng_min: bounds.getSouthWest().lng,
//     //         lat_max: bounds.getNorthEast().lat,
//     //         lng_max: bounds.getNorthEast().lng,
//     //         cls_obj: classes_request
//     //     },
//     //     success: function (response) {
//     //         clearMap(map);
//     //         for (var ind in response["polygons"]) {
//     //             L.polygon(response["polygons"][ind]).addTo(map);
//     //         }
//     //     },
//     //     error: function (xhr) {
//     //         console.log("Can't send a request to get polygons")
//     //     }
//     // });
// }

// function get_cls_request() {

// }

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

function add_events_listener() {
    // add_events_buttons_to_map();
}

// function add_events_buttons_to_map() {
//     var filterButtonsContainer = document.getElementById('filter-buttons-container');
//     var arrowLeftContainer = document.getElementById('arrow-left-container');
//     var arrowRightContainer = document.getElementById('arrow-right-container');
//     var step = 50; // Регулируйте величину сдвига

//     // Влево
//     document.getElementById('arrow-left').addEventListener('click', function () {
//         filterButtonsContainer.scrollLeft -= step;
//     });

//     // Вправо
//     document.getElementById('arrow-right').addEventListener('click', function () {
//         filterButtonsContainer.scrollLeft += step;
//     });

//     // Покажите и скройте стрелочки при необходимости
//     filterButtonsContainer.addEventListener('scroll', function () {
//         arrowLeftContainer.style.visibility = 'visible';
//         arrowRightContainer.style.visibility = 'visible';
//         setTimeout(function () {
//             arrowLeftContainer.style.visibility = 'hidden';
//             arrowRightContainer.style.visibility = 'hidden';
//         }, 1000);
//     });

// }
