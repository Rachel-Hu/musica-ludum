import os
from magenta.models.performance_rnn import performance_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

import magenta.music as mm
# Necessary until pyfluidsynth is updated (>1.2.5).
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# source: https://en.wikipedia.org/wiki/Scientific_pitch_notation
pitch_dict = {  'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
                'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
                'C5': 72, 'D5': 74, 'E5': 76,
                "F3s":54, "G3s":56, "A3s":58,
                "C4s":61, "D4s":63, "F4s":66, "G4s":68, "A4s":70, "C5s":73, "D5s":75}

def performance_rnn(record_file):
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

    input_sequence = melody_sequence
    num_steps = 8192 # change this for shorter or longer sequences
    temperature = 1.0 # the higher the temperature the more random the sequence.

    bundle = mm.sequence_generator_bundle.read_bundle_file('/home/ubuntu/team15/bundle/performance_with_dynamics.mag')
    generator_map = performance_sequence_generator.get_generator_map()
    generator = generator_map['performance_with_dynamics'](checkpoint=None, bundle=bundle)
    generator.initialize()

    # Derive the total number of seconds to generate.
    seconds_per_step = 1.0 / generator.steps_per_second
    generate_end_time = num_steps * seconds_per_step

    # Specify start/stop time for generation based on starting generation at the
    # end of the priming sequence and continuing until the sequence is num_steps
    # long.
    generator_options = generator_pb2.GeneratorOptions()
    # Set the start time to begin when the last note ends.
    generate_section = generator_options.generate_sections.add(
        start_time=input_sequence.total_time,
        end_time=generate_end_time)

    generator_options.args['temperature'].float_value = 1.0  # Higher is more random; 1.0 is default. 

    sequence = generator.generate(input_sequence, generator_options)

    new_file_name = record_file.split('/')[-1].split('.')[0] + '_performance_rnn.mid'
    mm.sequence_proto_to_midi_file(sequence, '/home/ubuntu/team15/midi/performance_rnn/' + new_file_name)
    return new_file_name
