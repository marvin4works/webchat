// var loc = window.location, new_uri;
// if (loc.protocol === "https:") {
//     new_uri = "wss:";
// } else {
//     new_uri = "ws:";

var ws=new WebSocket("ws://" + window.location.host + "/ws");

var btn_sendmsg = $( "#sendmsg" ); 
var txt_newmsg = $("#new_msg");
btn_sendmsg.prop("disabled", true);




$(document).ready(function () {

    ws.onopen = function () {
        console.log("websocket engage");
        ws.send(WS_KEY);
        btn_sendmsg.prop("disabled", false);
        
    };

    ws.onmessage = function(evt){
        //the received content is in evt.data, set it where you want
        console.log("msg from ws server:" + evt.data);
        //new msg show in text panel, just need to change the mvvc
        data_json = $.parseJSON(evt.data);
        console.log(data_json);
        data_json.self = data_json.name == USER_ID; 
        model.data.push(data_json);

        
    };

    ws.onclose = function () {
        console.log("connection closed");
        btn_sendmsg.prop("disabled", true);
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

var send_msg = function(msg){
    to_send = txt_newmsg.val()
    console.log("btn send msg clicked" + txt_newmsg.val());
    //ws.send('say', {name:'foo', text:'baa'});
    if (to_send != ""){
        ws.send(to_send);
        txt_newmsg.val("");
    }
    
}

btn_sendmsg.bind( "click", send_msg);

txt_newmsg.keyup(function(e){
    if(e.keyCode == 13) send_msg();
});

