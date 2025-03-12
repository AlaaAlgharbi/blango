from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from django.contrib.auth.models import User
from blog.api.serializers import PostSerializer, UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post, Tag
from rest_framework.decorators import action
from rest_framework.response import Response

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    @action(methods=["get"], detail=True, name="Posts with the Tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)
class UserDetail(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication]
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer
    