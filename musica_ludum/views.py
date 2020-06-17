from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, Http404

from django.urls import reverse

from django.core.files import File

from musica_ludum.models import Composition
from musica_ludum.forms import LoginForm, RegistrationForm
from musica_ludum.writemidi import write_midi
from musica_ludum.melodyRNN import melody_rnn
from musica_ludum.performanceRNN import performance_rnn

import os
from wsgiref.util import FileWrapper
import boto

REGION_HOST = 's3.us-east-2.amazonaws.com'
conn = boto.connect_s3('AKIAQ6HP5ZCZWJGKBP62', '7RqVWISEho1MohjMSGQOdihq4WV0Z6lp/CbRdcAp', host=REGION_HOST)

@login_required
def free_mode(request):
    context = {}
    context['username'] = request.user
    return render(request, 'musica_ludum/free.html', context)

@login_required
def game_mode(request):
    context = {}
    context['username'] = request.user
    return render(request, 'musica_ludum/game.html', context)

@login_required
def dashboard(request):
    context = {}
    midi_exists = Composition.objects.filter(user=request.user).exists()
    if midi_exists:
        midis = Composition.objects.filter(user=request.user)
        context['midis'] = midis
    context['username'] = request.user
    return render(request, 'musica_ludum/dashboard.html', context)

@login_required
def singlegame_mode(request):
    context = {}
    context['username'] = request.user
    #all_items = Post.objects.all().order_by('-time')
    return render(request, 'musica_ludum/singlegame.html', context)

@login_required
def get_key(request, audio):
    # audio_name = "./musica_ludum/static/musica_ludum/MusicLib/piano/" + audio
    # print(key)
    # key_audio = open(audio_name, "rb")
    # response = HttpResponse()
    # response.write(key_audio.read())
    # response['Content-Type'] ='audio/mp3'
    # # Store meta key info in session too.
    # if 'record' in request.session:
    #     if not request.session['melody'] and request.session['record']:
    #         request.session['melody'] = key
    #     elif request.session['melody'] and request.session['record']:
    #         request.session['melody'] = request.session['melody'] + ' ' + key
    # return response
    # Download file from aws s3
    audio_name = "piano/" + audio
    note = audio.split('.')[0]
    bucket_name = 'musica-ludum-midis'
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(audio_name)
    print(key.name)
    key.get_contents_to_filename('/home/ubuntu/team15/tmp/'+key.name)
    key_audio = open('/home/ubuntu/team15/tmp/'+audio_name, "rb")
    response = HttpResponse()
    response.write(key_audio.read())
    response['Content-Type'] ='audio/mp3'
    # Store meta key info in session too.
    if 'record' in request.session:
        if not request.session['melody'] and request.session['record']:
            request.session['melody'] = note
        elif request.session['melody'] and request.session['record']:
            request.session['melody'] = request.session['melody'] + ' ' + note
    return response

@login_required
def record(request):
    if 'record' not in request.session:
        request.session['record'] = True
    else:
        request.session['record'] = not request.session['record']
    if 'melody' not in request.session:
        request.session['melody'] = []
    if request.session['melody'] and not request.session['record']:
        print(request.session['melody'])
        # Need pip install for midi
        # Default name of new midi file is its number.
        # Could be renamed later.
        midi_exists = Composition.objects.exists()
        if midi_exists:
            last_midi = Composition.objects.all().order_by("-id")[0]
            id = last_midi.id + 1
        else:
            id = 0
        midi = write_midi(request.session['melody'], id)
        new_piece = Composition(user=request.user, piece_name=midi)
        new_piece.save()
        print(new_piece.piece_name)
        request.session['melody'] = '' 
    return HttpResponse('')

@login_required
def get_midi(request, id):
    midi = get_object_or_404(Composition, id=id)
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    else:
        midi_file = '/home/ubuntu/team15/midi/' + midi.piece_name
        wrapper = FileWrapper(open(midi_file,'rb'))
        response = HttpResponse(wrapper, content_type='audio/midi')
        response['Content-Length'] = os.path.getsize(midi_file)
        response['Content-Disposition'] = "attachment; filename=" + midi.piece_name
        return response

@login_required
def rename_midi(request, id):
    midi = get_object_or_404(Composition, id=id)
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    # print(request.POST)
    if 'new-name' in request.POST:
        new_name = request.POST['new-name'] + '.mid'
        os.rename('/home/ubuntu/team15/midi/' + midi.piece_name, '/home/ubuntu/team15/midi/' + new_name)
        # Also rename txt record
        os.rename('/home/ubuntu/team15/midi/record/' + midi.piece_name.split('.')[0] + '.txt', '/home/ubuntu/team15/midi/record/' + request.POST['new-name'] + '.txt')
        midi.piece_name = new_name
        midi.save()
        # print(midi.piece_name)
    return redirect(reverse('dashboard'))

@login_required
def delete_midi(request, id):
    midi = get_object_or_404(Composition, id=id)
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    midi_file = '/home/ubuntu/team15/midi/' + midi.piece_name
    os.remove(midi_file)
    # Also remove txt record 
    os.remove('/home/ubuntu/team15/midi/record/'+ midi.piece_name.split('.')[0] + '.txt')
    midi.delete()
    return redirect(reverse('dashboard'))

@login_required
def simple_compose(request, id):
    midi = get_object_or_404(Composition, id=id)
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    record_file = '/home/ubuntu/team15/midi/record/'+ midi.piece_name.split('.')[0] + '.txt'
    simple_midi = melody_rnn(record_file)
    wrapper = FileWrapper(open('/home/ubuntu/team15/midi/melody_rnn/'+ simple_midi,'rb'))
    response = HttpResponse(wrapper, content_type='audio/midi')
    response['Content-Length'] = os.path.getsize('/home/ubuntu/team15/midi/melody_rnn/' + simple_midi)
    response['Content-Disposition'] = "attachment; filename=" + simple_midi
    midi.mrnn_name = simple_midi
    midi.save()
    return response

@login_required
def complex_compose(request, id):
    midi = get_object_or_404(Composition, id=id)
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    record_file = '/home/ubuntu/team15/midi/record/'+ midi.piece_name.split('.')[0] + '.txt'
    complex_midi = performance_rnn(record_file)
    wrapper = FileWrapper(open('/home/ubuntu/team15/midi/performance_rnn/'+ complex_midi,'rb'))
    response = HttpResponse(wrapper, content_type='audio/midi')
    response['Content-Length'] = os.path.getsize('/home/ubuntu/team15/midi/performance_rnn/' + complex_midi)
    response['Content-Disposition'] = "attachment; filename=" + complex_midi
    midi.prnn_name = complex_midi
    midi.save()
    return response 

def get_simple(request, midi):
    midi = get_object_or_404(Composition, id=int(midi))
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    if not midi.mrnn_name:
        record_file = '/home/ubuntu/team15/midi/record/'+ midi.piece_name.split('.')[0] + '.txt'
        simple_midi = melody_rnn(record_file)
        midi.mrnn_name = simple_midi
        midi.save()
        midi_name = "/home/ubuntu/team15/midi/melody_rnn/" + simple_midi
        midi_file = open(midi_name, "rb")
        response = HttpResponse()
        response.write(midi_file.read())
        response['Content-Type'] ='audio/midi'
        return response
    midi_name = "/home/ubuntu/team15/midi/melody_rnn/" + midi.mrnn_name
    midi_file = open(midi_name, "rb")
    response = HttpResponse()
    response.write(midi_file.read())
    response['Content-Type'] ='audio/midi'
    return response
    

def get_complex(request, midi):
    midi = get_object_or_404(Composition, id=int(midi))
    print('MIDI fetched from db: {}'.format(midi.piece_name))
    if not midi.piece_name:
        raise Http404
    if not midi.prnn_name:
        record_file = '/home/ubuntu/team15/midi/record/'+ midi.piece_name.split('.')[0] + '.txt'
        simple_midi = performance_rnn(record_file)
        midi.prnn_name = simple_midi
        midi.save()
        midi_name = "/home/ubuntu/team15/midi/performance_rnn/" + simple_midi
        midi_file = open(midi_name, "rb")
        response = HttpResponse()
        response.write(midi_file.read())
        response['Content-Type'] ='audio/midi'
        return response
    midi_name = "/home/ubuntu/team15/midi/performance_rnn/" + midi.prnn_name
    midi_file = open(midi_name, "rb")
    response = HttpResponse()
    response.write(midi_file.read())
    response['Content-Type'] ='audio/midi'
    return response

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'musica_ludum/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'musica_ludum/login.html', context)

    user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'musica_ludum/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'musica_ludum/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))
