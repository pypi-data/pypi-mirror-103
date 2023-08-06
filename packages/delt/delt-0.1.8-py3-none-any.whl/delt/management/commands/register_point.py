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

DATA_MODELS = None

def parse_data_models():
    global DATA_MODELS
    if not DATA_MODELS:
        allmodels = apps.get_models()
        DATA_MODELS = []


        for model in allmodels:
            meta = model._meta
            try: 
                identifier = meta.identifier
            except:
                continue

            if identifier:
                module = model._meta.app_label
                extenders = meta.extenders if hasattr(meta, "extenders") else []
                DATA_MODELS.append(DataModel(module=module, identifier=identifier, extenders=extenders))

            
    return DATA_MODELS


def main():

    settings = get_active_settings()
    # Perform connection
    client = PointBergen(
        point_inward=settings.inward,
        point_outward=settings.outward,
        point_port=settings.port,
        needs_negotiation=settings.needs_negotiation,
        force_new_token=True,
        auto_reconnect=True# if we want to specifically only use pods on this innstance we would use that it in the selector
    )


    for model in parse_data_models():
        client.register(model)

    client.start()

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