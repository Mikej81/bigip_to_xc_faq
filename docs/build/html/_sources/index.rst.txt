.. BIG-IP to XC documentation master file, created by
   sphinx-quickstart on Fri Apr 26 17:06:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BIG-IP To Distributed Cloud Conversion Frequently Asked Questions and Tips
==========================================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

#. Disclaimer
#. Introduction
#. Disqualifiers
#. Access Policy Manager
#. Local Traffic Manager
#. Tools
#. APM to XC or Service Chaining
#. API Security
#. QKView - iHealth
  *  show /ltm profile http global
  *  Commands -- UNIX -- TMOS -- tmctl -a(blade)
  *  list /ltm virtual all-properties
#. LTM to LbaaS
#. LTM - Customer Edge (CE) Reserved Ports
#. LTM - SNAT (Pooling)
#. LTM - Traffic Group / Floating Self
#. LTM - Custom Monitor Shenanigans
#. QKView / iHealth - Commands
#. QKView / iHealth - Graphs
  * SSL Transactions
  * TMM Client-Side Throughput
  * TMM Server-Side Throughput
  * Throughput
#. iRules
  * RULE_INIT
  * CLIENT_ACCEPTED
  * CLIENTSSL_CLIENTCERT
  * LB_SELECTED & LB_FAILED
  * HTTP_REQUEST
  * HTTP_REQUEST_DATA
  * HTTP_RESPONSE
  * HTTP_RESPONSE_DATA
  * ACCESS_SESSION_STARTED, ACCESS_POLICY_AGENT_EVENT, ACCESS_POLICY_COMPLETED, ACCESS_ACL_DENIED, ACCESS_ACL_ALLOWED, REWRITE_REQUEST_DONE, REWRITE_RESPONSE_DONE, ACCESS_SESSION_CLOSED
  * Logging
#. Example Conversions in Terraform
#. AWAF to WAAP
#. Policy Supervisor
#. Customer Edge Sizing
#. Example(s) (Don’t know where to place yet)

Disclaimer
==========

This FAQ is not all inclusive.

Introduction
============

Disqualifiers
=============

This is a list of use-cases that can be used to immediately disqualify a migration, with some caveats. There are service chaining use-cases that could still work, or ways to implement policies to redirect traffic to a BIG-IP instead of XC, or ways to inline NGINX into XC to carry out many of the same effects.

Access Policy Manager
=====================

Not all use-cases within APM will be disqualifiers. Just note that the following are not currently supported in XC.

#. Access services that require Match Across.
  * DTLS - SSLVPN
  * PCOIP – VDI (BLAST works fine)
There are some workable use-cases around Federated Authentication and proxy/service chaining.

#. NTLM

Local Traffic Manager
=====================

There are very few disqualifiers for LTM.

#. Load Balancing services that require Match Across.
  * DTLS
  * PCOIP
#. Streaming Profiles. We do not support streaming content today in XC LBs.
  * E.g., Rewriting HTML page content.
#. OneConnect

Tools
=====

The following are tools available to use today.  It's important to note that none of these tools are 100%. It is highly recommended to work with an XC Specialist to help in migration from other platforms to XC.

- iHealth: `https://ihealth2.f5.com/`
- VS Code Extension: `https://marketplace.visualstudio.com/items?itemName=F5DevCentral.vscode-f5`
  - `https://f5devcentral.github.io/vscode-f5/#/xcDiagnostics`
- Policy Supervisor: `https://policysupervisor.io/`
- BIND to XC Conversion tool: `https://github.com/Mikej81/BINDtoXCDNS`
- Domain Keep-Alive Analyzer: `https://keepalive.f5-sa.myedgedemo.com/`

APM to Ditributed Cloud (Service Chaining)
==========================================

We covered the disqualifiers, but there are some that will work fine, like service chaining for Federation, or header validation.

[image]

API Security
============

QKView - iHealth
================

#. show /ltm profile http global

This command will give you a quick snapshot of traffic with a virtual server with an associated HTTP profile. 

[image]

We can see that we have had about 532 million requests across all virtual servers (over the last 30 days in this example). We can also see that there were about 71 million redirects. 

This data is perfect if we are evaluating an API use-case. 

#. UNIX - TMOS - tmctl -a (blade)

This gets us to the TMSTATS collections that span usually beyond the last 30 days that the RRD Graphs might show. Scroll down to the profile_http link and click it. This will give the aggregate values as well as every individual virtual server with a HTTP profile in a table format with column headers that are clickable to sort the data based on the values. Within this you will also reveal where some dormant virtuals are that do not need to be considered for migrations. 

[image]

LTM to Load Balancing as a Service
==================================

LTM to Customer Edge
====================

The following ports can not be used when advertising services on a Customer Edge. 

.. list-table:: Reserved Ports
   :widths: 50 50
   :header-rows: 0

   * - 22
     - 99
   * - 53
     - 10249

+----+-------+
| 22 | 999   |
| 53 | 10249 |
| 68 | 10250 |
| 323 | 10251 |
| 500 | 10252 |
| 1067 | 10256 | 
| 2379 | 10257 | 
| 2380 | 10259 | 
| 4500 | 18091 | 
| 5355 | 18092 | 
| 6443 | 18093 | 
| 8005 | 18095 | 
| 8007 | 22222 | 
| 8087 | 23790 | 
| 8443 | 23791 | 
| 8444 | 23801 | 
| 8505 | 23802 | 
| 8507 | 28000-32767 | 
| 9007 | | 
| 9090 | | 
| 9153 | | 
+------+-+