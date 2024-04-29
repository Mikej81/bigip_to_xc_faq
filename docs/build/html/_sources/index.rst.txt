.. BIG-IP to XC documentation master file, created by
   sphinx-quickstart on Fri Apr 26 17:06:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BIG-IP To Distributed Cloud Conversion Frequently Asked Questions and Tips
==========================================================================

.. _disclaimer:
==========
Disclaimer
==========

This FAQ is not all inclusive.

.. _introduction:
============
Introduction
============

.. _disqualifiers:
=============
Disqualifiers
=============

This is a list of use-cases that can be used to immediately disqualify a migration, with some caveats. There are service chaining use-cases that could still work, or ways to implement policies to redirect traffic to a BIG-IP instead of XC, or ways to inline NGINX into XC to carry out many of the same effects.

Access Policy Manager
=====================

Not all use-cases within APM will be disqualifiers. Just note that the following are not currently supported in XC.

#. Access services that require Match Across.

   * DTLS - SSLVPN
   * PCOIP - VDI BLAST works fine

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

.. _iHealth: https://ihealth2.f5.com/
.. _VS Code Extension: https://marketplace.visualstudio.com/items?itemName=F5DevCentral.vscode-f5
.. _Policy Supervisor: https://policysupervisor.io/
.. _BIND to XC Conversion tool: https://github.com/Mikej81/BINDtoXCDNS
.. _Domain Keep-Alive Analyzer: https://keepalive.f5-sa.myedgedemo.com/

- iHealth: `iHealth <iHealth_>`_
- VS Code Extension: `VS Code Extension <VS Code Extension_>`_
  - `VS Code Extension Diagnostics <VS Code Extension_>`_
- Policy Supervisor: `Policy Supervisor <Policy Supervisor_>`_
- BIND to XC Conversion tool: `BIND to XC Conversion tool <BIND to XC Conversion tool_>`_
- Domain Keep-Alive Analyzer: `Domain Keep-Alive Analyzer <Domain Keep-Alive Analyzer_>`_

APM to Ditributed Cloud (Service Chaining)
==========================================

We covered the disqualifiers, but there are some that will work fine, like service chaining for Federation, or header validation.

[image]
------------
API Security
------------

QKView - iHealth
================

-----------------------------
show /ltm profile http global
-----------------------------

This command will give you a quick snapshot of traffic with a virtual server with an associated HTTP profile. 

[image]

We can see that we have had about 532 million requests across all virtual servers (over the last 30 days in this example). We can also see that there were about 71 million redirects. 

This data is perfect if we are evaluating an API use-case. 
------------------------------
UNIX - TMOS - tmctl -a (blade)
------------------------------

This gets us to the TMSTATS collections that span usually beyond the last 30 days that the RRD Graphs might show. Scroll down to the profile_http link and click it. This will give the aggregate values as well as every individual virtual server with a HTTP profile in a table format with column headers that are clickable to sort the data based on the values. Within this you will also reveal where some dormant virtuals are that do not need to be considered for migrations. 

[image]

LTM to Load Balancing as a Service
==================================

--------------------
LTM to Customer Edge
--------------------

The following ports can not be used when advertising services on a Customer Edge. 

.. list-table:: Reserved Ports
   :widths: 50 50
   :header-rows: 0

   * - 22
     - 53 
   * - 68
     - 323
   * - 500
     - 1067
   * - 2379
     - 2380
   * - 4500
     - 5355
   * - 6443
     - 8005
   * - 8007
     - 8087
   * - 8443
     - 8444
   * - 8505
     - 8507
   * - 9007
     - 9090
   * - 9153
     - 9999
   * - 10249
     - 10250
   * - 10251
     - 10252
   * - 10256
     - 10257
   * - 10259
     - 18091
   * - 18092
     - 18093
   * - 18095
     - 22222
   * - 23790
     - 23791
   * - 23801
     - 23802
   * - 28000 - 32767 (volterra)
     - 28000 - 32767 (kubernetes) 

------------------
LTM - SNAT Pooling
------------------

Today, XC does not support a traditional SNAT pool type configuration, however, you can scale SNAT based on nodes in a cluster.  So a 3 node cluster will have 3 IPs for SNATTING, if you need more SNAT IPs, then add more nodes. 

