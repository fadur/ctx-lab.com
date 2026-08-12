---
title: "The Reporting Museum"
date: 2026-08-11
author: "Feisal Adur"
description: "Modern data infrastructure is very good at describing a business. The useful part begins when observation, objective, decision, and action form a loop."
series: "Ontology"
series_part: 2
draft: true
---

There's a running joke that the modern data stack is a very expensive staging environment for a PowerPoint slide. Databricks on one side, Palantir on the other, and at the end an executive spends ten minutes with the deck and decides what to do.

I think of the rest as a reporting museum. Dashboards, KPI scorecards, quarterly forecasts, the data mart whose owner left two reorganizations ago. Everyone walks through, pauses at conversion or fulfillment time, says "interesting," and carries on. The business has been observed. Whether the observation changes anything is somebody else's problem.

I ended [the last post](/field-notes/everything-has-changed-and-yet-everything-is-the-same/) with a promise to explain what a decade of arguing about "slow" in observability has to do with ontology.

The argument usually starts with two teams looking at different clocks. The API team says checkout takes 120 milliseconds. The product team says it takes four seconds. Support has customers waiting longer than either. Nobody has necessarily measured badly. The API clock starts when the request reaches the service and stops when the response leaves. The customer's clock starts when they press the button and stops when they know the order went through.

Queues make this worse. A worker may process an order in 80 milliseconds once it picks it up, while the order spends seven minutes waiting. An asynchronous API can return `202 Accepted` almost immediately and still leave the customer waiting five minutes for confirmation. The dashboard says the request was fast because it measured acceptance. The customer was waiting for completion.

Percentiles produce another version of the argument. The median can stay flat while a smaller group of customers gets a much worse experience. If those customers share a region, payment method, or account shape, the slow one percent is not random noise. It is a specific part of the business having a reliably bad time.

What I learned from these arguments is that "slow" has no useful meaning until you name the thing, its boundary, and the event that marks completion. Is checkout an HTTP request, a payment authorization, an order record, or the whole journey from pressing the button to seeing confirmation? The telemetry cannot answer that. Someone has to decide.

This is where ontology and the semantic layer meet observability. The ontology identifies the order, payment, customer, service, and events involved. The semantic layer defines which interval "checkout latency" refers to. Only then does "checkout is slow" become a claim two teams can test against the same definition.

A shared definition settles what was observed. It still does not tell you whether the observation is worth acting on.

Suppose the company chooses order throughput: get more orders from checkout to dispatch each hour. Faster is no good if fulfillment costs rise or more parcels arrive damaged, so the objective needs guardrails. Another company might choose margin or delivery reliability instead. Deciding among those goals and their trade-offs is the hard part.

Checkout latency is one signal that may help explain or predict throughput.[^1] If latency rises while completed orders fall, it may be worth acting on. If throughput stays put, latency may just be an interesting number.

The ontology tells you what the measurement is about. The objective tells you why you care. Without that objective, the ontology is an accurate description of the business and nothing more.

In many non-software companies, this is where IT stops. It collects the observations and puts them in dashboards, reports, and quarterly decks. The decision belongs to someone else, and the action to someone else again. That division reflects how the organization was built: the dashboard is the handoff between the people who maintain the information systems and the people with the authority to act.

It's also why KPIs get weird. "Make orders move through the warehouse faster" is a sentence a founder can say and mean. Past a certain size it has to be decomposed. Departments get objectives, teams get metrics, metrics start standing in for other metrics, and eventually the organization is tracking a few hundred numbers. We hope someone is still holding the whole causal chain in their head.

That's how a KPI turns into a number that has to go up because everyone signed off on it going up. By the time it reaches the teams expected to move it, the explanation for why it matters has often disappeared. The stand-in quietly replaces the thing it was standing in for. Teams hit the target and the dashboard goes green. Whether the business improved is harder to answer.

More measurement doesn't fix this. The argument for why moving a particular number should help has to survive alongside the number.

Lay the pieces end to end and you get a loop. An order has been waiting for 47 minutes. The ontology tells us which order, customer, warehouse, and shipment are involved. The semantic layer tells us that 47 minutes is unusual. The objective tells us whether the delay matters and which trade-offs are acceptable. A decision follows: reprioritize the order, add capacity, or leave it alone. Then the system measures what happened.

That last step matters. If the action did not improve throughput, you have learned something about the relationship between the signal and the objective. The loop ends when the result comes back, not when someone acts.

Treat the information system as the thing that makes this loop possible, rather than the thing that produces an artifact to be read and set down.

Agents make this more than an organizational diagram. A dashboard can leave the objective implicit because a person may supply it from experience. An agent needs the objective spelled out, along with the constraints it must respect and the actions it is allowed to take.

For the delayed order, that might mean reprioritizing the queue while keeping fulfillment cost and error rates within bounds. The agent acts, observes the result, and either continues or hands the decision back to a person. Ontology gives it the map. The semantic layer gives it consistent measurements. The objective, constraints, and available actions give it a basis for doing something.

Stick around a non-software company long enough and eventually someone will say, entirely unironically, that IT is a support function, a cost of doing business in the same broad category as keeping the lights on and making sure the printers work.

Honestly, that's a reasonable conclusion if IT appears to be running the reporting museum. When an information system collects data, moves it around, and sets a dashboard in front of the person making the decision, it is supporting the business. It may be very expensive support, but the description is fair.

Connect the observations to an objective, the objective to a decision, and the decision to an action whose result comes back into the system, and its role changes. It becomes part of how the business steers itself.

The guy calling IT a cost center is often the same guy who, a few years later, signs a large contract with Palantir to connect the reports back to the business. Some of that money buys real engineering. A good part of it buys software for managing a description of the business.

The software can be procured. The description still has to come from people who understand the business well enough to say precisely what its orders, customers, and warehouses are, how they relate, and which outcomes matter. No vendor can do that understanding for you.

[^1]: In [control theory](https://en.wikipedia.org/wiki/Control_theory), the observed variable is what you measure; the controlled variable is what you're trying to change. Confusing the two is where things go wrong.
