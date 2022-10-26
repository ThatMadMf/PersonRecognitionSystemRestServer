import base64
from io import BytesIO

import face_recognition
from PIL import Image
from PIL import ImageFont
from PIL.ImageDraw import ImageDraw
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class PerformRecognition(APIView):
    http_method_names = ['get']

    def get(self, request):
        image_test = face_recognition.load_image_file('./resources/obama-2.jpg')
        test_encoding = face_recognition.face_encodings(image_test)[0]

        face_locations = face_recognition.face_locations(image_test)

        if len(face_locations) == 0:
            return Response({"message": "no face detected"}, status.HTTP_400_BAD_REQUEST)

        train_image = face_recognition.load_image_file('./resources/obama-1.jpg')
        train_encoding = face_recognition.face_encodings(train_image)[0]

        results = face_recognition.compare_faces([train_encoding], test_encoding)

        if results[0]:
            top, right, bottom, left = face_locations[0]

            local_image_test = Image.fromarray(image_test)

            aggregated_image = ImageDraw(local_image_test)
            aggregated_image.rectangle([left, bottom, right, top], outline='red', width=5)

            font = ImageFont.truetype('UbuntuMono-R.ttf', 32)
            aggregated_image.text((left, bottom), "OBEMA >:(", font=font, fill=(255, 0, 0))

            buffer = BytesIO()
            local_image_test.save(buffer, format="JPEG")

            return Response(base64.b64encode(buffer.getvalue()), status.HTTP_200_OK)

        return Response(
            {"message": "Could not recognize"},
            status.HTTP_200_OK,
        )
