$(document).ready(function () {

    //AJAX控制获取用户输入并且传给后端
    $("#douyin-button").click(function () {
        var requestData = {'id': $("#douyin-user-id").val()};
        $.ajax({
            url: "/api/douyin",
            dataType: "json",
            data: $.param(requestData),
            type: "GET",
            success: function (response) {
                console.log("请求成功");
                console.log(response);
                var authorId = response.user_info.douyin_id;
                var authorDesc = response.user_infoauthor_desc;
                var nickname = response.user_info.nickname;
                var list = response.user_info.aweme_list;
                //获取作者的id，作者昵称，作者简介
                $("#response-user-id").append(authorId);
                $("#nickname").append(nickname);
                $("#user-desc").append(authorDesc);

                //新建新的节点获取作品的简介，作者的URL
                list.forEach(function (item_list) {
                    var treeH = document.createElement("tr");
                    var treeNode_des = document.createElement("td");
                    treeNode_des.innerText = item_list.description;
                    treeH.appendChild(treeNode_des);
                    var treeNode_url = document.createElement("td");
                    treeNode_url.innerText = item_list.url;
                    treeH.appendChild(treeNode_url);
                    document.getElementById("list-body").appendChild(treeH);
                    // for (item in item_list){
                    //     console.log(item.description);
                    //     console.log(item.url);


                    // }

                })
            },
            error: function () {
                alert("请求出错");
                window.location.reload();
            },

        })

    });

    $("#tiktok-button").click(function () {
        var requestData = {'id': $("#tiktok-user-id").val()};
        $.ajax({
            url: "/api/tiktok",
            dataType: "json",
            data: JSON.stringify(requestData),
            type: "GET",
            success: function (response) {
                console.log("请求成功");
                console.log(response);
                var authorId = response["douyin_id"];
                var uId = response["id"];
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