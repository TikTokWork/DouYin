$(document).ready(function () {

    //AJAX控制获取用户输入并且传给后端
    $("#douyin-button").mouseover(function () {
        $.css("background", "red");
    }).click(function () {
        $.css("background", "blue");
        var data_douyin = {'user_id': $("#douyin-user-id").val()};
        $.getJSON('/api', data_douyin, function (json_object) {

        })

    });

    $("#tiktok-button").mouseover(function () {
        $.css("background", "red");
    }).click(function () {
        $.css("background", "blue");
        var data_tiktok = {'user_id': $("#douyin-user-id").val()};
        $.getJSON('/api', data_tiktok, function (json_object) {

        })


    });
});