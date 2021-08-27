#define MAX_INT_DATA 4

const bit<16> TYPE_IPV4 = 0x800;
const bit<5> INT_OPTION_TYPE = 31;

typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

typedef bit<7> header_count_t;

typedef bit<16> queue_depth_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<6>    dscp;
    bit<2>    ecn;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr; 
}

header ipv4_option_t {
    bit<1> copied;
    bit<2> class;
    bit<5> option;
    bit<8> length;
}

header int_md_t {
    bit<5> originalOptionValue;
    bit<4> originalIhl;
    header_count_t countHeaders;
}

header int_data_t {
    queue_depth_t queueDepth;
}

/*
The parser is required to carry information between states.
*/
struct parser_metadata_t {
    /*
     * Stores the number of remainint INT Data headers to be parsed.
     * Keeps getting decremented to recursivelt parse the entire INT Header
     * Stack.
     */
    header_count_t numHeadersRemaining;
}

struct switch_metadata_t {
    // Switch ID for this switch. Extracted from `switchInfo` table.
    bit<8> switchId;
    
    // The INT Role {Source, Transit, Sink} for this Switch. Extracted from `switchInfo` table.
    bit<8> switchINTRole;
}

struct metadata {
    parser_metadata_t parser_metadata;
    switch_metadata_t switch_metadata;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    ipv4_option_t ipv4_option;
    int_md_t int_md;
    int_data_t[MAX_INT_DATA] int_data;
}
