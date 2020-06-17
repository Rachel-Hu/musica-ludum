from midiutil import MIDIFile

# source: https://en.wikipedia.org/wiki/Scientific_pitch_notation
pitch_dict = {  'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
                'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
                'C5': 72, 'D5': 74, 'E5': 76,
                "F3s":54, "G3s":56, "A3s":58,
                "C4s":61, "D4s":63, "F4s":66, "G4s":68, "A4s":70, "C5s":73, "D5s":75}

def write_midi(melody, id):
    old_pitch_list = melody.strip().split(' ')
    pitch_list = []
    for i in range(len(old_pitch_list)):
        if i % 2 == 0:
            pitch_list.append(old_pitch_list[i])
    # return pitch_list
    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track
    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track" + str(id))
    mf.addTempo(track, time, 120)
    # add some notes
    channel = 0
    volume = 100
    for note in pitch_list:
        pitch = pitch_dict[note]
        duration = 1         # 1 beat long
        mf.addNote(track, channel, pitch, time, duration, volume)
        time += 2
    # write it to disk
    with open("/home/ubuntu/team15/midi/record/" + str(id) + '.txt', 'w') as outtxt:
        for pitch in pitch_list:
            outtxt.write("%s\n" % pitch)
    midi_name = str(id) + ".mid"
    with open("/home/ubuntu/team15/midi/" + midi_name, 'wb') as outf:
        mf.writeFile(outf)
    return midi_name
