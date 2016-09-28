tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 metronet.m4 > metronet.yaml"

# include macros
include(macros.m4)

node_types:
    
    tosca.nodes.MetroNetworkSystem:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The Metro Network Service.
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            administrativeState:
                type: string
                required: true
            restUrl:
                type: string
                required: false


    tosca.nodes.MetroNetworkDevice:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The Metro Network Device.
        properties:
            xos_base_props
            restCtrlUrl:
                type: string
                required: true
            username:
                type: string
                required: true
            password:
                type: string
                required: true
            administrativeState:
                type: string
                required: true
            authType:
                type: string
                required: false
            id:
                type: string
                required: true
