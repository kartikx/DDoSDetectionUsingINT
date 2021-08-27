1. Ensure in the control plane that you don't add values to INTSwitchRole table that may be greater than 2 bits in length.
2. Need to be aware of MTU.

TODOs
1. How to raise errors?
2. Simple_int.p4 int_table is keyless. So I could have all associated metadata {intRole, switchId etc.} in a single row of the table, and then store it in the metadata. What does the syntax of table row without => mean?
3. Currently, I am assuming that a packet flowing into Source Switch, won't already have an ipv4 options header. I should replace this by a check, and then storing info into the INT_MD header to be replaced back at the source.
4. Read into applications of IPV4Option to see if I need to set length of options etc. because I don't need that from my implementation pov. Hence, I would only need to cache the option type. => Consensus: I should do this (Might allow reverse flow as well).
5. How do I make the int_data invalid at the Sink? Needs a loop, maybe I can do that in the deparser?
6. Operations like Ping won't work because INT doesn't work bidirectionally, I need to be sure that traffic flows in one way only, because if source adds the header then hosts might not be able to understand it. !!! I think it might be a good idea to use IPv4Options properly after all, if you can set the entire INT headers + data such that it appears like an option, then maybe hosts might ignore it all !!!.

Current Status: Source and Sink acting correctly, try to resolve current issues before proceeeding to next step.
For some reason the receive.py is not printing out the message properly, but the payload is being show on showing the packet. This is an issue, and indicate that packets are being tampered with.

7. Correctly IPv4 Option-ize Source Transit and Sink switches. Is 31 something to be ignored?

Questions to ask:
1. How to invalidate a header stack?
2. How to raise error messages in control blocks.
3. How to store entry in a table without key, single match only.