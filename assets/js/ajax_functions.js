(function ($) {


    function list_card_in_table(card_list) {
        $("#card_list table").remove();
        $("#card_list").append("<table class=\"table\"></table>");
        $("#card_list table").append("<tr><td>Серия</td><td>Номер</td><td>Дата выпуска</td><td>Дата завершения активности</td><td>Сумма на карте</td><td>Статус карты</td><td>Активировать/Дизактивировать</td><td>Удалить</td></tr>");
        var status_card = '';
        var status_chenge_block = '';
        var delete_button = '';
        for (let value of card_list) {
            delete_button = '<button class="delete_button btn btn-danger" id="' + value.pk + '">Удалить</button>';
            if (value.card_status == 0) {
                status_card = 'Карта не активирована';
                status_chenge_block = '<input type="checkbox"  class="status_activated" type="checkbox" id=' + value.pk + ' name="status_change">';

            } else if (value.card_status == 1) {
                status_card = 'Карта активирована';
                status_chenge_block = '<input type="checkbox" class="status_activated" id=' + value.pk + ' name="status_change" checked>';

            } else {
                status_card = 'Карта просрочена';
                status_chenge_block = 'Карта просрочена';
            }
            $("#card_list table").append('<tr><td>' + value.card_series + '</td><td>' + value.card_number + '</td><td>' + value.card_issue_datetime_in_format + '</td><td>' + value.card_activity_end_datetime_in_format + '</td><td>' + value.sum_on_card + '</td><td>' + status_card + '</td>' + '</td><td>' + status_chenge_block + '</td><td>' + delete_button + '</td></tr>');
        }
        $(".status_activated").change(function () {
            if (this.checked) {
                activated_card(0, this.id);
            } else {
                activated_card(1, this.id);
            }
            get_list_cards();
        });
        $(".delete_button").on('click', function (event) {
            delete_card(this.id);
            get_list_cards();
        });
        // $(".delete_button").click(function () {
        //     delete_card(this.id);
        //     get_list_cards();
        // });
    }


    function activated_card(activated, pk) {
        $.ajax({
            type: "POST",
            url: '/api/card/activated/',
            dataType: "json",
            cache: false,
            data: {
                status_change: activated,
                pk: pk,
            },
            success: function (result) {
                get_list_cards();
            }
        });
    }

    function delete_card(pk) {
        $.ajax({
            type: "DELETE",
            url: '/api/card/',
            dataType: "json",
            cache: false,
            data: {
                pk: pk,
            },
            success: function (result) {
                get_list_cards();
            }
        });
    }

    function get_list_cards() {
        $.ajax({
            type: "GET",
            url: '/api/card/',
            dataType: "json",
            cache: false,
            success: function (result) {
                list_card_in_table(result.data);
            }
        });
    }

    $("#GenerateForm").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: '/api/card/generate/',
            data: $(this).serialize(),
            success: function (data) {
                get_list_cards();
            }
        });
    });
    $("#SearchForm").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: '/api/card/search/',
            data: $(this).serialize(),
            success: function (result) {
                list_card_in_table(result.data);
            }
        });
    });


    get_list_cards();


})
(jQuery);
