import os
import sys

from synchronizers.base.syncstep import SyncStep
from services.metronetwork.models import *
from xos.logger import Logger, logging
from synchronizers.metronetwork.providers.providerfactory import ProviderFactory

# metronetwork will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)


class SyncMetroNetworkService(SyncStep):
    provides = [MetroNetworkService]
    observes = MetroNetworkService
    requested_interval = 0
    initialized = False

    def __init__(self, **args):
        SyncStep.__init__(self, **args)

    def fetch_pending(self, deletion=False):

        # The general idea:
        # We do one of two things in here:
        #    1. Full Synchronization of the DBS (XOS <-> MetroONOS)
        #    2. Look for updates between the two stores
        # The first thing is potentially a much bigger
        # operation and should not happen as often
        #
        # The Sync operation must take into account the 'deletion' flag

        objs = []

        # Get the NetworkService object - if it exists it will test us
        # whether we should do a full sync or not - it all has our config
        # information about the REST interface

        metronetworkservice = self.get_metronetwork_service()
        if not metronetworkservice:
            logger.debug("No Service configured")
            return objs

        # Check to make sure the Service is enabled
        metronetworkservice = self.get_metronetwork_service()
        if metronetworkservice.administrativeState == 'disabled':
            # Nothing to do
            logger.debug("MetroService configured - state is Disabled")
            return objs

        # The Main Loop - retrieve all the NetworkDevice objects - for each of these
        # Apply synchronization aspects
        networkdevices = NetworkDevice.objects.all()

        for dev in networkdevices:

            # Set up the provider
            provider = ProviderFactory.getprovider(dev)

            # First check is for the AdminState of Disabled - do nothing
            if dev.administrativeState == 'disabled':
                # Nothing to do with this device
                logger.debug("NetworkDevice %s: administrativeState set to Disabled - continuing" % dev.id)

            # Now to the main options - are we syncing - deletion portion
            elif dev.administrativeState == 'syncrequested' and deletion is True:

                logger.info("NetworkDevice %s: administrativeState set to SyncRequested" % dev.id)

                # Kill Links
                networklinks = provider.get_network_links_for_deletion()
                for link in networklinks:
                    objs.append(link)

                # Kill Ports
                allports = provider.get_network_ports_for_deletion()
                for port in allports:
                    objs.append(port)

                logger.info("NetworkDevice %s: Deletion part of Sync completed" % dev.id)
                dev.administrativeState = 'syncinprogress'
                dev.save(update_fields=['administrativeState'])

            # Now to the main options - are we syncing - creation portion
            elif dev.administrativeState == 'syncinprogress' and deletion is False:

                logger.info("NetworkDevice %s: administrativeState set to SyncRequested" % dev.id)
                # Reload objects in the reverse order of deletion

                # Add Ports
                networkports = provider.get_network_ports()
                for port in networkports:
                    objs.append(port)

                # Add Links
                networklinks = provider.get_network_links()
                for link in networklinks:
                    objs.append(link)

                logger.info("NetworkDevice %s: Creation part of Sync completed" % dev.id)
                dev.administrativeState = 'enabled'
                dev.save(update_fields=['administrativeState'])

            # If we are enabled - then check for events - in either direction and sync
            elif dev.administrativeState == 'enabled' and deletion is False:
                logger.debug("NetworkDevice: administrativeState set to Enabled - non deletion phase")

                # This should be the 'normal running state' when we are not deleting - a few things to do in here

                # Get the changed objects from the provider - deletions are handled separately
                eventobjs = provider.get_updated_or_created_objects()
                for eventobj in eventobjs:
                    # Simply put in the queue for update - this will handle both new and changed objects
                    objs.append(eventobj)

                # Handle changes XOS -> ONOS
                # Check for ConnectivityObjects that are in acticationequested state - creates to the backend
                activatereqs = NetworkEdgeToEdgePointConnection.objects.filter(adminstate='activationrequested')
                for activatereq in activatereqs:

                    # Call the XOS Interface to create the service
                    logger.debug("Attempting to create EdgePointToEdgePointConnectivity: %s" % activatereq.id)
                    if (provider.create_point_to_point_connectivity(activatereq)):
                        # Everyting is OK, lets let the system handle the persist
                        objs.append(activatereq)
                    else:
                        # In the case of an error we persist the state of the object directly to preserve
                        # the error code - and because that is how the base synchronizer is designed
                        activatereq.save()

                # Check for ConnectivityObjects that are in deacticationequested state - deletes to the backend
                deactivatereqs = NetworkEdgeToEdgePointConnection.objects.filter(adminstate='deactivationrequested')
                for deactivatereq in deactivatereqs:

                    # Call the XOS Interface to delete the service
                    logger.debug("Attempting to delete EdgePointToEdgePointConnectivity: %s" % deactivatereq.id)
                    if provider.delete_point_to_point_connectivity(deactivatereq):
                        # Everyting is OK, lets let the system handle the persist
                        objs.append(deactivatereq)
                    else:
                        # In the case of an error we persist the state of the object directly to preserve
                        # the error code - and because that is how the base synchronizer is designed
                        deactivatereq.save()

            # If we are enabled - and in our deletion pass then look for objects waiting for deletion
            elif dev.administrativeState == 'enabled' and deletion is True:
                logger.debug("NetworkDevice: administrativeState set to Enabled - deletion phase")

                # Any object that is simply deleted in the model gets removed automatically - the synchronizer
                # doesn't get involved - we just need to check for deleted objects in the domain and reflect that
                # in the model
                #
                # Get the deleted objects from the provider
                eventobjs = provider.get_deleted_objects()
                for eventobj in eventobjs:
                    # Simply put in the queue for update - this will handle both new and changed objects
                    objs.append(eventobj)

        # In add cases return the objects we are interested in
        return objs

    def sync_record(self, o):
        # Simply save the record to the DB - both updates and adds are handled the same way
        o.save()

    def delete_record(self, o):
        # Overriden to customize our behaviour - the core sync step for will remove the record directly
        # We just log and return
        logger.debug("deleting Object %s" % str(o), extra=o.tologdict())

    def get_metronetwork_service(self):
        # We only expect to have one of these objects in the system in the curent design
        # So get the first element from the query
        metronetworkservices = MetroNetworkService.get_service_objects().all()
        if not metronetworkservices:
            return None

        return metronetworkservices[0]
