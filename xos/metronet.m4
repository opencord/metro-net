
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 metronet.m4 > metronet.yaml"

# include macros
include(macros.m4)

node_types:

   tosca.nodes.VNodGlobalService:
        description: >
            CORD: The MetroNet Service.
        derived_from: tosca.nodes.Root
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props

   tosca.nodes.MetroNetworkSystem:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The Metro Network Service.
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props
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

   tosca.nodes.EcordBandwidthProfile:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord bandwith profile.
        capabilities:
        properties:
            xos_base_props
            bwpcfgcbs:
                type: integer
                required: false
            bwpcfgebs:
                type: integer
                required: false
            bwpcfgcir:
                type: integer
                required: false
            bwpcfgeir:
                type: integer
                required: false
            name:
                type: string
                required: true

   tosca.nodes.EcordUserNetworkInterface:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The ecord user netowrk interface
        capabilities:
        properties:
            xos_base_props
            enabled:
                type: boolean
                required: false
            capacity:
                type: integer
                required: false
            bw_used:
                type: integer
                required: false
            vlanIds:
                type: string
                required: false
            name:
                type: string
                required: true
            location:
                type: string
                required: false
            latlng:
                type: string
                required: false

   tosca.relationships.UsesBandwidthProfile:
        derived_from: tosca.relationships.Root
        valid_target_types: [ tosca.capabilities.xos.EcordBandwidthProfile ]