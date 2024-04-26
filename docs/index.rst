# BIG-IP To Distributed Cloud Conversion Frequently Asked Questions and Tips

## Table of Contents

- Disclaimer
- Introduction
- Disqualifiers
- Access Policy Manager
- Local Traffic Manager
- Tools
- APM to XC or Service Chaining
- API Security
- QKView - iHealth
- show /ltm profile http global
- QKView / iHealth – Commands
  - Commands --> UNIX --> TMOS --> tmctl –a(blade)
  - list /ltm virtual all-properties
- LTM to LbaaS
- LTM – Customer Edge (CE) Reserved Ports
- LTM – SNAT (Pooling)
- LTM – Traffic Group / Floating Self
- LTM – Custom Monitor Shenanigans
- QKView / iHealth – Commands
- QKView / iHealth – Graphs
  - SSL Transactions
  - TMM Client-Side Throughput
  - TMM Server-Side Throughput
  - Throughput
- iRules
  - RULE_INIT
  - CLIENT_ACCEPTED
  - CLIENTSSL_CLIENTCERT
  - LB_SELECTED & LB_FAILED
  - HTTP_REQUEST
  - HTTP_REQUEST_DATA
  - HTTP_RESPONSE
  - HTTP_RESPONSE_DATA
  - ACCESS_SESSION_STARTED, ACCESS_POLICY_AGENT_EVENT, ACCESS_POLICY_COMPLETED, ACCESS_ACL_DENIED, ACCESS_ACL_ALLOWED, REWRITE_REQUEST_DONE, REWRITE_RESPONSE_DONE, ACCESS_SESSION_CLOSED
  - Logging
- Example Conversions in Terraform
- AWAF to WAAP
- Policy Supervisor
- Customer Edge Sizing
- Example(s) (Don’t know where to place yet)

## Disclaimer

This FAQ is not all inclusive.

## Introduction

## Disqualifiers

This is a list of use-cases that can be used to immediately disqualify a migration, with some caveats. There are service chaining use-cases that could still work, or ways to implement policies to redirect traffic to a BIG-IP instead of XC, or ways to inline NGINX into XC to carry out many of the same effects.

### Access Policy Manager

Not all use-cases within APM will be disqualifiers. Just note that the following are not currently supported in XC.

- Access services that require Match Across.
  - DTLS - SSLVPN
  - PCOIP – VDI (BLAST works fine)
There are some workable use-cases around Federated Authentication and proxy/service chaining.

### Local Traffic Manager

There are very few disqualifiers for LTM.

- Load Balancing services that require Match Across.
  - DTLS
  - PCOIP
- Streaming Profiles. We do not support streaming content today in XC LBs.
  - E.g., Rewriting HTML page content.
- OneConnect

## Tools

The following are tools available to use today.  It's important to note that none of these tools are 100%. It is highly recommended to work with an XC Specialist to help in migration from other platforms to XC.

- iHealth: <https://ihealth2.f5.com/>
- VS Code Extension: <https://marketplace.visualstudio.com/items?itemName=F5DevCentral.vscode-f5>
  - <https://f5devcentral.github.io/vscode-f5/#/xcDiagnostics>
- Policy Supervisor: <https://policysupervisor.io/>
- BIND to XC Conversion tool: <https://github.com/Mikej81/BINDtoXCDNS>
- Domain Keep-Alive Analyzer: <https://keepalive.f5-sa.myedgedemo.com/>

## APM to XC Service Chaining

We covered the disqualifiers, but there are some that will work fine, like service chaining for Federation, or header validation.

[image]
