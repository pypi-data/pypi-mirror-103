from delt.registry.nodes import registry
from delt.discover import AutodiscoverApps
from delt.settings import get_active_settings
from django.core.management import BaseCommand
from bergen.messages.postman.provide import *
from bergen.clients.point import PointBergen
import logging 
from bergen.messages import *
from bergen.provider.base import BaseProvider
from django.conf import settings
from django.apps import apps
from bergen.schema import DataModel

logger = logging.getLogger(__name__)
autodiscover = AutodiscoverApps("nodes.py")

def main():

    settings = get_active_settings()
    # Perform connection
    client = PointBergen(
        point_inward=settings.inward,
        point_outward=settings.outward,
        point_port=settings.port,
        needs_negotiation=settings.needs_negotiation,
        force_new_token=True,
        auto_reconnect=True)

    autodiscover()

    client.negotiate()

    registry.register()


class Command(BaseCommand):
    help = "Registeres with Arkitekt"
    leave_locale_alone = True

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)


    def handle(self, *args, **options):

        # Get the backend to use
        main()
        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.