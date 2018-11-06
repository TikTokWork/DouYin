$(document).ready(function () {

    //AJAX控制获取用户输入并且传给后端
    $("#douyin-button").mouseover(function () {
        $.css("background", "red");
    }).click(function () {
        $.css("background", "blue");
        var requestData = {'id': $("#douyin-user-id").val()};
        $.ajax({
            url: "http://localhost:5000/api/douyin",
            dataType: "json",
            data: JSON.stringify(requestData),
            type: "GET",
            success: function (response) {
                alert("请求成功");
                var authorId = response["id"];
                var authorDesc = response["author_desc"];
                var nickname = response["nickname"];
                var list = response["aweme_list"];
                //获取作者的id，作者昵称，作者简介
                $("#response-user-id").append(authorId);
                $("#nickname").append(nickname);
                $("#user-desc").append(authorDesc);

                //新建新的节点获取作品的简介，作者的URL
                list.forEach(function (object) {
                    var treeH = document.createElement("tr");
                    for (i in object){
                        var treeNode = document.createElement("td");
                        treeNode.innerText = i;
                        treeH.appendChild(treeNode);
                    }
                    $("#list-body").appendChild(treeH);
                })
            },
            error: function () {
                alert("请求出错");
                window.location.reload();
            },

        })

    });

    $("#tiktok-button").mouseover(function () {
        $.css("background", "red");
    }).click(function () {
        $.css("background", "blue");
        var requestData = {'id': $("#tiktok-user-id").val()};
        $.ajax({
            url: "/api/tiktok",
            dataType: "json",
            data: JSON.stringify(requestData),
            type: "GET",
            success: function (response) {
                alert("请求成功");
                var authorId = response["id"];
                var authorDesc = response["author_desc"];
                var nickname = response["nickname"];
                var list = response["aweme_list"];
                //获取作者的id，作者昵称，作者简介
                $("#response-user-id").append(authorId);
                $("#nickname").append(nickname);
                $("#user-desc").append(authorDesc);

                //新建新的节点获取作品的简介，作者的URL
                list.forEach(function (object) {
                    var treeH = document.createElement("tr");
                    for (i in object){
                        var treeNode = document.createElement("td");
                        treeNode.innerText = i;
                        treeH.appendChild(treeNode);
                    }
                    $("#list-body").appendChild(treeH);
                })
            },
            error: function () {
                alert("请求出错");
                window.location.reload();
            },

        })


    });

});