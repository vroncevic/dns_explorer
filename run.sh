#!/usr/bin/env bash

# Use case 1: Standard domain scan (no cluster variations, non-verbose)
python3 main.py explore --domain google.com

# Use case 2: Scan with cluster variations (size 1)
python3 main.py explore --domain google.com --cluster 1

# Use case 3: Scan with cluster size 2 and verbose logging enabled
python3 main.py explore --domain google.com --cluster 2 --verbose True

# Use case 4: Query domain DNS records (A, AAAA, MX, NS, TXT, SOA)
python3 main.py records --domain google.com

# Use case 5: Resolve forward IP and reverse hostnames for a single domain name
python3 main.py resolve --domain google.com --verbose True

# Use case 6: Query reverse DNS hostnames for an IP address
python3 main.py reverse --ip 8.8.8.8
