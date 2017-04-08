function downloadURL(url) {
    if( $('#idown').length ){
        $('#idown').attr('src',url);
    }else{
        $('<iframe>', { id:'idown', src:url }).hide().appendTo('body');
    }
}
