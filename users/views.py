from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from users.serializers import PromoteUserSerializer
from users.models import User

class UpdateStatusUserViewSet(ModelViewSet):
    """
    API endpoints for Assigning Any Clients to Admin in the E-comerce site
    - Support proper pagination system
    - Allow Admin can change this
    - Please access through individual id to change status
    """
    queryset = User.objects.all()
    serializer_class = PromoteUserSerializer 
    permission_classes = [IsAdminUser]  

    # @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    # def promote_to_admin(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PromoteUserSerializer(user, data=request.data, partial=True, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"message": f"{user.first_name} admin status updated"})
    
    