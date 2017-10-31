#!/usr/bin/python

__author__ = 'ban'
__date__ = '2016-12-18 13:01:00'
__version__ = '0.5'

# -----------------------------------------------------------------------------
# Copyright (c) 2016-2017 Bartosz Antosik (ban) for the research carried
# On Frideric Chopin University of Music in Warsaw, POLAND
# -----------------------------------------------------------------------------

import sys
import wave
import audioop
import ntpath
import os
import subprocess

import speech_recognition

SILENCE_WINDOW_FXS = 2048
SILENCE_TRESHOLD_FXS = 64  # 0..32767
SILENCE_TRAIL_FXS = 8192

SILENCE_WINDOW_SRV = 4096
SILENCE_TRESHOLD_SRV = 256
SILENCE_SUSTAIN_SRV = 4096
SILENCE_TRAIL_SRV = 22050

SAMPLE_ABS_MAX = 32767
SAMPLE_ABS_NUL = 0

RECOGNIZE_SPEECH = True

PREFIX_FXS = 'efekty'
PREFIX_SRV = 'sluchacz'
SUFFIX_NORM = 'norm'
PREFIX_LBL = 'etykiety-in'

def sampToSecs(begin, end, rate):

    return begin * (1 / rate), end * (1 / rate)

def trySpeechRecognize(chunk):

    sr = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(chunk) as source:
        audio = sr.record(source)

    try:
        return sr.recognize_google(audio, show_all=False, language='pl')
    except speech_recognition.UnknownValueError:
        return ''
    except speech_recognition.RequestError as e:
        return ''


def process(fxs_file, survey_file, tags_file):

    ch_fxs = wave.open(fxs_file, mode='rb')
    ch_survey = wave.open(survey_file, mode='rb')
    tags = open(tags_file, 'w', encoding='utf-8')

#    print(ch_survey.getnframes())
#    print(ch_survey.getsampwidth())

#    ch_survey.rewind()
#    print(audioop.avgpp(ch_survey.readframes(ch_survey.getnframes()), ch_survey.getsampwidth()))

#    ch_survey.rewind()
#    print(audioop.max(ch_survey.readframes(ch_survey.getnframes()), ch_survey.getsampwidth()))

#    sh_silence_raw = []
#    sh_audio_raw = []

#    for i in range(0, SILENCE_WINDOW_FXS):
#        sh_silence_raw.append(struct.pack('h', SAMPLE_ABS_NUL))
#        sh_audio_raw.append(struct.pack('h', SAMPLE_ABS_MAX))

#    sh_silence_str = b''.join(sh_silence_raw)
#    sh_audio_str = b''.join(sh_audio_raw)

    # -------------------------------------------------------------------------
    # Silence/Signal detection in FXs
    # -------------------------------------------------------------------------

    tags_fxs = []
    p_silence = True
    beg = 0
    last = 0

    ch_fxs.rewind()
    for s in range(ch_fxs.getnframes() // SILENCE_WINDOW_FXS):
        pos = ch_fxs.tell()

        rms = audioop.rms(ch_fxs.readframes(SILENCE_WINDOW_FXS), 2)

        if rms > SILENCE_TRESHOLD_FXS:
            if p_silence:
                beg = pos
            p_silence = False
            last = pos
        else:
            # ensure some hysteresis
            if pos > last + SILENCE_TRAIL_FXS:
                if not p_silence:
                    tags_fxs.append((beg, pos))
                p_silence = True

    # -------------------------------------------------------------------------
    # Silence/Signal detection in RESPONSES
    # -------------------------------------------------------------------------

    tags_survey = []
    p_silence = True
    p_long = False
    beg = 0
    last = 0
    lfrm = bytes()

    ch_survey.rewind()
    for s in range(ch_survey.getnframes() // SILENCE_WINDOW_SRV):
        pos = ch_survey.tell()

        frm = ch_survey.readframes(SILENCE_WINDOW_SRV)
        rms = audioop.rms(frm, 2)

        if rms > SILENCE_TRESHOLD_SRV:
            # begin audio chunk
            if p_silence:
                p_long = False
                beg = pos
                ch_chunk = wave.open('chunk.wav', mode='wb')
                ch_chunk.setparams(ch_survey.getparams())

                ch_chunk.writeframes(lfrm)

            p_silence = False
            last = pos

            if pos >= beg + SILENCE_SUSTAIN_SRV:
                p_long = True
        else:
            if p_long:
                # ensure some hysteresis
                if pos > last + SILENCE_TRAIL_SRV:
                    # end audio chunk
                    if not p_silence:
                        ch_chunk.close()

                        # skip those before first prompt
                        if pos > tags_fxs[0][0]:
                            if RECOGNIZE_SPEECH:
                                srt = trySpeechRecognize('chunk.wav')
                                if srt:
                                    tags_survey.append((beg, pos, srt))
                            else:
                                tags_survey.append((beg, pos, ''))

                    p_silence = True
            else:
                if not p_silence:
                    ch_chunk.close()

                p_silence = True

        if not p_silence:
            ch_chunk.writeframes(frm)

        lfrm = frm

    ch_chunk.close()
    os.remove('chunk.wav')

    for i, p in enumerate(tags_fxs):
        pb, pe = sampToSecs(p[0], p[1], ch_fxs.getframerate())

        print('{:.6f}\t{:.6f}\t{}'.format(pb, pe, 'prompt #' +
            str(i + 1) + ': '), file=tags)

    for i, p in enumerate(tags_survey):
        pb, pe = sampToSecs(p[0], p[1], ch_survey.getframerate())

        # Match answers to prompt numbers
        fx_id = 0
        for fn, fnn in zip(tags_fxs, tags_fxs[1:]):
            if (p[0] >= fn[0]) and (p[0] < fnn[0]):
                break
            fx_id += 1

        print('{:.6f}\t{:.6f}\t{}'.format(pb, pe, 'answer #' +
            str(fx_id + 1) + ': ' + p[2]), file=tags)

    ch_fxs.close()
    ch_survey.close()

    tags.close()

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Usage:', ntpath.basename(sys.argv[0]), 'fx_wave_file')
        exit()
    fx_file_name = sys.argv[1]
    srv_file_name = (sys.argv[1]).replace(PREFIX_FXS, PREFIX_SRV)

    fx_file_name_norm = fx_file_name.replace(
        '.wav', '-' + SUFFIX_NORM + '.wav')
    srv_file_name_norm = srv_file_name.replace(
        '.wav', '-' + SUFFIX_NORM + '.wav')

    base, ext = os.path.splitext(sys.argv[1])
    tags_file_name = base.replace(PREFIX_FXS, PREFIX_LBL) + '.txt'

    print('Summary:')
    print('')
    print('F/X prompt file: ', fx_file_name)
    print('Survey file: ', srv_file_name)
    print('Input labels file: ', tags_file_name)
    print('')
    print('F/X prompt file (norm): ', fx_file_name_norm)
    print('Survey file (norm): ', srv_file_name_norm)
    print('')

    print('Normalizing WAVs')

    sProc = subprocess.Popen('sox "' + fx_file_name +
        '" -t wavpcm -b 16 -c 1 --norm "' + fx_file_name_norm + '"',
        shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = sProc.wait()

    sProc = subprocess.Popen('sox "' + srv_file_name +
        '" -t wavpcm -b 16 -c 1 --norm "' + srv_file_name_norm + '"',
        shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = sProc.wait()

    print('Tagging WAVs')

    process(fx_file_name_norm, srv_file_name_norm, tags_file_name)

#  os.remove(fx_file_name_norm)
#  os.remove(srv_file_name_norm)
