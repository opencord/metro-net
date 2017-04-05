import os, sys
from itertools import chain

from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible #if needed
from synchronizers.new_base.ansible_helper import run_template_ssh #if needed
from synchronizers.new_base.modelaccessor import *
from xos.logger import Logger, logging
from synchronizers.metronetwork.providers.providerfactory import ProviderFactory
from synchronizers.metronetwork.invokers.invokerfactory import InvokerFactory

# metronetwork will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)


class SyncMetroNetworkSystem(SyncStep):
    provides = [MetroNetworkSystem]
    observes = MetroNetworkSystem
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

        # Get the NetworkSystem object - if it exists it will test us
        # whether we should do a full sync or not - it all has our config
        # information about the REST interface

        metronetworksystem = self.get_metronetwork_system()
        if not metronetworksystem:
            logger.debug("No Service configured")
            return objs

        # Check to make sure the Metro Network System is enabled
        metronetworksystem = self.get_metronetwork_system()
        if metronetworksystem.administrativeState == 'disabled':
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
                p2pactivatereqs = NetworkEdgeToEdgePointConnection.objects.filter(adminstate='activationrequested')
                mp2mpactivatereqs = NetworkMultipointToMultipointConnection.objects.filter(adminstate='activationrequested')
                r2mpactivatereqs = NetworkEdgeToMultipointConnection.objects.filter(adminstate='activationrequested')
                activatereqs = list(chain(p2pactivatereqs, mp2mpactivatereqs, r2mpactivatereqs))
                for activatereq in activatereqs:

                    # Call the XOS Interface to create the service
                    logger.debug("Attempting to create EdgePointToEdgePointConnectivity: %s" % activatereq.id)
                    if (provider.create_network_connectivity(activatereq)):
                        # Everyting is OK, lets let the system handle the persist
                        objs.append(activatereq)
                    else:
                        # In the case of an error we persist the state of the object directly to preserve
                        # the error code - and because that is how the base synchronizer is designed
                        activatereq.save()

                # Check for ConnectivityObjects that are in deacticationequested state - deletes to the backend
                p2pdeactivatereqs = NetworkEdgeToEdgePointConnection.objects.filter(adminstate='deactivationrequested')
                mp2mpdeactivatereqs = NetworkMultipointToMultipointConnection.objects.filter(adminstate='deactivationrequested')
                r2mpdeactivatereqs = NetworkEdgeToMultipointConnection.objects.filter(adminstate='deactivationrequested')
                deactivatereqs = list(chain(p2pdeactivatereqs, mp2mpdeactivatereqs, r2mpdeactivatereqs))
                for deactivatereq in deactivatereqs:

                    # Call the XOS Interface to delete the service
                    logger.debug("Attempting to delete EdgePointToEdgePointConnectivity: %s" % deactivatereq.id)
                    if provider.delete_network_connectivity(deactivatereq):
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

                # Handle the case where we have deleted Eline Services from our side - if the Service is in
                # enabled state then we call the provider, otherwise just queue it for deletion
                elinedeletedobjs = NetworkEdgeToEdgePointConnection.deleted_objects.all()
                for elinedeletedobj in elinedeletedobjs:
                    if elinedeletedobj.adminstate == 'enabled':
                        provider.delete_network_connectivity(elinedeletedobj)
                    # Either way queue it for deletion
                    objs.append(elinedeletedobj)

                # Handle the case where we have deleted Etree Services from our side - if the Service is in
                # enabled state then we call the provider, otherwise just queue it for deletion
                etreedeletedobjs = NetworkEdgeToMultipointConnection.deleted_objects.all()
                for etreedeletedobj in etreedeletedobjs:
                    # TODO: Handle the case where its connected, we need to disconnect first
                    if etreedeletedobj.adminstate == 'enabled':
                        provider.delete_network_connectivity(etreedeletedobj)
                    # Either way queue it for deletion
                    objs.append(etreedeletedobj)

                # Handle the case where we have deleted Elan Services from our side - if the Service is in
                # enabled state then we call the provider, otherwise just queue it for deletion
                elandeletedobjs = NetworkMultipointToMultipointConnection.deleted_objects.all()
                for elandeletedobj in elandeletedobjs:
                    # TODO: Handle the case where its connected, we need to disconnect first
                    if elandeletedobj.adminstate == 'enabled':
                        provider.delete_network_connectivity(elandeletedobj)
                    # Either way queue it for deletion
                    objs.append(elandeletedobj)

                # Handle the case where we have deleted VnodGlobal Services from our side - if there is
                # an attached Eline/Etree/Elan we set that to deleted
                vnodbloaldeletedobjs = VnodGlobalService.deleted_objects.all()
                for vnodbloaldeletedobj in vnodbloaldeletedobjs:
                    # Check for dependent eline service
                    if vnodbloaldeletedobj.metronetworkpointtopoint is not None:
                        elineobj = vnodbloaldeletedobj.metronetworkpointtopoint
                        elineobj.deleted = True
                        objs.append(elineobj)
                    # Check for dependent elan service
                    if vnodbloaldeletedobj.metronetworkmultipoint is not None:
                        elanobj = vnodbloaldeletedobj.metronetworkmultipoint
                        elanobj.deleted = True
                        objs.append(elanobj)
                    # Check for dependent etree service
                    if vnodbloaldeletedobj.metronetworkroottomultipoint is not None:
                        etreeobj = vnodbloaldeletedobj.metronetworkroottomultipoint
                        etreeobj.deleted = True
                        objs.append(etreeobj)

                    objs.append(vnodbloaldeletedobj)

        # In add cases return the objects we are interested in
        return objs

    def sync_record(self, o):

        # First we call and see if there is an invoker for this object - the idea of the invoker
        # is to wrap the save with a pre/post paradigm to handle special cases
        # It will only exist for a subset of ojbects
        invoker = InvokerFactory.getinvoker(o)

        # Call Pre-save on the inovker (if it exists)
        if invoker is not None:
            invoker.presave(o)

        # Simply save the record to the DB - both updates and adds are handled the same way
        o.save()

        # Call Post-save on the inovker (if it exists)
        if invoker is not None:
            invoker.postsave(o)

    def delete_record(self, o):
        # Overriden to customize our behaviour - the core sync step for will remove the record directly
        # We just log and return
        logger.debug("deleting Object %s" % str(o), extra=o.tologdict())

    def get_metronetwork_system(self):
        # We only expect to have one of these objects in the system in the curent design
        # So get the first element from the query
        metronetworksystem = MetroNetworkSystem.objects.all()
        if not metronetworksystem:
            return None

        return metronetworksystem[0]
