.. BIG-IP to XC documentation master file, created by
   sphinx-quickstart on Fri Apr 26 17:06:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BIG-IP To Distributed Cloud Conversion Frequently Asked Questions and Tips
==========================================================================

.. _disclaimer:

Disclaimer
==========

Please note that this FAQ document is intended as a general guide and is not exhaustive. While we strive to provide accurate and up-to-date information, the rapidly evolving nature of cloud technologies means that specific details may change over time. Therefore, this guide should not be considered a substitute for professional advice or detailed consultation relevant to your specific circumstances.

.. _introduction:

Introduction
============

This semi-comprehensive guide is designed to streamline your migration from F5 BIG-IP to F5 Distributed Cloud.  This document aims to address frequently asked questions that arise during the migration process, offering clear, concise answers and practical insights to ensure a smooth transition.

.. _disqualifiers:

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

API Security
------------

QKView - iHealth
================

Graphs
------

SSL Transactions
^^^^^^^^^^^^^^^^

[image]

TMM Client-Side Throughput
^^^^^^^^^^^^^^^^^^^^^^^^^^

The sum throughput of all Traffic Management Microkernel (TMM) and Packet Velocity ASIC (PVA) traffic on the client side. The following fields are represented in bits per second and packets per second: 

Client In: The sum of all ingress traffic 

Client Out: The sum of all egress traffic 

[image]

TMM Server-Side Throughput
^^^^^^^^^^^^^^^^^^^^^^^^^^

The sum throughput of all TMM and PVA traffic on the server side. The following fields are represented in bits per second and packets per second: 

Server In: The sum of all egress traffic 

Server Out: The sum of all ingress traffic 

[image]

Throughput
^^^^^^^^^^

The total throughput in and out of the BIG-IP system collected from all interfaces, including traffic processed by all Traffic Management Microkernel (TMM) and Packet Velocity ASIC (PVA), except the management interface. The following fields are represented in bits per second and packets per second: 

In: The ingress traffic to the system through its interfaces 

Out: The egress traffic from the system through its interfaces 

Service: The larger of the two values of combined client and server-side ingress traffic or egress traffic, measured within TMM. You can compare this to VE-licensed bandwidth. 

[image]

iRules
------

One of the first things to evaluate with irules, is if they are even being used. An effective way to gauge that is to check the Unused Objects under the Config Explorer. So, if you have 150 total irules, but are not using 102 of them, then that means we only need to review 48 irules, and based on historical evidence, I would estimate over 75% of those are just uncustomized redirect irules. 

[image]

Commands
--------

list /ltm virtual all-properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A straightforward way, other than reviewing the bigip.conf is to use the list /ltm virtual all-properties command and then search for “rules {”. 

IRules that can be ignored because it’s a checkbox choice in XC are redirects: 

.. code-block:: tcl
   
   rules { 
        /Common/_sys_https_redirect 
   } 

In the example QKView I am using, there are 670 instances of “rules”, and 468 instances of “/Common/_sys_https_redirect”. So, we have 202 instances of potential irules to evaluate, which is still pretty high.  But if we look at the irules, many customers have built custom redirects, which we can potentially ignore as well once we see they are just redirects. 

Let's look at an irule example, we can see it's in use, and has had 34k executions in the past 30 days. I'm sure someone will argue the point, but this is still a redirect irule. Or you could call it an apology page. It's setting the default pool, and if there aren't any active members, sending it to another page.  

[image]

This is extremely easy to do with just L7 Routes, and custom error pages. 

In this qkview, there are mostly custom redirect irules based on host headers, over and over again.  This is a manual process, so be prepared to see a lot of redirects. 

[image]

Then be prepared to see a ton of custom logging or header injections. Header Insert, Removal, and Appending can be easily done with the Load Balancer Advanced config, or more granularly via the L7 Route configs. 

In the case of this irule, it's just going to insert the header on every HTTP REQUEST. This is managed at the top-level Load Balancer Configs under More Options.

[image]
[image]

If this irule had more logic, IF host header = this.domain.com, then we would use the L7 Route options. 

[image]


show /ltm profile http global
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command will give you a quick snapshot of traffic with a virtual server with an associated HTTP profile. 

[image]

We can see that we have had about 532 million requests across all virtual servers (over the last 30 days in this example). We can also see that there were about 71 million redirects. 

This data is perfect if we are evaluating an API use-case. 

UNIX - TMOS - tmctl -a (blade)
------------------------------

This gets us to the TMSTATS collections that span usually beyond the last 30 days that the RRD Graphs might show. Scroll down to the profile_http link and click it. This will give the aggregate values as well as every individual virtual server with a HTTP profile in a table format with column headers that are clickable to sort the data based on the values. Within this you will also reveal where some dormant virtuals are that do not need to be considered for migrations. 

[image]

LTM to Load Balancing as a Service
==================================


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


SNAT Pooling
------------------

Today, XC does not support a traditional SNAT pool type configuration, however, you can scale SNAT based on nodes in a cluster.  So a 3 node cluster will have 3 IPs for SNATTING, if you need more SNAT IPs, then add more nodes. 

Traffig Group / Floating Self-IP
--------------------------------

To create the same scenario as a traffic group or floating self, you can use VRRP.  Check out Harmon's article here, where he discusses some of the CE design scenarios.  https://community.f5.com/t5/technical-articles/f5-distributed-cloud-customer-edge-site-deployment-amp-routing/ta-p/319435 

A byproduct of enabling VRRP on your cluster, and creating a common VIP, is that you can also use that common VIP as a default gateway. 

Custom Monitors
---------------

If you have been relying on custom monitors for routine tasks such as backing up data to an FTP server, sending email reports, or generating alerts based on storage availability. With F5 Distributed Cloud (XC), many of these functions are seamlessly integrated, thanks to our SaaS platform’s built-in scheduled reporting and alert capabilities.

However, if you need to perform a specific task that isn't currently supported by XC, such as invoking an API or executing a specialized function, we've got you covered. You can easily recreate this functionality in a small container script (for example, using bash) and deploy it as a scheduled task within our virtual Kubernetes environment.

For instance, if you need to activate a service policy or a network firewall rule at particular times each day, you can set up a cron job in XC. This job will operate on your schedule and interact with the XC API to execute your policies as planned.

.. code-block:: yaml

   kind: CronJob
   apiVersion: batch/v1beta1
   metadata:
     name: coleman-generic-restcurl
     labels:
       app: restcurl
       type: cron
     annotations:
       ves.io/virtual-sites: m-coleman/coleman-ves-io-ny-re
   spec:
     schedule: "30 10,20 * * 1-5" # Every weekday at 10:30, and 20:30 UTC
     jobTemplate:
       metadata:
         labels:
           app: restcurl
           type: cron
       spec:
         template:
           metadata:
             annotations:
               ves.io/workload-flavor: tiny
               ves.io/virtual-sites: m-coleman/coleman-ves-io-ny-re
           spec:
             restartPolicy: Never
             containers:
               - name: curl-worker
                 image: curlimages/curl:latest
                 imagePullPolicy: IfNotPresent
                 env:
                   - name: API_URI
                     value: "http://<tenant>.console.ves.volterra.io/api/web/namespaces"
                   - name: API_TOKEN
                     value: "APIToken <token value>"
                   - name: API_METHOD
                     value: "POST"
                   - name: API_PAYLOAD
                     value: '{"metadata": {"name": "service-policy-1","namespace": "namespace"}, "spec": { "deny_all_requests": {} } }'
                 command:
                   - "/bin/sh"
                   - "-ec"
                   - |
                     set -o nounset
                     set -o errexit
                     echo "API Call"
                     curl -s -X ${API_METHOD} -H 'Content-Type: application/json' -H "Authorization: ${API_TOKEN}" "${API_URI}"


iRules
======

If not clear, any irules that are performing redirects, header additions, rewrites, or appending values are easily migrated to L7 Routes. If the irules requires things like binary scan, that is something XC does not support today. 

IRules that focus on Access Control based on evaluating IP blocks, client source addresses, etc., are easily migrated to Service Policies. 

RULE_INIT
---------

RULE_INIT is generally used to set some static variables for use in the rest of the irule, since we don’t have any programming logic in XC in order to take advantage of this, it can generally be thrown out, but pay attention to any definitions of data groups or things like that so you can understand the irules purpose; is it pulling domain names, is it pulling client ips, etc. 

CLIENT_ACCEPTED
---------------

Depending on what is happening during CLIENT_ACCEPTED this event may not be needed, or if there is some complex action requirements it will not be a good possibility for porting. Most customers use this to log client ip/prefix data, or select a pool based on an identifying client attribute, this can be done via L7 Routes.

