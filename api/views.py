from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Profile, Post
from api.serializers import PostSerializer


@csrf_exempt
def postList(request):
    """
    List all code posts, or create a new post.
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def some_post(request, author_id):

    if  request.method == "GET":
        posts = Post.objects.filter(author_id= author_id)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

