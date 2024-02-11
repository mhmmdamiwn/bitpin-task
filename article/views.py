from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated
from json import JSONDecodeError
from django.http import JsonResponse

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        # Pass the request context to the serializer
        return {'request': self.request}
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
        

class CreateOrUpdateRatingView(generics.GenericAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data['post'].id
            user = request.user
            score = serializer.validated_data['score']

            rating, created = Rating.objects.update_or_create(
                post_id=post_id, user=user,
                defaults={'score': score}
            )
            return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)