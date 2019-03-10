import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from apis.serializers import ArtSerializer
from apps.book.models import Art


class BookListAPIView(APIView):
    '''书籍列表页'''
    @csrf_exempt
    def get(self, request):
        # 1.获取所有书籍
        books = Art.objects.all()[0:9]
        # 2.通过序列化器的转换（模型转换为JSON）
        serializer = ArtSerializer(books, many=True)
        # permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
        # 3.返回响应
        # return HttpResponse(serializer.data)
        # return HttpResponse(json.dumps(serializer.data), content_type="application/json")
        return JsonResponse(serializer.data)
        # def post(self, request):
        #     # 1.接收参数
        #     data = request.data
        #     # 2.验证参数（序列化器的校验）
        #     serializer = ArtSerializer(data=data)
        #     serializer.is_valid(raise_exception=True)
        #     # 3.数据入库
        #     serializer.save()
        #     # 4.返回响应
        #     return Response(serializer.data)




