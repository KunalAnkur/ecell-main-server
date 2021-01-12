# TODO: clean imports
# from rest_framework import status
from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
# from rest_framework.viewsets import ModelViewSet
from .models import Event, EventRegister
from .serializers import *
from decorators import ecell_user,relax_ecell_user
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.six.moves.urllib.parse import urlsplit


# from rest_framework import status, generics
 
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from utils.swagger import set_example
from utils.swagger import set_example
from rest_framework import status, generics
# from . import responses
# TODO: simplify with drf
# @api_view(['GET', ])
# def get_events(request, year):
#     # print(request.META['SERVER_PROTOCOL'])
#     res_message = ""
#     res_status = ""
#     res_data = []
#     # scheme = urlsplit(request.build_absolute_uri(None)).scheme
#     # print(scheme)
#     events = Event.objects.filter(year=year, flag=True)
#     if len(events) > 0:
#         res_data = EventListSerializer(
#             events, many=True, context={
#                 'request': request}).data
#         res_message = "Events Fetched successfully."
#         res_status = status.HTTP_200_OK
#     else:
#         res_message = "Events Couldn't be fetched"
#         res_status = status.HTTP_404_NOT_FOUND

#     return Response({
#         "message": res_message,
#         "data": res_data
#     }, status=res_status)

class EventView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    @swagger_auto_schema(
        operation_id='get_events',
        request_body=EventListSerializer,
        responses={
            # '200': set_example(responses.get_events_200),
            # '404': set_example(responses.events_not_found_404),
        },
    )
    def list(self,request,year):
       queryset = Event.objects.filter(year=year, flag=True)
       serializer = EventListSerializer(events, many=True, context={'request': request})
       data = serializer.data
       if queryset.count() > 0:
            return Response({"message":"Events Fetched successfully","data":data},status.HTTP_200_OK)
       else:
            return Response({"message": "Events Couldn't be fetched"}, status.HTTP_404_NOT_FOUND)  


# TODO: simplify with drf
@api_view(['POST', ])
@ecell_user
def event_register(request, id):
    eventregister = EventRegister()
    user = request.ecelluser
    res_status = status.HTTP_401_UNAUTHORIZED
    if user.verified:
        eventregister.user = user
        try:
            eventregister.event = Event.objects.get(id=id)
        except:
            res_message="Registration Failed. Event does not exist."
            res_status=status.HTTP_404_NOT_FOUND
            
        else:
            eventregister.save()
            res_message= "Registration Successful"
            res_status=status.HTTP_200_OK
    else:
        res_message = "You need to verify your account to register for an event"
    return Response({
        "message": res_message
    }, status=res_status)



# TODO: simplify with drf
@api_view(['POST', ])
@ecell_user
def event_unregister(request, id):
    u = request.ecelluser
    if u:
        try:
            e = Event.objects.get(id=id)
        except:
            res_message="Event does not exist"
            res_status=status.HTTP_404_NOT_FOUND   
        else:
            try:
                reg = EventRegister.objects.filter(user = u, event= e)  
            except:
                res_message= "Event not registered"
                res_status=status.HTTP_404_NOT_FOUND
            else:
                res_message="Registration deleted successfully"
                reg.delete()
                res_status=status.HTTP_200_OK
    
    else:
        res_message = "Login to continue"
    return Response({
        "message": res_message
    }, status=res_status)


# TODO: in next meeting report why this exsits
class NoticeBoardListView(ListAPIView):
    queryset = NoticeBoard.objects.filter(show=True)
    serializer_class = NoticeBoardSerializer