document.addEventListener("DOMContentLoaded", function () {
    addDeleteButtonHandler();
    addEditButtonHandler();
});


function addDeleteButtonHandler() {
    /* Функция для добавления обработчика для кнопки удаления новостей */
    $(".delete-button").click(function () {
        var cardBody = $(this).closest(".container").find(".card-id").text().trim(); // Находим ближайший родительский элемент с классом card-body
        console.log(cardBody);

        //        requestData = { "id": cardBody };
        // Отправка запроса
        fetch('/delete_polygon?polygon_id=' + cardBody, { //Пофиксить на адресс сервера
            method: 'DELETE',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                $(this).closest(".container").remove();
            })
            .catch(error => {
                console.error('There was an error with form submission:', error);
            });
    });
}

function addEditButtonHandler() {
    /* Функция для добавления обработчика редактирования записи */
    $(".edit-button").click(function () {
        var cardBody = $(this).closest(".container").find(".card-id").text().trim(); // Находим ближайший родительский элемент с классом card-body
        console.log(cardBody);
        var url = "/polygon_creation_form?polygon_id=" + cardBody;
        window.location.href = url;
    });
}