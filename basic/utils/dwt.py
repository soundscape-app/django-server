import pywt
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import soundfile as sf
from pydub import AudioSegment

class WaveletTransformFilter:
    @staticmethod
    def load_wav_file(file_path):
        audio, sample_rate = librosa.load(file_path, sr=None, mono=True)
        return audio, sample_rate

    @staticmethod
    def dwt_noise_filter(audio: np.ndarray, wavelet='haar', mode='soft'):
        c_approx, c_detail = pywt.dwt(audio, wavelet)

        c_approx_transformed = pywt.threshold(c_approx, np.std(c_approx), mode=mode)
        c_detail_transformed = pywt.threshold(c_detail, np.std(c_detail), mode=mode)

        audio_transformed = pywt.idwt(c_approx_transformed, c_detail_transformed, wavelet)
        return audio_transformed

    @staticmethod
    def export_wav_file(audio: np.ndarray, sample_rate: int, file_path):
        sf.write(file_path, audio, sample_rate, format='wav')

    @staticmethod
    def convert_mp3_to_wav(file_path):
        if file_path.split('.')[1] != 'mp3':
            raise Exception('File is not mp3 format. Conversion failed.')
        audio_segment = AudioSegment.from_mp3(file_path)
        audio_segment.export(file_path.split('.')[0] + '.wav', format='wav')

    @staticmethod
    def apply_filter_to_file(file_path, prefix_dir='', wavelet='haar', mode='soft'):
        audio, sample_rate = WaveletTransformFilter.load_wav_file(file_path)
        audio_transformed = WaveletTransformFilter.dwt_noise_filter(audio, wavelet, mode)

        output_file_path = prefix_dir + file_path.split('.')[0] + '_transformed.wav'
        WaveletTransformFilter.export_wav_file(audio_transformed, sample_rate, output_file_path)

    @staticmethod
    def plot_melspectogram(ax, audio, sample_rate):
        librosa.display.specshow(
            librosa.power_to_db(
                librosa.feature.melspectrogram(audio, sr=sample_rate), 
                ref=np.max
            ), 
            y_axis='mel', 
            fmax=8000, 
            x_axis='time',
            ax=ax
        )

    @staticmethod
    def plot_mfcc(ax, audio, sample_rate):
        librosa.display.specshow(
            librosa.feature.mfcc(audio, sr=sample_rate), 
            x_axis='time',
            ax=ax
        )

    @staticmethod
    def plot_difference(before_audio: str, after_audio: str, prefix_dir='', show=False):
        filename = before_audio.split('.')[0]

        before_audio, before_sample_rate = WaveletTransformFilter.load_wav_file(before_audio)
        after_audio, after_sample_rate = WaveletTransformFilter.load_wav_file(after_audio)

        fig = plt.figure(figsize=(20, 8))
        fig.suptitle('Difference between before and after', fontsize=16)

        default_graph_1 = fig.add_subplot(3, 2, 1)
        default_graph_2 = fig.add_subplot(3, 2, 2)

        default_graph_1.set_title('Before')
        default_graph_1.plot(before_audio, label='Before')
        default_graph_2.set_title('After')
        default_graph_2.plot(after_audio, label='After')

        mfcc_graph_1 = fig.add_subplot(3, 2, 3)
        mfcc_graph_2 = fig.add_subplot(3, 2, 4)

        mfcc_graph_1.set_title('Before MFCC')
        WaveletTransformFilter.plot_mfcc(mfcc_graph_1, before_audio, before_sample_rate)
        mfcc_graph_2.set_title('After MFCC')
        WaveletTransformFilter.plot_mfcc(mfcc_graph_2, after_audio, after_sample_rate)

        melspectogram_graph_1 = fig.add_subplot(3, 2, 5)
        melspectogram_graph_2 = fig.add_subplot(3, 2, 6)

        melspectogram_graph_1.set_title('Before Melspectogram')
        WaveletTransformFilter.plot_melspectogram(melspectogram_graph_1, before_audio, before_sample_rate)
        melspectogram_graph_2.set_title('After Melspectogram')
        WaveletTransformFilter.plot_melspectogram(melspectogram_graph_2, after_audio, after_sample_rate)

        plt.tight_layout()
        fig.savefig(prefix_dir + filename + '_diff.png', dpi=fig.dpi)

        if show:
            plt.show()
