
from rest_framework.response import Response
from rest_framework.views import APIView
import logging



logger = logging.getLogger(__name__)


def NegotiateViewBuilder(registry):

    class NegotiateView(APIView):
        """Negotiate view will receive post requests on each negotiate (its like a hook)
        """
        permission_classes = ()
        authentication_classes = ()

        def post(self, request):
            logger.info(f"Arkitekt Provider-Registration: {request.data}")
            json_answer = registry.on_negotiate(request)
            return Response(json_answer)
                  
    return NegotiateView



