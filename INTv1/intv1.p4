#include <core.p4>
#include <v1model.p4>

#include "include/headers.p4"
#include "include/parsers.p4"

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
    Hence, don't decrement TTL or modify MAC addresses.
    */
    action forward(bit<9> egressPort) {
        standard_metadata.egress_spec = egressPort;
    }

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

    apply {
        ipv4forwarding.apply();
    }
}

/*
The Source Switch is required to take a packet and add the INT-MD header
and it's own Metadata.

The packets that reach here definitely have an IPv4 Header.

Possible errors:
1. INT-MD header might already exist.
2. There might not be any space to add metadata.
*/
control SourceSwitchProcessing(inout headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    apply {
        log_msg("Source");

        // Source shouldn't receive a packet which already has int_md set.
        // TODO look for a way to raise an error.
        if (hdr.int_md.isValid()) {
            log_msg("[ERROR] Source encountered INT_MD header");
            return;
        }

        /*
        Set the IPv4 Options to indicate that there are INT Headers present in the packet.
        This allows transit nodes to expect INT Headers and parse them appropriately.

        TODO: Read into applications of IPV4Option to see if I need to set length of options etc.
        because I don't need that from my implementation pov.
        Hence, I would only need to cache the option type.

        TODO: Allow packets with already existing IPv4Options header to flow into source?
        See if this would be a necessity, or whether I can get by with packets not having any.
        */

        hdr.ipv4_option.setValid();
        hdr.ipv4_option.option = INT_OPTION_TYPE;

        // Increase IHL length, to indicate that there are options.
        hdr.ipv4.ihl = hdr.ipv4.ihl + 1;

        // Set the INT_MD Header valid, and set the count.
        hdr.int_md.setValid();
        hdr.int_md.countHeaders = 1;

        // Set the first INT_DATA header valid, and set the data values.
        hdr.int_data[0].setValid();
        hdr.int_data[0].queueDepth = (queue_depth_t) standard_metadata.deq_qdepth;
    }
}

/*
Transit Switches are only required to add the data (to an already existing array
of data) and increase the count.

Possible errors:
1. INT_MD might not exist.
2. METADATA limit may have been reached (fail silently).
*/
control TransitSwitchProcessing(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {
        log_msg("Transit");

        if (!hdr.int_md.isValid()) {
            log_msg("[ERROR] Transit node couldn't find INT_MD Header");
            return;
        }

        header_count_t numHeaders = hdr.int_md.countHeaders; 

        if (numHeaders == MAX_INT_DATA) {
            log_msg("[NOTE] Maximum INT_DATA limit reached");
            return;
        }

        // Should I increment IHL here?

        // Can safely index into array.
        hdr.int_data[numHeaders].setValid();
        hdr.int_data[numHeaders].queueDepth = (queue_depth_t) standard_metadata.deq_qdepth;

        hdr.int_md.countHeaders = numHeaders + 1;
    }
}

/*
For now, I will skip the clone parts. Sink is required to just
restore IPv4 Options and invalidate the INT_MD.

*/
control SinkSwitchProcessing(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {
        log_msg("Sink");

        if (!hdr.int_md.isValid()) {
            log_msg("[ERROR] Sink node couldn't find INT_MD Header");
            return;
        }

        log_msg("Num headers: {}", {hdr.int_md.countHeaders});

        // TODO this should actually be a restoration by consulting int_md.
        hdr.ipv4.ihl = 5;
        hdr.ipv4_option.setInvalid();
        hdr.int_md.setInvalid();

        // How to do this? Needs a loop. Could set a flag and handle in the deparser maybe.
        hdr.int_data[0].setInvalid();
        hdr.int_data[1].setInvalid();
    }
}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    bit switchInfoTableKey = 0;
                     
    action populateSwitchInfo(bit<4> switchId, bit<2> role) {
        meta.switch_metadata.switchId = (bit<8>) switchId;
        meta.switch_metadata.switchINTRole = (bit<8>) role;
    }

    table SwitchInfo {
        key = {
            switchInfoTableKey : exact;
        }
        actions = {
            populateSwitchInfo;
        }
        size = 1;
    }

    SourceSwitchProcessing()  sourceProcessingInstance;
    TransitSwitchProcessing() transitProcessingInstance;
    SinkSwitchProcessing()    sinkProcessingInstance;

    apply {
        // Get the INT role for this switch.
        // For Switches not involved in INT, the search will miss.
        if(SwitchInfo.apply().hit && hdr.ipv4.isValid()) {
            log_msg("Switch ID: {}, SwitchRole: {}", {meta.switch_metadata.switchId, meta.switch_metadata.switchINTRole});
            // TODO replace with enum for readability.
            if (meta.switch_metadata.switchINTRole == 0) {
                sourceProcessingInstance.apply(hdr, meta, standard_metadata);
            }
            else if (meta.switch_metadata.switchINTRole == 1) {
                transitProcessingInstance.apply(hdr, meta, standard_metadata);
            }
            else if (meta.switch_metadata.switchINTRole == 2) {
                sinkProcessingInstance.apply(hdr, meta, standard_metadata);
            } else {
                // Switch not involved in INT.
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