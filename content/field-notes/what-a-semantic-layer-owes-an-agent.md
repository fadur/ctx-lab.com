---
title: "What a Semantic Layer Owes an Agent"
date: 2026-08-26
author: "Feisal Adur"
description: "A semantic layer for agents should make shared organizational decisions callable, consistent, and capable of returning undefined."
draft: true
---

I've been trying to get clearer on what a semantic layer should mean when the consumer is an agent.

A lot of my recent work has been about helping the people who understand a process give agents the context and knowledge they need, without waiting for every rule to be encoded in software.

I believe in that approach. The more I work this way, though, the more one problem keeps showing up.

Take something as simple as a travel policy that says meals are reimbursable up to a reasonable amount, adjusted for high-cost cities.

A domain expert puts that in an agent's instructions. Another team does the same. If all goes well, maybe we end up with one central chatbot and several skills, sub-agents, or MCP servers behind it. Or maybe there are twenty agents built by different parts of the organisation. If we're really good, they all pull the same policy into context.

Eventually somebody asks:

> I spent $92.33 on dinner in Tokyo last night. How do I get reimbursed?

One path through the system says the meal is reimbursable up to $75. Another caps it at $82. A third decides that "reasonable amount" means manager approval is required.

Each answer can be locally defensible. Nobody notices, because why would they? They all sound reasonable on their own. It's not like the agents compare notes. The policy required interpretation, and that interpretation happened wherever the instructions were written.

I kept coming back to what I would rather have instead. The nearest analogy is a DSPy signature,[^1] but only in the shape of the interface: give the question declared inputs and outputs rather than leaving every caller to shape the answer for itself. The resolver is not asking a model to interpret the policy again.

```text
resolve("meal_reimbursement_limit", city="Tokyo", date="2026-08-24")
→ {
    limit: 82,
    currency: "USD",
    basis: "high-cost-city index, Q3 2026",
    source: "T&E policy §4.2"
  }
```

Ask the same question twice and you get the same answer.

There is exactly one place the number can come from, and everyone who asks gets routed to it. Carefulness becomes less important because the architecture carries the consistency.

The more interesting case is where the answer does not exist yet.

```text
resolve("meal_reimbursement_limit", city="Nuuk", date="2026-08-24")
→ {
    status: "undefined",
    reason: "city has no current cost classification",
    source: "T&E policy §4.2"
  }
```

This response may matter more. The system knows the edge of what the organisation has decided. Nuuk has no current classification, so the agent has no number to invent and the missing definition becomes visible.

An answer such as $82 means something because the same system is capable of returning `undefined`.

## The easy cases hide the problem

Travel limits are simple enough that you could reasonably ask why any of this needs infrastructure. Put the number in the instructions and move on. The problem becomes clearer once several ordinary rules interact. Take refunds.

Imagine a policy containing these rules:

- items can be refunded within 30 days if unused
- final-sale items cannot be refunded
- defective items can be refunded even when used
- defective items can also be refunded when marked final sale

Now somebody asks:

> I bought a final-sale item 12 days ago, used it once, and it turned out to be defective. Can I return it?

The answer is yes. The defective-item rule overrides both the unused condition and the final-sale restriction.

That relationship is part of the policy.

You can still put all four statements into Markdown and ask a model to reason over them. It will often get the answer right, and that "often" started bothering me.

The problem grows with the policy. Return windows vary by product class and jurisdiction. Warranty status matters, recalled products introduce exceptions, and a rule added six months later may override one branch of the old policy. Then customer support, ecommerce, and finance each build an agent with its own instructions.

At some point there is a decision hiding inside the prose:

```text
refund_eligibility(
  purchase_age_days=12,
  final_sale=true,
  used=true,
  defective=true
)

→ {
  eligible: true,
  reason: "defective_item_override",
  policy: "returns-policy-v7"
}
```

Once that decision exists, I do not particularly want every invocation of every agent to derive it again.

The agent still has plenty to do: collect the relevant facts, ask whether the item is defective, explain the decision, and probably cite the rule. It might initiate the return afterward. It just doesn't need to rediscover the organisation's refund semantics every time.

## Markdown moved the boundary

Real policies rarely arrive as four tidy rules. They are spread across documents, regional addenda, old decisions, and the judgment of people who know which source wins when they disagree. This is exactly where LLMs are useful: they can work with knowledge before someone has cleaned it up enough to look like software.

This puts the people who understand the process in the middle of the work. They know where the policy is incomplete, which exception is deliberate, and when the written rule no longer matches what happens in practice. I find building tools that make this manageable unusually rewarding. The material is messy and the decisions are hard. Helping people work through that complexity without first becoming software engineers is the point.

Traditional software tended to force some of that ambiguity to become explicit before execution. Someone eventually had to encode a rule as a condition, a lookup, a state transition, a decision table, a type, or plain application code. That work was often tedious, but it produced an artifact where the interpretation could be inspected, tested, versioned and disputed.

LLMs let us postpone that formalization. A paragraph can produce behavior, and frontier models will only get better at interpreting one. But they cannot recover a decision the organisation never made. The uncertainty may be in the model or in the policy. Either way, it travels with the instructions.

If a policy says "reasonable amount," each skill can acquire its own idea of reasonable. If four refund rules interact, each agent can reconstruct their precedence from prose. If the organisation has never resolved a particular edge case, the model can still produce a fluent answer.

Nothing necessarily fails, which is what makes the divergence difficult to see. Each individual result can look reasonable. With enough evals you can catch some of it, and I would certainly rather have the evals. In practice, plenty of these systems are being authored much faster than their evaluation suites are growing.

The underlying issue remains even with good evaluation: the same organisational decision is being reinterpreted in multiple places, and each reinterpretation is somewhere meaning can drift.

## Where the semantic layer clicked for me

This is where semantic modeling and a semantic layer finally separated in my head.

Semantic modeling is the work of deciding what something means: what counts as a high-cost city, which refund rule takes precedence, what `eligible` means, when a policy becomes effective, and which exception overrides which default. The semantic model records those decisions. The semantic layer makes them available to the systems that need them.

In [the last post](/field-notes/the-reporting-museum/) I described the graph as a shared vocabulary for the organisation's concepts and relationships. The resolver is how an agent asks a specific question of that model without loading the whole thing into context.

`refund_eligibility`, its inputs, and a reason like `defective_item_override` belong to the same model. The agent supplies the facts and gets an answer in the organisation's own terms, including `undefined`.

For analytics, the semantic layer has usually meant making metrics, dimensions, entities and relationships consistently queryable. For agents, I think the useful version reaches further into decisions the organisation has already made about how its world works.

The meal policy gets modeled once by the people who own travel policy; the agent asks for the reimbursement limit. The returns team decides how its exceptions compose; the agent asks whether a case is eligible.

This does not require turning the entire organisation into a rules engine. Some knowledge is genuinely fuzzy, some decisions require human judgment, and plenty of agent behavior belongs in natural language. I am interested in the meanings we already expect to be shared. If ten agents can all be asked whether the same receipt is reimbursable, `reimbursable` should mean the same thing in all ten places.

When the organisation has never decided, `undefined` may be one of the most valuable answers the layer can return. It exposes a gap that the policy owner can resolve once, with an effective date and a version, instead of letting each skill acquire its own patch.

The provenance can travel with the answer too:

```text
{
  eligible: true,
  reason: "defective_item_override",
  policy: "returns-policy-v7",
  effective_from: "2026-07-01",
  source: "Returns policy §7.3"
}
```

Now the agent can explain where the answer came from without every skill author separately preserving that chain. This is the semantic layer I have been looking for: shared meaning that every agent can call, including when the answer is `undefined`.

## One problem remains

Making meaning callable creates another problem. A skill can say "call `refund_eligibility`," but that assumes the runtime knows what the capability is and how to reach it. The context remains portable; the capability may not be.

In the next post, I'll share how I think agents can bind to these capabilities across distributed runtimes without coupling themselves too tightly. Dependencies travel about as well as I do: technically, but not without complaints.

[^1]: [DSPy signatures](https://dspy.ai/learn/programming/signatures/) declare the inputs and outputs of a language-model operation. The comparison here is to that declarative contract, not to using an LM to resolve the policy.
