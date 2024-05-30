
var validateFunctions = {
    "polygon-name": { "func": textareaValidation, "error_message": "Введите название полигона" },
    "polygon-coordinates": { "func": textareaValidation, "error_message": "Выберите полигон на карте" },
    "date-from": { "func": dateValidation, "error_message": "Выберите дату" },
    "date-to": { "func": dateValidation, "error_message": "Выберите дату" },
    "download-to": { "func": dateValidation, "error_message": "Выберите дату" },
};

var map;
var currentPolygon;
var drawnItems;

document.addEventListener("DOMContentLoaded", function () {
    AddingFormSubmissionHandler();
    addMap();
    loadData();
    addButtonHandler();
});

function addButtonHandler(){
    var goBackButton = document.getElementById('button-back');
    // Добавляем обработчик события при нажатии на кнопку
    goBackButton.addEventListener('click', function() {
        // Переходим на предыдущую страницу
        window.history.back();
    });
}

function loadData() {
    /* Фунция для загрузки данных новости при редактировании */
    polygon_id = document.getElementById("polygon-id").value;
    console.log(polygon_id);
    if (!(polygon_id === null || polygon_id === undefined || polygon_id === 'null')) {
        // event_id = parseInt(event_id);
        console.log("not null");
        fetch('/get_polygon?polygon_id=' + polygon_id, { //Пофиксить на адресс сервера
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();

            }).then(data => {

                polygon_name = document.getElementById("polygon-name");
                polygon_name.value = data['name'];

               if (currentPolygon) {
                    drawnItems.removeLayer(currentPolygon);
                }
                currentPolygon = L.polygon(data['footprint'], { color: 'blue' }).addTo(map);
                drawnItems.addLayer(currentPolygon);

                console.log(currentPolygon.getBounds());
                map.fitBounds(currentPolygon.getBounds());
                updatePolygonInput();


                date_from = document.getElementById("date-from");
                date = new Date(data['start_time']);
                year = date.getFullYear();
                month = String(date.getMonth() + 1).padStart(2, '0');
                day = String(date.getDate()).padStart(2, '0');
                formattedDate = `${year}-${month}-${day}`;
                date_from.value = formattedDate;

                date_to = document.getElementById("date-to");
                date = new Date(data['end_time']);
                year = date.getFullYear();
                month = String(date.getMonth() + 1).padStart(2, '0');
                day = String(date.getDate()).padStart(2, '0');
                formattedDate = `${year}-${month}-${day}`;
                date_to.value = formattedDate;


                download_to = document.getElementById("download-to");
                date = new Date(data['download_to']);
                year = date.getFullYear();
                month = String(date.getMonth() + 1).padStart(2, '0');
                day = String(date.getDate()).padStart(2, '0');
                formattedDate = `${year}-${month}-${day}`;
                download_to.value = formattedDate;
                // Изменяем кнопку
                button_submit = document.getElementById("button-submit-form");
                button_submit.innerText = 'Сохранить';

            })
            .catch(error => {
                console.error('There was an error with form submission:', error);
            });
    }
}



function addMap() {
    var mapOptions = {
        center: [54.187558, 45.177761],
        zoom: 16,
        attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
        minZoom: 10,
        maxZoom: 20
    }

    map = new L.map('map2', mapOptions); // Creating a map object
    map.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

    // var sidebarDiv = document.getElementById('sidebar');
    base_maps = load_layer()
    L.control.mousePosition().addTo(map);
    base_maps["OpenStreetMap"].addTo(map);

    drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            remove: true
        },
        draw: {
            polygon: {
            showArea: true,
                icon: new L.DivIcon({
                        iconSize: [10, 10],
                        className: 'leaflet-div-icon leaflet-editing-icon'
                    })
                },
            polyline: false,
            rectangle: false,
            circle: false,
            circlemarker: false,
            marker: false,
            point: false
        }
    });
    map.addControl(drawControl);
    currentPolygon = null;
    map.on(L.Draw.Event.CREATED, function (event) {
            if (currentPolygon) {
            drawnItems.removeLayer(currentPolygon);
        }
        var layer = event.layer;
        currentPolygon = layer;
        drawnItems.addLayer(layer);
        updatePolygonInput();
    });
    map.on(L.Draw.Event.DRAWSTART, function (event) {
            if (currentPolygon) {
            drawnItems.removeLayer(currentPolygon);
        }
    });

    map.on(L.Draw.Event.DELETED, function () {
        updatePolygonInput();
    });

    map.on('draw:edited', function (event) {
        updatePolygonInput();
    });
}

    function updatePolygonInput() {
        var latLngs = [];
        drawnItems.eachLayer(function (layer) {
            var latLngArray = [];

            layer.getLatLngs()[0].forEach(function (latLng) {
                latLngArray.push([latLng.lat, latLng.lng]);
            });
            latLngs.push(latLngArray);
        });
        document.getElementById('polygon-coordinates').value = JSON.stringify(latLngs)
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



function AddingFormSubmissionHandler() {
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(form => {
        form.querySelectorAll('.form-control').forEach(field => {
            field.addEventListener('blur', () => {
                validateField(field);
            });
        });
    });

    document.getElementById("formPolygonCreate").addEventListener("submit", function (event) {
        event.preventDefault();
        var form = event.target;

        // Валидация полей формы
        var isValid = true;
        form.querySelectorAll('.form-control').forEach(field => {
            // if (isDisplayed(field)) {
                console.log('Валидирую поле: ', field)
                result = validateField(field);
                isValid &= validateField(field);
            // }
        });

        if (!isValid) {
            console.log('Валидация не пройдена!')
            return;
        }

        polygon_name = form.elements["polygon-name"].value;

        polygon_coordinates = form.elements["polygon-coordinates"].value;
//        polygon_coordinates = event_coordinates.split(", ");
//        polygon_coordinates = {
//            "lng": parseFloat(event_coordinates[1]),
//            'lat': parseFloat(event_coordinates[0])
//        }
        console.log('Start from time ' + form.elements["date-from"].value)
        date_from = form.elements["date-from"].value;
        date_to = form.elements["date-to"].value;
        download_to = form.elements["download-to"].value;

        polygon_id = document.getElementById("polygon-id").value;
        console.log(form.elements);

        var requestData = {
            "polygon_id": polygon_id,
            "name": polygon_name,
            "footprint": polygon_coordinates,
            "start_time": date_from,
            "end_time": date_to,
            "download_to": download_to
        }

        console.log(requestData)
        fetch('/create_polygon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                window.location.href = "/polygons";
                // Обработка успешного ответа
                console.log('Form submitted successfully');
            })
            .catch(error => {
                console.error('There was an error with form submission:', error);
            });
    });
}

function isDisplayed(element) {
    while (element) {
        var computedStyle = window.getComputedStyle(element);
        if (computedStyle.getPropertyValue('display') === 'none') {
            return false;
        }
        element = element.parentElement;
    }
    return true;
}


/* функции для валидации формы */

function validateField(field) {
    // const error = field.parentElement.querySelector('.invalid-feedback');
    var isValid = true
    var selectedFunction = validateFunctions[field.getAttribute('name')]["func"];
    error_message = validateFunctions[field.getAttribute('name')]["error_message"];
    if (selectedFunction(field)) {
        divMessage = successMessage('Успешно!');
        field.classList.remove('is-invalid');
    } else {
        divMessage = errorMessage(error_message);
        field.classList.add('is-invalid');
        isValid = false;
    }
    addValidMessage(field.parentNode, divMessage, ['.valid-feedback', '.invalid-feedback'])
    return isValid;
}

function fieldValidationStub(field) {
    /* Функция-заглушка для валидации полей. Возвращает всегда true не зависимо от значения поля */
    return true;
}

function dateValidation(field) {
    /* Фунция для валидации даты */
    // console.log('Значение даты: ' + field.value);
    if (field.value.trim() !== "") {
        return true;
    } else {
        return false;
    }

}
function selectedValidation(field) {
    // console.log('Выбор группы: ' + field.value)
    if (field.value.trim() !== "") {
        return true;
    } else {
        return false;
    }
}

function textareaValidation(field) {
    if (field.value.trim() !== "") {
        return true;
    } else {
        return false;
    }
}

function validationPositiveNumbers(field) {
    // console.log('Значение чисел: ' + field.value);
    if (field.value.trim() !== "" && field.value >= 0) {
        return true;
    } else {
        return false;
    }
}

function addValidMessage(node, elementAdded, listClassesDeleted) {
    for (var i = 0; i < listClassesDeleted.length; i++) {
        var elementToRemove = node.querySelector(listClassesDeleted[i]);
        if (elementToRemove) {
            elementToRemove.remove();
        }
    }
    node.appendChild(elementAdded);
}

function successMessage(message) {
    const div = document.createElement("div");
    div.classList.add("valid-feedback");
    div.textContent = message;
    return div;
}

function errorMessage(message) {
    const div = document.createElement("div");
    div.classList.add("invalid-feedback");
    div.textContent = message;
    return div;
}