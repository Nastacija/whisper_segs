import whisper, os
import pandas as pd
from write_seg import write_seg


model = whisper.load_model("medium")

def annotate(wav_name, s_freq, bps, n_ch, lvl):

    result = model.transcribe(wav_name)
    df = pd.DataFrame(result["segments"])

    labels = []

    for start_time, content in zip(df['start'], df['text']):
        start_pos = start_time* s_freq
        txt = content.replace(',', '').replace('.', '').lower()
        data = {'position': start_pos,
                'level': lvl,
                'name': txt}
        labels.append(data)
        if start_time == df['start'][len(df['start'])-1]:
            fin_pos = df['end'][len(df['end'])-1] * s_freq
            data = {'position': fin_pos,
                'level': lvl,
                'name': ''}
            labels.append(data)

    print(labels)

    seg_name = wav_name.rstrip('wav') + 'seg'
    write_seg(s_freq, bps, n_ch, labels, seg_name)

def annotate_all(dirname):

    speakers = os.listdir(dirname)
    print(speakers)

    for spkr in speakers:
        files = os.listdir(f'{dirname}/{spkr}')
        print(spkr, files)
        s_freq = int(input('sampling frequency = '))
        bps = int(input('bytes rer sample = '))
        n_ch = int(input('channels = '))
        lvl = str(input('level = '))
        aud = []
        for fl in files:
            if fl.endswith('.wav') == True:
                aud.append(f'{dirname}/{spkr}/{fl}')
        for fl in aud:
            annotate(fl, s_freq, bps, n_ch, lvl)

annotate_all('speakers')




