var recording = false;
$('li.piano-key').click(function(){
    var key = this.id;
    console.log(key);
    var audioURL = "piano/" + key + ".mp3";
    $.ajax({
        url: audioURL,
        success: function() {
            $('audio #source').attr('src', audioURL);
            $('audio').get(0).load();
            $('audio').get(0).play();
        }
    });
});

$('#record').click(function(){
    recording = !recording;
    $(this).toggleClass("fa-play-circle fa-pause-circle");
    $.ajax({
        url: "record",
        success: function() {
            console.log("Start/Stop recording!");
        }
    });
    if(!recording) {
        window.location.replace("/dashboard");
    }
});