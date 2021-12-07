
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
    register<bit<8>>(1) count;

    apply {
        log_msg("Source");

        log_msg("Egress port: {}", {standard_metadata.egress_port});

        // INT on non IPv4 Packets is unsupported.
        if (!hdr.ipv4.isValid()) {
            log_msg("[NOTE] Source received non IPv4 packet.");
            return;
        }

        // Source shouldn't receive a packet which already has int_md set.
        // TODO look for a way to raise an error.
        if (hdr.int_md.isValid()) {
            log_msg("[ERROR] Source encountered INT_MD header.");
            mark_to_drop(standard_metadata);
            return;
        }

        // Check if Overhead needs to be minimized.  
        if (minimizeOverhead == 1) {
            @atomic {
                bit<8> val;
                count.read(val, (bit<32>)0);

                log_msg("Counter value: {}", {val});

                // See if we should conduct telemetry on this packet.
                if (val == (bit<8>) 0) {
                    meta.int_metadata.addINT = 1;
                } else {
                    meta.int_metadata.addINT = 0;
                }

                // Increment count.
                if (val == rateLimit) {
                    count.write((bit<32>)0, 0);
                } else {
                    count.write((bit<32>)0, val+1);
                }

                // Don't perform INT on this flow.
                if (meta.int_metadata.addINT == 0) {
                    return;
                }
            }
        }



        /*
        Set the IPv4 Options to indicate that there are INT Headers present in the packet.
        This allows transit nodes to expect INT Headers and parse them appropriately.

        TODO: Allow packets with already existing IPv4Options header to flow into source?
        See if this would be a necessity, or whether I can get by with packets not having any.
        */
        if (hdr.ipv4_option.isValid()) {
            log_msg("[ERROR] Source encountered existing IPv4 Options, dropping.");
            mark_to_drop(standard_metadata);
        } else {
            hdr.ipv4_option.setValid();

            // Don't copy Options into all fragments.
            hdr.ipv4_option.copied = 0;
            // Option is of Measurement class.
            hdr.ipv4_option.class  = 2;
            // Indicates to future nodes that this is an INT Option.
            hdr.ipv4_option.option = INT_OPTION_TYPE;
            // 2 Byte Option Field + INT_MD + INT Data.
            hdr.ipv4_option.length = 2 + INT_MD_Header_Size + INT_DATA_Size;

            // Increase IHL length. 1 word for {Option + INT_MD} and 1 for {INT_DATA}. 
            hdr.ipv4.ihl = hdr.ipv4.ihl + (bit<4>)((2 + INT_MD_Header_Size)>>2) + (bit<4>)(INT_DATA_Size >> 2);
            // Increase the IPv4 header total length by adding the newly created option.
            hdr.ipv4.totalLen = hdr.ipv4.totalLen + 2 + (bit<16>)INT_MD_Header_Size + (bit<16>)INT_DATA_Size;

            // Set the INT_MD Header valid, and set the count and sourceIngressTime.
            hdr.int_md.setValid();
            hdr.int_md.countHeaders = 1;
            hdr.int_md.sourceIngressTime = (ingress_global_time_t) standard_metadata.ingress_global_timestamp;

            // Set the first INT_DATA header valid, and set the data values.
            hdr.int_data[0].setValid();
            hdr.int_data[0].switchId     = (switch_id_t)           meta.switch_metadata.switchId;
            hdr.int_data[0].queueDepth   = (queue_depth_t)         standard_metadata.deq_qdepth;
            hdr.int_data[0].queueTime    = (queue_time_delta_t)    standard_metadata.deq_timedelta;

            log_msg("Switch: {}, Enq Depth: {}, QTime: {}, SourceITime: {}", {hdr.int_data[0].switchId, hdr.int_data[0].queueDepth, hdr.int_data[0].queueTime, hdr.int_md.sourceIngressTime});
        }
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

        // INT on non IPv4 Packets is unsupported.
        if (!hdr.ipv4.isValid()) {
            log_msg("[NOTE] Transit received non IPv4 packet.");
            return;
        }

        // If no INT_MD header, don't perform INT.
        if (!hdr.int_md.isValid()) {
            log_msg("[NOTE] Transit couldn't find INT_MD Header, returning");
            // mark_to_drop(standard_metadata);
            return;
        }

        header_count_t numHeaders = hdr.int_md.countHeaders; 

        // Can't add any more Telemetric information to Packet, fail silently.
        if (numHeaders == MAX_INT_DATA) {
            log_msg("[NOTE] Transit Maximum INT_DATA limit reached");
            return;
        }

        // Adding a new option word, increment appropriate values.
        hdr.ipv4_option.length = hdr.ipv4_option.length + INT_DATA_Size; 
        hdr.ipv4.ihl = hdr.ipv4.ihl + (bit<4>)(INT_DATA_Size >> 2);
        hdr.ipv4.totalLen = hdr.ipv4.totalLen + (bit<16>)INT_DATA_Size;

        // Can safely index into array.
        hdr.int_data[numHeaders].setValid();
        hdr.int_data[numHeaders].switchId   = (switch_id_t)           meta.switch_metadata.switchId;
        hdr.int_data[numHeaders].queueDepth = (queue_depth_t)         standard_metadata.enq_qdepth;
        hdr.int_data[numHeaders].queueTime  = (queue_time_delta_t)    standard_metadata.deq_timedelta;

        hdr.int_md.countHeaders = numHeaders + 1;

        log_msg("Switch: {}, Enq Depth: {}, QTime: {}", {hdr.int_data[numHeaders].switchId, hdr.int_data[numHeaders].queueDepth, hdr.int_data[numHeaders].queueTime});
    }
}

/*
 * Sink Switch deals with cloned and normal packets.
 * This method deals with normal packet processing. It is required to restore the packet to as it was
 * before INT addition.
 */
control SinkSwitchProcessing(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {
        log_msg("Sink");

        if (!hdr.ipv4.isValid()) {
            log_msg("[NOTE] Sink received non IPv4 packet, returning.");
            return;
        }

        if (!hdr.int_md.isValid()) {
            log_msg("[NOTE] Sink node couldn't find INT_MD Header, returning.");
            return;
        }
        header_count_t numHeaders = hdr.int_md.countHeaders; 

        log_msg("Num headers: {}", {numHeaders});
        log_msg("Normal Packet Ingress Time: {}", {standard_metadata.ingress_global_timestamp});

        // TODO: If you decide to support IPv4 Options, this restoration should be performed
        // By consulting INT_MD data.

        hdr.ipv4.ihl = 5;
        // We have increment both totalLen and optionLen by the same amounts,
        // and option length started from 0 (assuming no ipv4_option to begin with).
        hdr.ipv4.totalLen = hdr.ipv4.totalLen -  (bit<16>)hdr.ipv4_option.length;

        hdr.ipv4_option.setInvalid();
        hdr.int_md.setInvalid();

        // I am not aware of a better way to do this.
        hdr.int_data[0].setInvalid();
        hdr.int_data[1].setInvalid();
        hdr.int_data[2].setInvalid();
        hdr.int_data[3].setInvalid();
    }
}

/**
  * Responsible for handling the Cloned Packets destined towards the Collector
  * at the sink.
  */
control SinkSwitchCloneProcessing(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {
        // hdr.int_md.sinkIngressTime = (ingress_global_time_t) meta.sink_metadata.ingress_global_timestamp;
        hdr.int_md.sinkIngressTime = (ingress_global_time_t) standard_metadata.egress_global_timestamp;
        log_msg("Clone Packet Egress Time: {}", {hdr.int_md.sinkIngressTime});
    }
}