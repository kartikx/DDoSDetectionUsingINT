1. Ensure in the control plane that you don't add values to INTSwitchRole table that may be greater than 2 bits in length.
2. Need to be aware of MTU.

Design Decisions
1. Source and Transit will not add INT headers if egress port is not = 2. `NOTE` You will need to keep changing this as topology changes. 

TODOs
1. How to raise errors?
3. Currently, I am assuming that a packet flowing into Source Switch, won't already have an ipv4 options header. I should replace this by a check, and then storing info into the INT_MD header to be replaced back at the source.
4. Read into applications of IPV4Option to see if I need to set length of options etc. because I don't need that from my implementation pov. Hence, I would only need to cache the option type. => Consensus: I should do this (Might allow reverse flow as well).
5. How do I make the int_data invalid at the Sink? Needs a loop, maybe I can do that in the deparser?
6. Operations like Ping won't work because INT doesn't work bidirectionally, I need to be sure that traffic flows in one way only, because if source adds the header then hosts might not be able to understand it. !!! I think it might be a good idea to use IPv4Options properly after all, if you can set the entire INT headers + data such that it appears like an option, then maybe hosts might ignore it all !!!.

8. Read into Checksums and fix it.
11. Remove transit/sink node drop on not finding INT_MD, this leads to reverse flows being dropped completely.
12. INT A Survey, mentions that INT Header should be 8+8+8 (Control Header + Seq Number + Bitmap).

## Implementing the IPv4 Options solution
* It may be possible that the Source receives a packet which already has IPv4 Options.
* In this case, the Parser will notice that the value of IHL is >5, however the option headers won't be parsed since the option number would be incorrect.
* Hence the source will add the INT header and data.
* On the transit header, the parser will notice that option value is 31. 
* However, the parser might accidentally parse an original option header as the INT header. This is not good.

### Notes
* IPv4 Options is a part of the IPv4 header itself. So every INT header (+data) could be disguised as an IPv4 Option?
* The options are 0-40 bytes in length, and must be a multiple of 4. Giving us a total of 10 options that we could include.

Questions to ask:
1. How to invalidate a header stack?
2. How to raise error messages in control blocks.
3. How to store entry in a table without key, single match only.

Question to clarify with Sir:
1. Is my approach of handling reverse flow issues correct?

Things to keep track of when Topology Changes
1. Forwarding Tables will change.
2. Collector sniff port will change.
