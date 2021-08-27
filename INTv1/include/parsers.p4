error { IPHeaderWithoutOptions }

parser MyParser(packet_in packet,
              out headers hdr,
              inout metadata meta,
              inout standard_metadata_t standard_metadata) {
    /*
    Currently dealing with only IPv4 packets.
    */
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    /*
    The Packet __might__ have an INT packet. I need a way
    to indicate this.
    If I use IPv4Options to do this, I need to ensure that the
    option is restored. Read more into INT_SPEC and IPv4Options for this.
    */
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        verify(hdr.ipv4.ihl >= 5, error.IPHeaderWithoutOptions);
        transition select(hdr.ipv4.ihl) {
            5: accept;
            default: parse_ipv4_option; 
        }
    }

    state parse_ipv4_option {
        packet.extract(hdr.ipv4_option);
        transition select(hdr.ipv4_option.option) {
            INT_OPTION_TYPE: parse_int;
            default: accept;
        }
    }

    /*
    At this point, I am sure that the packet has INT Headers.
    */
    state parse_int {
        packet.extract(hdr.int_md);
        meta.parser_metadata.numHeadersRemaining = hdr.int_md.countHeaders;
        transition select(meta.parser_metadata.numHeadersRemaining) {
            0: accept;
            default: parse_int_data;
        }
    }
    
    /*
    TODO enable logging to verify that this works.
    */
    state parse_int_data {
        packet.extract(hdr.int_data.next);
        meta.parser_metadata.numHeadersRemaining = meta.parser_metadata.numHeadersRemaining - 1;
        transition select(meta.parser_metadata.numHeadersRemaining) {
            0: accept;
            default: parse_int_data;
        }
    }
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv4_option);
        packet.emit(hdr.int_md);
        packet.emit(hdr.int_data);
    }
}