---
title: "LiteLLM vs Envoy AI Gateway: breadth is table stakes"
date: 2026-07-19
author: "Feisal Adur"
description: "Provider count used to matter. Now most of the list is the same OpenAI-compatible integration wearing different base URLs."
draft: false
---

I'm on vacation, which means in practice that I have more time to play around on my homelab. This week I needed an inference gateway. The default answer is LiteLLM, and I've used it enough to know why it's the default. I picked Envoy AI Gateway instead.

And honestly, part of the reason I picked it is that I wanted to try something new. The rest of this post is really me re-examining my assumptions about the defaults.

The first question is provider coverage. LiteLLM supports a hundred-plus providers; Envoy AI Gateway lists sixteen.

## What the provider count is made of

LiteLLM won its position honestly. In 2023 and 2024, every provider shipped a different API, and a Python proxy that translated all of them into one OpenAI-shaped interface solved a real problem. The provider count was the product.

Then the market converged. New providers stopped inventing API schemas and started shipping OpenAI-compatible endpoints, because compatibility is free distribution: every SDK, every gateway, every agent framework already speaks the dialect. The result is that most of any gateway's provider list is now the same integration wearing different base URLs.

Which means the headline number measures the wrong thing. A hundred providers where ninety are OpenAI-compatible is ten integrations and ninety config entries.

## Adding an unsupported provider was configuration, not implementation

I wanted Moonshot AI on my home gateway. Envoy AI Gateway doesn't list it as a supported provider, but Moonshot speaks the OpenAI schema, so adding it looked like normal infrastructure work: tell the gateway where it lives, how to authenticate, and which model names should go there.

![For an OpenAI-compatible provider, this is just endpoint, auth, and routing.](/images/openai-compatible-provider.svg)

```yaml
apiVersion: aigateway.envoyproxy.io/v1beta1
kind: AIServiceBackend
metadata:
  name: moonshot
  namespace: envoy-ai-gateway-system
spec:
  schema:
    name: OpenAI
  backendRef:
    name: moonshot
    group: gateway.envoyproxy.io
    kind: Backend
    port: 443
```

That's more than one block of YAML, but it's still configuration. Nothing required a plugin, a fork, or a custom translation layer. I didn't have to wait on upstream. The gateway already knew how to speak OpenAI; I just had to point it at another endpoint, wire up auth, and add a route.

In practice, "unsupported provider" meant "not pre-packaged," not "architecturally blocked." This is what OpenAI-compatibility convergence does to the coverage argument: if the provider speaks the common dialect, adding it is infrastructure work, not integration work.

## Where translation still earns its keep

The compatibility story has real exceptions. Anthropic's native Messages API, AWS Bedrock, and GCP Vertex all diverge enough that genuine schema translation still matters. This is the part of LiteLLM's translation layer that still matters.

Envoy AI Gateway covers that narrower set too. It ships translation for the APIs that actually differ, including Anthropic Messages to Bedrock Converse, so an Anthropic-native client can reach Bedrock without switching protocols. Once you separate the genuinely different APIs from the OpenAI-compatible ones, provider coverage stops saying very much.

## What's left to compare

Strip out breadth and you're left with the boring infrastructure questions, which is where the two projects stop resembling each other.

Data plane. LiteLLM is a Python process. Envoy AI Gateway is Envoy: the same proxy already handling ingress for a large share of cloud-native deployments, with a decade of production hardening behind it. Everything downstream of this choice, from connection handling to failure modes under load, follows from it.

Config model. LiteLLM is a YAML file that grows until someone is afraid of it. Envoy AI Gateway is Gateway API CRDs: `AIGatewayRoute`, `AIServiceBackend`, `BackendSecurityPolicy`, each a typed Kubernetes resource with a schema, RBAC, and a reconciliation loop. Routes, credentials, and rate limits are separate objects owned by separate teams, which is how a platform team actually wants to run this.

Cross-cutting concerns. In LiteLLM, auth, rate limiting, and observability are application features, implemented in Python inside the proxy. In Envoy AI Gateway they're gateway features: token-based rate limiting in the filter chain, credential handling with rotation in `BackendSecurityPolicy`, metrics from the same Envoy telemetry you already scrape. The AI gateway stops being a special snowflake in your infrastructure and becomes another route on the gateway you already operate.

Maturity cuts the other way. LiteLLM has years of accumulated edge-case handling for provider quirks. Envoy AI Gateway hit 1.0 in June 2026; its core CRDs only reached v1beta1 this spring. It's production-hardened by the companies building it, Bloomberg and Tetrate among them, but it has fewer miles on it, and you'll occasionally be the first person to hit something.

## Verdict

If you need a multi-provider proxy on a VM this afternoon, LiteLLM is still the right default. That's what it's good at, and its popularity makes sense on those terms.

I picked Envoy AI Gateway because it fit the way I already run the homelab. Local Ollama models and cloud models sit behind the same OpenAI-compatible endpoint. Secrets go through the same 1Password path as everything else. Adding a provider is backend config and a route.

Provider count matters less to me now. Once most of the market converged on the OpenAI schema, breadth stopped being the interesting question. The question is whether model traffic fits cleanly into the rest of the system.

In my case, Envoy AI Gateway did.
