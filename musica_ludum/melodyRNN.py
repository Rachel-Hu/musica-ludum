import magenta.music as mm
import magenta
import tensorflow
from magenta.protobuf import music_pb2
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.protobuf import generator_pb2

# source: https://en.wikipedia.org/wiki/Scientific_pitch_notation
pitch_dict = {  'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
                'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
                'C5': 72, 'D5': 74, 'E5': 76,
                "F3s":54, "G3s":56, "A3s":58,
                "C4s":61, "D4s":63, "F4s":66, "G4s":68, "A4s":70, "C5s":73, "D5s":75}

def melody_rnn(record_file):
    start_time = 0.0
    timestep = 0.5
    end_time = 0.5
    melody_sequence = music_pb2.NoteSequence()
    with open(record_file, 'r') as record:
        for line in record:
            melody_sequence.notes.add(pitch=pitch_dict[line.strip()], \
                                start_time=start_time, end_time=end_time, velocity=80)
            start_time += timestep
            end_time += timestep
    melody_sequence.total_time = end_time
    melody_sequence.tempos.add(qpm=60)

    bundle = mm.sequence_generator_bundle.read_bundle_file('/home/ubuntu/team15/bundle/basic_rnn.mag')

    # Initialize the model.
    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    # Model options. Change these to get different generated sequences! 

    input_sequence = melody_sequence # change this to teapot if you want
    num_steps = 512 # change this for shorter or longer sequences
    temperature = 1.0 # the higher the temperature the more random the sequence.

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
                    if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm 
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
    start_time=last_end_time + seconds_per_step,
    end_time=total_seconds)

    # Ask the model to continue the sequence.
    sequence = melody_rnn.generate(input_sequence, generator_options)

    new_file_name = record_file.split('/')[-1].split('.')[0] + '_melody_rnn.mid'
    mm.sequence_proto_to_midi_file(sequence, '/home/ubuntu/team15/midi/melody_rnn/' + new_file_name)
    return new_file_name