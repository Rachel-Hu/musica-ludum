function play_simple(midi) {
    var midiURL = "simpleMIDI/" + midi;
    $.ajax({
        url: midiURL,
        success: function() {
            MIDIjs.play(midiURL);
        }
    });
}

function play_complex(midi) {
    var midiURL = "complexMIDI/" + midi;
    $.ajax({
        url: midiURL,
        success: function() {
            MIDIjs.play(midiURL);
        }
    });
}