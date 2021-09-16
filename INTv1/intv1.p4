#include <core.p4>
#include <v1model.p4>

#include "include/headers.p4"
#include "include/parsers.p4"
#include "include/constants.p4"
#include "include/INTprocessing.p4"

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {}
}

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }

    /*
    This is a switch, and not a router.
    Hence, don't decrement TTL or modify MAC addresses. Simply forward packet.
    */
    action forward(bit<9> egressPort) {
        standard_metadata.egress_spec = egressPort;
    }

    // Stores the Egress Port for a given Destination IP.
    table ipv4forwarding {
        key = {
            hdr.ipv4.dstAddr : exact;
        }
        actions = {
            forward;
            drop;
        }
        default_action = drop;
        size = 256;
    }

    // Serves as the static key for SwitchInfo table, since it has only a single row to index into.
    bit switchInfoTableKey = 0;
    
    // Read the Switch information from Table, and populate the Metadata using it.
    action populateSwitchInfo(bit<4> switchId, bit<2> role) {
        meta.switch_metadata.switchId = (switch_id_t) switchId;
        meta.switch_metadata.switchINTRole = role;
    }

    // In the event of Table miss, populate Metadata with default values.
    action populateSwitchInfoDefault() {
        meta.switch_metadata.switchId = (switch_id_t) 0;
        meta.switch_metadata.switchINTRole = INTRole.Undefined;
    }

    table SwitchInfo {
        key = {
            switchInfoTableKey : exact;
        }
        actions = {
            populateSwitchInfo;
            populateSwitchInfoDefault;
        }
        default_action = populateSwitchInfoDefault;
        size = 1;
    }

    apply {
        // Store information about the Switch in Metadata.
        SwitchInfo.apply();

        // Forward the packet based on Destination IP Address.
        ipv4forwarding.apply();

        // On the Sink Switch, we clone INT packets towards Collector.
        if (meta.switch_metadata.switchINTRole == INTRole.Sink && hdr.int_md.isValid()) {
            meta.sink_metadata.ingress_global_timestamp = (ingress_global_time_t) standard_metadata.ingress_global_timestamp;
            clone3(CloneType.I2E, SinkSessionID, meta);
        }
    }
}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    SourceSwitchProcessing()    sourceProcessingInstance;
    TransitSwitchProcessing()   transitProcessingInstance;
    SinkSwitchProcessing()      sinkProcessingInstance;
    SinkSwitchCloneProcessing() sinkCloneProcessingInstance;

    apply {
        /**
          * INT Processing to be applied only on IPv4 Packets,
          * since we use IPv4 Options to encapsulate INT data.
          */
        if(hdr.ipv4.isValid()) {
            // Normal newly arrived packet.
            if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_NORMAL) {
                /**
                    * Information about the Switch INT Role is already stored into metadata on Ingress.
                    * We use it here to delegate responsibility to the correct processing subroutine.
                    */
                log_msg("Switch ID: {}, SwitchRole: {}", {meta.switch_metadata.switchId, meta.switch_metadata.switchINTRole});
                if (meta.switch_metadata.switchINTRole == INTRole.Source) {
                    sourceProcessingInstance.apply(hdr, meta, standard_metadata);
                }
                else if (meta.switch_metadata.switchINTRole == INTRole.Transit) {
                    transitProcessingInstance.apply(hdr, meta, standard_metadata);
                }
                else if (meta.switch_metadata.switchINTRole == INTRole.Sink) {
                    sinkProcessingInstance.apply(hdr, meta, standard_metadata);
                } else {
                    // Switch not involved in INT.
                }
            }
            // Packet was cloned during Ingress.
            else if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_CLONE) {
                if (meta.switch_metadata.switchINTRole == INTRole.Sink) {
                    sinkCloneProcessingInstance.apply(hdr, meta, standard_metadata);
                } else {
                    // This should not have happened.
                    log_msg("Received Ingress Cloned packet on role: {}", {meta.switch_metadata.switchINTRole});
                    // Doubt can I even do this on Egress?
                    mark_to_drop(standard_metadata);
                }
            }
            // Received unexpected packet.
            else {
                log_msg("Received packet with unexpected instance type: {}", {standard_metadata.instance_type});
                mark_to_drop(standard_metadata);
            }
        }
    }
}

// BIG TODO.
control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {}
}

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;