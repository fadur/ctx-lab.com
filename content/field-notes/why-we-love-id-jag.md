---
title: "Why I Like ID-JAG"
date: 2026-07-03
author: "Feisal Adur"
description: "Everyone bolts human OAuth onto a bot and hopes the bot behaves. ID-JAG is the first identity model I've seen that treats agents as their own category."
draft: false
---

A well-built agentic system uses OAuth correctly. Each agent has its own app registration, not a shared service account. When it acts on your behalf, it uses an On-Behalf-Of flow — your identity token in, a narrowly scoped delegated token out, valid only for the downstream resource it needs. That's the right shape for a single hop.

The harder question is what happens in a chain.

## The chain problem

When your assistant doesn't just call one service but orchestrates a sequence — travel booking hands off to an approval workflow, which hands off to an expense system — each hop needs to do three things before it can make the next call.

First, it needs a new token scoped to the *next* service, which means another round trip to the identity provider for a fresh OBO exchange. Second, it needs to carry forward proof of the full delegation chain — not just "this agent has permission" but "this agent was called by that agent, acting on behalf of this user, who authorised the original request." Third, it needs to bind that token to the specific process making the call, so it can't be lifted from memory and replayed somewhere else.

![What each hop requires in a properly-built multi-agent chain](/proper-chain-delegation.svg)

That's a round trip to the IDP at every hop, a chain assertion format you define and propagate, and validation logic at every downstream service that knows how to read the full chain — not just the leaf token. It's all solvable. Teams do build it. But it's a meaningful amount of custom plumbing, it has to be right at every hop, and every new service that joins the chain has to implement the same validation correctly.

## What Entra already gives you

Microsoft went further than a plain token exchange here. Entra now has a feature called Agent ID[^1] that gives each agent its own identity, not a shared app registration that every copy of your assistant uses, but a distinct record for "this specific travel-booking assistant," with its own policies and no login credentials of its own to leak. When that assistant acts on your behalf, Entra issues a token that says, natively, this action was taken by you, through this specific agent. That's built into the platform, not something I had to bolt on myself.

![Entra On-Behalf-Of token exchange flow](/entra-obo-flow.svg)

That's genuinely good, and a big step up from the shared-token setups most agent tooling still ships with today. But it only works inside one Entra tenant, meaning inside one company's identity boundary. And most of what an assistant actually touches doesn't live there.

Take the receipts from that expense report. Say they get archived to a storage bucket in AWS once the report is filed. Your travel assistant authenticated you through Entra to get this far, but AWS's S3 has never heard of an Entra user and has no idea what an Entra token means. It only understands AWS's own permission model, IAM roles and policies, a completely separate identity system with no built-in concept of "the same person who logged into Entra a moment ago." The instant your assistant crosses that line, from a Microsoft-authenticated action to a resource sitting in a different company's cloud, it needs a way to prove who it is and who it's acting for that has nothing to do with Entra. The usual workaround is a static AWS key baked into the agent, or one shared service role handed to every agent in the fleet. Which puts you right back at the same problem: one broad, reusable credential that any agent, or anything that steals it, can use as far as it reaches.

## The part I'm actually excited about

The boundary that matters isn't Entra versus nothing, it's inside one company's walls versus everywhere else an agent actually has to go. The IETF's ID-JAG draft[^2] and the related XAA[^3] work are aimed exactly at that seam. The idea flips who does the work: instead of every cloud provider inventing its own way to trust a token minted by someone else's identity system, the identity provider issues a narrow, single-purpose delegation assertion that any resource, anywhere, can verify on its own terms, no shared tenant required.

![ID-JAG delegation flow](/id-jag-flow.svg)

What got me genuinely excited is that the delegation token can be locked down to one specific piece of software, not just one company or one app registration. Every workload in the platforms I build already carries a SPIFFE identity, something like `spiffe://corp.ai/agents/awesome-agent-1`, and ID-JAG lets me mint a token that's only valid for that exact identity. Not "any assistant at this company." Not even "this app." One specific running instance of one specific agent.

Roughly what minting one of those looks like:

```python
import jwt
import time

AGENT_SPIFFE_ID = "spiffe://corp.ai/agents/awesome-agent-1"

claims = {
    "iss": "https://idp.corp.ai",           # who issued this
    "sub": "user:feisal@corp.ai",           # who the action is on behalf of
    "act": {"sub": AGENT_SPIFFE_ID},        # which exact agent is acting
    "aud": "https://expenses.corp.ai/api",  # the one resource this is good for
    "iat": int(time.time()),
    "exp": int(time.time()) + 60,           # good for one minute, not one session
}

id_jag = jwt.encode(claims, idp_signing_key, algorithm="ES256")
```

If that token leaks, or an attacker compromises a completely different agent running in the same cluster, it doesn't matter. The token only means something coming from `awesome-agent-1`, calling the expenses API, in the next sixty seconds. That's a much smaller blast radius than "a valid credential for this company," and it's the first identity model I've seen that treats an individual agent as something worth naming and constraining, rather than lumping every piece of automation into one generic service account.

## Where this leaves us

Entra's Agent ID solves this well inside Microsoft's own walls. Okta is further along on the open, cross-boundary version of the same idea, and Entra doesn't implement ID-JAG itself yet, so this is still a bet on where things are heading rather than something you can lean on for the AWS side of that expense report today. But it's the first spec I've read that asks the right question: not "how do we bolt human login onto a bot," but "how do we say, precisely, which piece of software is allowed to act, for how long, and on whose behalf."

Answering it cleanly is most of the hard part of building an agent platform. Everything after it, the orchestration, the multi-step workflows, the systems talking to each other, gets easier to trust once that answer is in place.

[^1]: [Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/agent-identities)
[^2]: [IETF ID-JAG draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-identity-assertion-authz-grant)
[^3]: [XAA](https://xaa.dev/)
