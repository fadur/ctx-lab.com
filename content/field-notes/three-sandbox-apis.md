---
title: "Three Sandbox APIs, Reviewed Honestly"
date: 2026-06-04
author: "Feisal Adur"
description: "An agent that writes and runs its own code needs somewhere to run it. I looked at three primitives: agent-sandbox, OpenSandbox, and Cloudflare Sandbox."
draft: false
---

I've built a lot of agents. Most of them, at some point, need to run code — write a file, execute a shell command, check the output, decide what to do next. The way you give an agent that capability is with a sandbox, and from the agent's perspective it's just another tool:

```typescript
sandbox.exec("/workspace", "date")
// → { stdout: "Wed Jun  4 09:15:22 UTC 2026", exitCode: 0 }
```

The agent calls it, gets a result, moves on.

That's it. But that simple interface is what lets you embed complicated workflows and run them at scale — not one agent doing one thing, but many, each in its own environment, writing code, running it, reading the output, doing it again.

I looked at three primitives: agent-sandbox, OpenSandbox, and Cloudflare Sandbox.

**What I looked at**

Three things, in order of how much they matter when you're actually building on top of one of these.

**Lifecycle.** How do you create a sandbox, hold it across a session, and throw it away? Warm pools, session binding, and clean teardown matter more than they sound — cold-start latency compounds quickly when you're spinning up sandboxes per workflow.

**Exec model.** How does a command actually reach the sandbox? A direct path to the process matters — under agent load you're making a lot of tool calls, and anything that routes through a shared control plane becomes a bottleneck or a timeout problem fast.

**DX.** What's it actually like to build with? SDK quality, what the API surface feels like, what's missing that you'd expect to be there.

| | Lifecycle | Exec model | DX |
|---|---|---|---|
| agent-sandbox | ✓ | ✗ | ✗ |
| OpenSandbox | ✗ | ✓ | ✓ |
| Cloudflare Sandbox | ✗ | ✗ | ✓ |

## agent-sandbox[^2]

A `Sandbox` CRD and controller, Apache-2.0, out of KubeCon Atlanta last November. Declare a `Sandbox`, the controller reconciles a pod with gVisor or Kata isolation. `SandboxClaim`/`SandboxWarmPool` absorb creation churn so you're not cold-booting a pod per session.

The lifecycle model is right. `kubectl get sandboxes` works. Reconciliation, status conditions, RBAC on the object all behave the way you'd expect from a Kubernetes-native resource.

It has no execution protocol of its own. Exec rides the standard Kubernetes remotecommand path: the API server's `/exec` subresource, streamed through kubelet. Every command an agent runs is a round-trip through kube-apiserver, a shared control-plane component that wasn't built to be the hot path for thousands of concurrent agent sessions hammering it with tool calls. The same limitation shows up a second way: long agent think-time looks idle to any proxy in the path, and gets killed by timeouts that have nothing to do with the workload.

Still `v1alpha1`. No opinion on workload identity. You bring your own SPIFFE/SPIRE.

## OpenSandbox[^3]

REST API platform, SDKs in Python, Go, TypeScript, Java, C#. On Kubernetes, `opensandbox-server` talks to the API directly to create a Pod plus PVC, and an `execd` sidecar in every pod handles command dispatch over its own protocol. An ingress component routes calls to the right pod's `execd` by sandbox ID.

That's the part worth taking: exec never touches the Kubernetes API server. It's a direct path to a sidecar, which is the right shape for high-frequency tool calls under agent load. The file API is the most complete of the three, with full CRUD, permissions, and glob search. It also ships a per-sandbox egress policy API and an MCP server, which the other two don't have.

The cost is that sandbox state lives outside Kubernetes, in the server's own database. There's no `kubectl get sandboxes`, no reconciliation loop, no native RBAC on the object. If you already own CRDs and reconcile against etcd for everything else, this is a second, disconnected state store with no way to join it to the first.

## Cloudflare Sandbox[^4]

TypeScript SDK for Workers, a Durable Object underneath. `sandbox.exec()` with streaming, a WebSocket PTY with an `xterm.js` addon, `inotify` file watching, `sandbox.gitCheckout()`, multiple isolated shell sessions per sandbox, and backup/restore to R2 with copy-on-write.

This is the best raw DX of the three. The PTY terminal, git checkout as a first-class call, file watching, and session isolation are all ahead of what the other two ship.

It's also a Durable Object, TypeScript-only, locked to the Cloudflare runtime. You can't call it from a Go CLI or an Elixir operator without a Worker proxy in front of it. There's no TTL or explicit renew; lifetime is whatever the Durable Object gives you. There's no egress control surface at all. If you're running on your own cluster with data residency requirements, none of that is negotiable.

## What's missing

agent-sandbox has the right lifecycle and no exec story. OpenSandbox has the right exec model and lifecycle state that lives outside Kubernetes. Cloudflare Sandbox has the best DX and you can't self-host it.

None of them is the complete picture yet, which makes it an interesting space to watch. Out of the three, I keep coming back to agent-sandbox — the Kubernetes-native lifecycle management is just indispensable, and that's the piece that's hardest to bolt on after the fact.[^1]

[^1]: AWS Lambda MicroVMs launched June 22 — haven't run it yet, so take this as a first read rather than a verdict. On paper the lifecycle model looks genuinely good, better than anything else here. But every AWS serverless product ships with the same tax: CloudFormation to provision it, IAM to gate it, and IAM's access model is miserable to work with compared to just calling an API. Cloudflare's sandbox works out of the box with none of that ceremony. Based on what AgentCore has been like to actually use, I'm not optimistic this one breaks the pattern. Will update once I've built against it. [AWS blog](https://aws.amazon.com/blogs/aws/run-isolated-sandboxes-with-full-lifecycle-control-aws-lambda-introduces-microvms/).
[^2]: [github.com/kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox)
[^3]: [github.com/opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)
[^4]: [cloudflare.com/products/sandboxes](https://www.cloudflare.com/products/sandboxes/)
