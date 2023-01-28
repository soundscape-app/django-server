from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from basic.models import Audio
from basic.utils.dwt import WaveletTransformFilter as wltf

class WaveletTransformView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        audio = request.FILES.get('audio', None)
        wavelet = request.data.get('wavelet', 'haar')
        mode = request.data.get('mode', 'soft')
        
        if not audio:
            return Response(
                {'message': 'Audio file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        original_audio = Audio.objects.create(
            wav_file=audio
        )
        original_audio.save()

        wltf.apply_filter_to_file(file_path=original_audio.wav_file.path, wavelet=wavelet, mode=mode)

        file_name = '/media/' + str(original_audio.wav_file).split('.')[0] + '_transformed.wav'

        return Response(
            {'output_audio' : file_name},
            status=status.HTTP_200_OK
        )
