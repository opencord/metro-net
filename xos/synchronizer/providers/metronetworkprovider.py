from xos.logger import Logger, logging
from core.models.netw import *

logger = Logger(level=logging.INFO)


class MetroNetworkProvider(object):
    networkdevice = None

    def __init__(self, networkdevice, **args):
        self.networkdevice = networkdevice
        pass

    # Methods to support for Synchronization - effectively list all interfaces
    #
    # Method for retrieving all network ports from the backend system
    # Intended for use when doing a re-sync
    def get_network_ports(self):
        # Default method needs to be overriden
        logger.debug("get_network_ports default called - should be overriden")

    # Method for getting a list of network ports to delete
    # The default imnplementation just gets a list from the local DB
    # Intended for use when doing a re-sync
    def get_network_ports_for_deletion(self):
        # Default method needs to be overriden
        logger.debug("get_network_ports for deletion called - default is all ports in the db related to this id")
        objs = []
        # ports = NetworkPort.objects.filter(networkdevice=self.networkdevice.id)
        ports = NetworkPort.objects.all()
        for port in ports:
            objs.append(port)

        return objs

    # Method for retrieving all network links from the backend system
    # Includes Connectivity Objects
    # Intended for use when doing a re-sync
    def get_network_links(self):
        # Default method needs to be overriden
        logger.debug("get_network_links default called - should be overriden")
        objs = []
        return objs

    # Method for getting a list of network links to delete
    # Includes Connectivity Objects
    # Intended for use when doing a re-sync
    def get_network_links_for_deletion(self):
        # Default method needs to be overriden
        logger.debug("get_network_links for deletion called - should be overidden")
        objs = []
        return objs

    # Methods to support Event Management - movement of changes from the Domain to XOS
    #
    # Method for Create and Update - Create and Update are together given the base design
    def get_updated_or_created_objects(self):
        # Default method needs to be overriden
        logger.debug("get_updated_or_created_objects default called - should be overriden")
        objs = []
        return objs

    # Method for Delete - Create and Update are together given the base design
    def get_deleted_objects(self):
        # Default method needs to be overriden
        logger.debug("get_deleted_objects default called - should be overriden")
        objs = []
        return objs

    # Methods to support Movement of changes from XOS into the Domain
    #
    # Method for creating point to point connectivity object
    #
    # obj     - Connection object - with all configuration variables set
    # returns - Boolean - indicating whether or not the request succeeded - in either case the Admin/Oper
    #                     states are assigned - if False the backend_status field
    #                     should be assigned with the appropriate error code - in the case of True the
    #                     backend_status will be assigned by the system and should be unassigned

    def create_point_to_point_connectivity(self, obj):
        # Default method needs to be overriden
        logger.debug("create_point_to_point_connectivity called - should be overriden")
        return False

    # Method for deleting point to point connectivity object
    #
    # obj     - Connection object
    # returns - Boolean - indicating whether or not the request succeeded - in either case the Admin/Oper
    #                     states are assigned - if False the backend_status field
    #                     should be assigned with the appropriate error code - in the case of True the
    #                     backend_status will be assigned by the system and should be unassigned
    def delete_point_to_point_connectivity(self, obj):
        # Default method needs to be overriden
        logger.debug("delete_point_to_point_connectivity called - should be overriden")
        return False
