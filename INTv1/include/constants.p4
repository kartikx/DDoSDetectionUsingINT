#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1

enum bit<2> INTRole {
    Source    = 0,
    Transit   = 1,
    Sink      = 2,
    Undefined = 3
}

/**
  * The Source switch has been configured to attach INT headers to a packet only
  * if it is scheduled on a path towards the Sink.
  * This prevents attaching INT headers on reverse flows (from Sink to Source for example).
  * This constant stores the egress port whose packets must be attached with INT Headers.
  */
const bit<9> INTSourceEgressPort = 2;

/**
  * Same as above, but for Transit Switches.
  * A more complicated topology might lead to complications.
  * For example, if we have multiple transit switches but they don't have the same
  * port leading towards the Sink.
  */
const bit<9> INTTransitEgressPort = 2;

const bit<32> SinkSessionID = 100;