from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import views, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from places.serializers import SpotSerializer


class SpotApiView(views.APIView):
    serializer_class = SpotSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        yield {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError | Exception:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status=status.HTTP_400_BAD_REQUEST)

