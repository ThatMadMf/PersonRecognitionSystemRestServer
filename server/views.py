import base64
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from rest_framework import status, permissions
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


class Me(APIView):
    model = User
    serializer = UserSerializer
    http_method_names = ['get']
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(self.serializer(request.user).data, status.HTTP_200_OK)


class Users(GenericApiView):
    model = User
    serializer = UserSerializer


class UserFaceEncodings(GenericApiView):
    model = UserFaceEncoding
    serializer = UserFaceEncodingSerializer


class FaceRecognition(APIView):
    http_method_names = ['post']
    serializer = FaceRecognitionSerializer

    @staticmethod
    def get_array(binary):
        return np.frombuffer(base64.decodebytes(binary), dtype=np.float32)

    def post(self, request, image_type='form-data'):
        try:
            if image_type == 'form-data':
                input_image = face_recognition.load_image_file(request.data['image'])
                face_locations = face_recognition.face_locations(input_image)[0]
                input_encoding = face_recognition.face_encodings(input_image, face_locations)[0]
            else:
                input_bytes = BytesIO(base64.b64decode(request.data['image']))
                pil_image = Image.open(input_bytes)
                input_image = np.asarray(pil_image)
                face_locations = face_recognition.face_locations(input_image)
                input_encoding = face_recognition.face_encodings(input_image, face_locations)[0]
        except IndexError as e:
            return Response(data={'result': 'not recognized'}, status=status.HTTP_400_BAD_REQUEST)

        temp = list(map(list, zip(*UserFaceEncoding.objects.values_list('user_id', 'user__first_name', 'encoding'))))

        users = temp[0]
        names = temp[1]
        encodings = temp[2]

        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(encodings, input_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(encodings, input_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            top, right, bottom, left = face_locations[0]

            local_image_test = Image.fromarray(input_image)

            aggregated_image = ImageDraw(local_image_test)
            aggregated_image.rectangle([left, bottom, right, top], outline='red', width=5)

            font = ImageFont.truetype('UbuntuMono-R.ttf', 32)
            aggregated_image.text((left, bottom), names[best_match_index], font=font, fill=(255, 0, 0))

            buffer = BytesIO()
            local_image_test.save(buffer, format="JPEG")

            return Response(
                {
                    'result': 'recognized',
                    'userId': users[best_match_index],
                    'confidence': face_distances.max(),
                    'image': base64.b64encode(buffer.getvalue()),
                },
                status.HTTP_200_OK,
            )

        return Response({'result': 'not recognized'}, status.HTTP_200_OK)


class CaptureSessions(GenericApiView):
    model = CaptureSession
    serializer = CreateCaptureSessionSerializer
    http_method_names = ['post']


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
