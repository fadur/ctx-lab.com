---
title: "Everything Has Changed, and Yet Everything Is the Same"
date: 2026-07-07
author: "Feisal Adur"
description: "Ontology and semantic layers are back because LLMs finally consume the meaning people used to write down for machines that never arrived."
draft: true
---

The word "ontology" is suddenly everywhere in enterprise AI. From the outside, Palantir seems to have built its whole platform around one.[^1] Databricks shipped its version this year,[^2] and the word "semantic" now shows up on all slides.

I haven't used either platform. I've only read about them. This is an outsider's read of the pitch.

An **ontology** is a written map of what things are and how they connect. A **semantic layer** is a written definition of what the numbers mean.[^3]

The idea is old. What changed is that something can finally read it. What stayed the same is the hard part: nobody can sell you the meaning of your business. You still have to write that down yourself.

## This was built twenty years ago

In the 2000s this was called the semantic web.[^4] Formal ways to write down what data means, so machines could read it. There were real standards, working tools, and an entire research field behind it. Cory Doctorow's old essay "Metacrap" is still one of the best short explanations of why this kind of work so often runs aground in practice.[^5]

Commercially it went nowhere, and the reason was economics rather than any flaw in the idea. Writing everything down was expensive. You paid experts to spend months modeling the business, and the payoff was a query tool that three people in the company knew how to use. Nothing useful ever consumed all that carefully encoded meaning, so nobody could justify producing it.

## What changed

An LLM consumes it.

Consider what actually happens today when someone asks for revenue by segment. The question goes to an analyst because the analyst carries the context. They know which tables matter, what revenue means in this company, and which column finance actually trusts versus which one is a leftover from an old migration. Their job, for this question, is translating it into a query, and their scarcity is why the question sits in a backlog for two weeks.

Write that context down and you can hand the translation step to an agent. It reads the definitions, builds the query the analyst would have built, and puts the result in front of the person who asked. The knowledge is the same. The difference is that something can finally read it and do useful work with it.

In 2008, writing down meaning was a cost with no consumer. Now it's what turns a backlog of questions into things that get answered on demand.

People hear this and think source of truth: define the metric once, bless it, and make engineers implement it. But that is not where the hard part is. The hard part starts when the definition begins cascading through real systems. A metric becomes a query, a query feeds a dashboard, the dashboard drives a pipeline, and then the edge cases show up. That is where you find out whether the definition was real or just tidy.[^6]

## Agents don't need your data

To answer a question, the agent needs the map, and only the map. It reads the definitions, writes a query, and the query executes where your queries already execute, under the access controls you already have. The model consumes metadata. The rows stay where they are.

![The model reads the map, not the data](/images/ontology-two-planes.svg)

This starts eating into a category of software I've spent a lot of time building. A lot of internal tooling is just a pre-compiled answer to a question someone expected to be asked often enough: a dashboard, a report page, an internal tool with three filters and an export button, an endpoint that exists because a team asked the same question twice.

I've written a lot of that software. A lot of ETL pipelines too. Someone takes business meaning that lives in a person's head, hard-codes it into a pipeline or a view, then keeps paying to maintain it every time the schema shifts or the business changes its mind about what a number means.

If the meaning is written down in a form an agent can read, a lot of that starts to look less like durable software and more like a cached answer. The query can be built on demand. The view can be assembled when the question is asked. The expensive part is still deciding, precisely, what things mean.

![Stop pre-compiling answers](/images/ontology-precompiled.svg)

I don't think you can really buy this as a product. You can buy software that helps you manage the map. You can buy a better interface over it. The map is still yours, and the hard part is still writing it down.

## What's the same

I've spent a lot of time in rooms where the real argument was not about observability, but about meaning. What does it mean when someone says *the system is slow*? Which latency counts? When does it become a problem? Half the work is not collecting data. It's forcing a shared definition into a form a machine can act on.

The map finally has a reader. The thing semantic web people wanted machines to do twenty years ago is now genuinely useful.

The work is still the work. Someone still has to decide what it means for *the system to be slow*, what *revenue* means, what counts, what doesn't, and where the edge cases live. The software got better. The argument didn't go away.

That's the next post: what a decade of arguing about the definition of "slow" has to do with ontology.

[^1]: [Palantir Foundry ontology overview](https://www.palantir.com/docs/foundry/ontology/overview)
[^2]: [Databricks: Redefining semantics with a data layer for the future of BI and AI](https://www.databricks.com/blog/redefining-semantics-data-layer-future-bi-and-ai)
[^3]: [Databricks metric views](https://docs.databricks.com/aws/en/business-semantics/metric-views)
[^4]: [The Semantic Web and the Semantic Web](https://twobithistory.org/2018/05/27/semantic-web.html)
[^5]: [Metacrap: Putting the torch to seven straw-men of the meta-utopia](https://people.well.com/user/doctorow/metacrap.htm)
[^6]: [James C. Scott, *Seeing Like a State*](https://en.wikipedia.org/wiki/Seeing_Like_a_State#Summary)
