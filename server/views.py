import base64
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from server.serializers import *


class GenericApiView(APIView):
    model = None
    serializer = None
    http_method_names = ['get', 'post']

    def get(self, request):
        return Response(self.serializer(self.model.objects.all(), many=True).data, status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class Users(GenericApiView):
    model = User
    serializer = UserSerializer


class UserFaceEncodings(GenericApiView):
    model = UserFaceEncoding
    serializer = UserFaceEncodingSerializer


class FaceRecognitionSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        fields = ['image']


class FaceRecognition(APIView):
    http_method_names = ['post']
    serializer = FaceRecognitionSerializer

    def get_array(self, binary):
        return np.frombuffer(base64.decodebytes(binary), dtype=np.float32)

    def post(self, request):
        temp = list(map(list, zip(*UserFaceEncoding.objects.values_list('user_id', 'encoding'))))

        users = temp[0]
        encodings = temp[1]

        input_image = face_recognition.load_image_file(request.data['image'])
        input_encoding = face_recognition.face_encodings(input_image)[0]

        face_distances = face_recognition.face_distance(encodings, input_encoding)

        return Response(
            {"userId": users[np.argmin(face_distances)], "confidence": face_distances.max()},
            status.HTTP_200_OK,
        )


class RecognitionSessions(APIView):
    http_method_names = ['post']

    def post(self, request):
        pass


class FrameRecognition(APIView):
    http_method_names = ['get']

    def get(self, request):
        image_test = face_recognition.load_image_file('./resources/obama-2.jpg')
        test_encoding = face_recognition.face_encodings(image_test)[0]

        face_locations = face_recognition.face_locations(image_test)

        if len(face_locations) == 0:
            return Response({"message": "no face detected"}, status.HTTP_400_BAD_REQUEST)

        train_image = face_recognition.load_image_file('./resources/obama-1.jpg')
        train_encoding = face_recognition.face_encodings(train_image)[0]

        results = face_recognition.face_distance([train_encoding], test_encoding)

        if results[0]:
            top, right, bottom, left = face_locations[0]

            local_image_test = Image.fromarray(image_test)

            aggregated_image = ImageDraw(local_image_test)
            aggregated_image.rectangle([left, bottom, right, top], outline='red', width=5)

            font = ImageFont.truetype('UbuntuMono-R.ttf', 32)
            aggregated_image.text((left, bottom), "OBEMA >:(", font=font, fill=(255, 0, 0))

            buffer = BytesIO()
            local_image_test.save(buffer, format="JPEG")

            print((1 - results[0]) * 100)

            return Response(base64.b64encode(buffer.getvalue()), status.HTTP_200_OK)

        return Response(
            {"message": "Could not recognize"},
            status.HTTP_200_OK,
        )
