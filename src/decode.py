from transformers import MarianMTModel
import sys
import librosa
from espnet2.bin.asr_inference import Speech2Text
from espnet_model_zoo.downloader import ModelDownloader
import time
import torch
import wave
import struct
import math
import os
from scipy import fromstring, int16
import numpy as np
import subprocess

import shutil
import glob

import soundfile

# speech2text = Speech2Text.from_pretrained(
#     "reazon-research/reazonspeech-espnet-v1"
# )
# d = ModelDownloader()
# speech2text = Speech2Text(
#     **d.download_and_unpack("reazon-research/reazonspeech-espnet-v1"),
#     device=sys.argv[2]  # CPU で認識を行う場合は省略
# )
# print(speech2text)

beam_size = 20
speech2text = Speech2Text.from_pretrained(
    "reazon-research/reazonspeech-espnet-v1",
    beam_size=beam_size,
    batch_size=0,
    device=sys.argv[2]
)
time_sta = time.time()


# ----------------------------------------
# wavファイルの分割
# ---------------------------------------

def cut_wav(filename, time):
    # ファイル読み出し
    wavf = filename
    wr = wave.open(wavf, 'r')

    # waveファイルが持つ性質を取得
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time)
    t = int(time)
    frames = int(ch * fr * t)
    num_cut = int(integer//t) + 1

    # 確認用
    print("total time(s) : ", total_time)
    print("total time(integer) : ", integer)
    print("time : ", t)
    print("number of cut : ", num_cut)

    # waveの実データを取得し数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = np.frombuffer(data, dtype=int16)

    print()

    for i in range(num_cut):
        print(str(i) + ".wav --> OK!")
        # 出力データを生成
        outf = '/output/' + str(i) + '.wav'
        if i != num_cut:
            start_cut = i*frames
            end_cut = i*frames + frames
            Y = X[start_cut:end_cut]
        else:
            start_cut = i*frames
            end_cut = i*frames + frames
            Y = X[start_cut:]

        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
    return num_cut


if sys.argv[4] == "cut":
    # すでに同じ名前のディレクトリが無いか確認
    file = os.path.exists("/output")
    print(file)

    if file == False:
        # 保存先ディレクトリの作成
        os.mkdir("/output")

    # ファイル名とカット時間を入力しwavファイルを分割
    f_name = sys.argv[1]
    cut_time = int(sys.argv[3])
    n = int(cut_wav(f_name, cut_time))

    for i in range(n):
        speech, rate = librosa.load(
            "/output/" + str(i) + ".wav", sr=16000)
        result = speech2text(speech)
        print(str(i*cut_time)+"~"+str((i+1)*cut_time), "s: ", result[0][0])
elif sys.argv[4] == "full":
    speech, rate = librosa.load(
        sys.argv[1], sr=16000)
    result = speech2text(speech)
    print(result[0][0])
time_end = time.time()
tim = time_end - time_sta
print("処理時間：", tim)
