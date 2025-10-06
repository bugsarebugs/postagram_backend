from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets 
from core.user.serializers import UserSerializer 
from core.user.models import User 
from core.abstract.viewsets import AbstractViewSet
from rest_framework.exceptions import PermissionDenied

class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer 

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)
    
    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])

        # ! Only allow users to access their own profile (unless they are admin)
        if self.request.method in ['PATCH', 'PUT']:
            if not self.request.user.is_superuser and obj != self.request.user:
                raise PermissionDenied("You are not allowed to edit another user's profile.")
        self.check_object_permissions(self.request, obj)
        return obj 
    