#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__NAME__ = 'Griffin Lim Algorithm'

import scipy
import shutil
import numpy as np
import librosa
from librosa import display
from optparse import OptionParser
from matplotlib import pyplot as plt


def griffin_lim(stftm_matrix, shape, min_iter=20, max_iter=50, delta=20):
    y = np.random.random(shape)
    y_iter = []

    for i in range(max_iter):
        if i >= min_iter and (i - min_iter) % delta == 0:
            y_iter.append((y, i))

        stft_matrix = librosa.core.stft(y)  # stft_matrix:(1025,122), stftm_matrix:(1025,122)
        stft_matrix = stftm_matrix * (stft_matrix / np.abs(stft_matrix))  # np.array乘除为对应元素乘除
        y = librosa.core.istft(stft_matrix)  # (62208,)

    y_iter.append((y, max_iter))  # 当达到max_iter时添加
    return y_iter


if __name__ == '__main__':
    # 程序中argv[0]已替换为wave_name
    wave_name = "sample.wav"
    """
    cmd_parser = OptionParser(usage="usage: %prog <wav-file>")

    cmd_parser.parse_args()
    (opts, argv) = cmd_parser.parse_args()

    if len(argv) != 1:
        cmd_parser.print_help()
        exit(-1)
    """

    # 每次运行代码时设置相同的seed,则每次生成的随机数也相同,相当于说"0"是给随机数起的名字
    np.random.seed(0)
    # assume 1 channel wav file
    sr, data = scipy.io.wavfile.read(wave_name)  # sr:16000, data:(62208,),非(-1,1),整数

    stftm_matrix = np.abs(librosa.core.stft(data))  # <class 'tuple'>:(1025, 122)
    stftm_matrix_modified = stftm_matrix + np.random.random(stftm_matrix.shape)  # 生成0和1之间的随机浮点数float

    y_iters = griffin_lim(stftm_matrix_modified, data.shape)
    n_figure = 1 + len(y_iters)

    plt.figure(figsize=(8, 14))
    plt.subplot(n_figure, 1, 1)
    display.waveplot(data, sr=sr)
    plt.title('origin wave')

    for i in range(0, len(y_iters)):
        y, n_iters = y_iters[i]
        store_file = wave_name.replace('.wav', '_griffinlim_iters{iters}.wav'.format(iters=n_iters))
        print('NumIters {}, Audio: {}'.format(n_iters, store_file))
        plt.subplot(n_figure, 1, i + 2)
        display.waveplot(y.astype(np.int16), sr=sr)
        plt.title('reconstructed wave from STFT-M (Iter {})'.format(n_iters))

        shutil.rmtree(store_file, ignore_errors=True)  # 如果存在此音频文件则删除
        scipy.io.wavfile.write(store_file, sr, y.astype(np.int16))

    store_file = wave_name.replace('.wav', '_griffinlim.png')
    print("Waveform image: {}".format(store_file))
    plt.savefig(store_file, dpi=100)

    print('DONE')
