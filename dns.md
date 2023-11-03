# Notes on How DNS Works

- **DNS Request**:
  - A request for mapping a hostname to an IP address (e.g., `tiktok.com` to `192.168.1.1`).
  - Sent from a client to a DNS server listed in `etc/resolve.conf`.
  - Uses port 53 in the UDP header.
  - DNS requests and responses can be observed using packet capture tools like Wireshark.
- **Name Assignment and Hierarchical Control**:
  - Names and IP mappings are stored in a hierarchical, distributed database.
  - Name servers controlled by different authorities provide information about parts of the name space.
  - Example: `puffer.stanford.edu` is divided into parts: root (`""`), `edu`, `stanford`, and `puffer`.
- **DNS Lookup**:
  - Recursive process through the distributed DNS database.
  - In practice, a DNS server usually performs the recursive lookup and may use cached responses.
  - DNS replies have an expiration date indicating the validity of the IP mapping.
- **Resources**: Further understanding can be gained through online resources and forums.

## Types of Domains

### **1. Generic Domains**
   - Examples:
     - `.com` (Commercial)
     - `.edu` (Educational)
     - `.mil` (Military)
     - `.org` (Non-profit organization)
     - `.net` (Similar to commercial)

### **2. Country Domains**
   - Examples:
     - `.in` (India)
     - `.us` (United States)
     - `.uk` (United Kingdom)

### **3. Inverse Domain**
   - Used for IP to domain name mapping.
   - Example:
     - To find the IP address for `geeksforgeeks.org`, use `nslookup www.geeksforgeeks.org`.

## Hierarchy of Name Servers

### **1. Root Name Servers**
   - Contacted by name servers that can't resolve a name.
   - Contacts authoritative name server for name mapping if not known.
   - Returns the IP address to the host.

### **2. Top-Level Servers**
   - Responsible for top-level domains (e.g., `.com`, `.org`, `.edu`, `.uk`, `.fr`, etc.).
   - Contains information about authoritative domain servers for second level domains.

### **3. Authoritative Name Servers**
   - Organization's DNS server providing authoritative hostName to IP mappings.
   - Can be maintained by an organization or service provider.
   - Example:
     - To reach `cse.dtu.in`, root DNS server directs to top level domain server and then to authoritative domain name server.

## Domain Name Server Workflow
- **Process**:
   1. **Client Request**: Client sends a request to local name server.
   2. **Root Server**: If local server can't find the address, it sends a request to the root name server.
   3. **Intermediate/Authoritative Server**: Root server routes the query to an intermediate or authoritative name server.
   4. **IP Address Retrieval**: Intermediate server knows the authoritative server, and IP address is returned to the local name server and then to the host.

## Recursive Resolution
- **Process**:
   1. **Query Generation**: Application generates a DNS Query for destination IP.
   2. **Local Server Check**: Local DNS server checks if it knows the IP address.
   3. **Root Server Check**: If not, query is sent to root name server, which directs to respective Top-Level Domain server.
   4. **Destination's Local DNS Server**: If top-level domain server doesn't have mapping, it directs to destination's local DNS server.
   5. **IP Address Retrieval**: IP Address is retrieved and sent back through the hierarchy to the host.

## Conclusion
- DNS is a systematic, hierarchical structure that facilitates the translation of human-readable domain names to IP addresses.
