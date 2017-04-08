
var ws=new WebSocket("ws://localhost:8888/ws");

$(document).ready(function () {

    ws.onopen = function () {
        console.log("websocket engage");
        ws.send("hi from js");
    };

    ws.onmessage = function(evt){
        //the received content is in evt.data, set it where you want
        console.log("msg from ws server:" + evt.data);
    };

    ws.onclose = function () {
        console.log("connection closed");
    };

    // $(".column li").on("mouseup")  //the function  that sends data
    // {
    //     pid = $(this).attr("id");
    //     oldCid = $(this).parent().parent().attr("id");
    //     newCid = $(this).parent().attr("id");
    //     message = pid + " " + oldCid + " " + newCid;
    //     ws.send(message);   
    // };

    
});



