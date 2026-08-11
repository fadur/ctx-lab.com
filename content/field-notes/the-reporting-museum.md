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

I ended [the last post](/field-notes/everything-has-changed-and-yet-everything-is-the-same/) with a promise to explain what a decade of arguing about "slow" in observability has to do with ontology. Take an order moving through an online retailer. Checkout, payment, inventory allocation, pick, pack, parcel out the door. Model that as an ontology: orders, customers, payments, products, inventory, shipments, warehouses, and the events that move each one from one state to the next. Fine. Now someone says "checkout is slow." On its own that sentence means nothing. It's a vibe. But if the semantic layer has already defined checkout latency as a specific sequence of events, and defined what a P50 or P99 crossing a given threshold means for the customer, "slow" stops being a vibe and starts being a claim you can check.

You can now check whether checkout is slow. You still haven't said why it matters.

Suppose the company chooses order throughput: get more orders from checkout to dispatch each hour. Even that needs guardrails. Faster is no good if fulfillment costs rise or more parcels arrive damaged. So the objective becomes: increase throughput without increasing cost or errors. Another company might choose margin or delivery reliability instead. Choosing is the hard part.

Think about a restaurant during an ordinary Wednesday dinner rush. A waiter says, "It's busy tonight." That could mean every table is occupied, the kitchen has twelve open tickets, or food is waiting under the heat lamp because nobody is available to run it. "Busy" tells you how the room feels. It does not tell the manager what to do.

Suppose the goal is to get the right food to each table while it is still hot. If tickets are piling up, the kitchen may need help. If plates are waiting at the pass, the kitchen is not the problem; someone needs to run food. The same busy restaurant calls for a different action depending on where the delay is.

Now checkout latency has a place in the argument. It is not the objective. It is one signal that may help explain or predict throughput.[^1] If latency rises and completed orders fall, it may be worth acting on. If throughput does not move, latency may just be an interesting number.

The ontology tells you what the measurement is about. The objective tells you why you care. Without that objective, the ontology is an accurate description of the business and nothing more.

In many non-software companies, this is where IT stops. It collects the observations and puts them in dashboards, reports, and quarterly decks. The decision belongs to someone else, and the action to someone else again. That division is not necessarily a mistake. It is simply how the organization was built. The dashboard is the handoff between the people who maintain the information systems and the people who run the business.

It's also why KPIs get weird. "Make orders move through the warehouse faster" is a sentence a founder can say and mean. Past a certain size it has to be decomposed: departments get objectives, teams get metrics, metrics start standing in for other metrics, and eventually the organization is tracking a few hundred numbers, and we hope someone is still holding the whole causal chain in their head. That's how a KPI turns into a number that has to go up because everyone signed off on it going up. By the time it reaches the teams expected to move it, the explanation for why it matters has often disappeared. The stand-in quietly replaced the thing it was standing in for. Teams hit the target. The dashboard goes green. The business? Meh, who knows.

More measurement doesn't fix this. What fixes it is not losing the argument for why moving this particular number is supposed to help.

Lay the pieces end to end and you get something closer to a loop than a report. State of the world, observed through events and measurements. Ontology says what those observations are about. Semantic layer makes their meaning consistent. Objective says what's being optimized, and under what constraints. A decision gets made. The world changes. You observe the result and run it again. Treat the information system as the thing that makes that loop possible, not as the thing that produces artifacts to be read and set down.

This is where agents stop being a curiosity and start being useful. Handing an agent a warehouse and a good semantic layer isn't enough by itself, the same way handing an intern a data warehouse isn't enough. The agent can know an order exists, belongs to a customer, has been sitting in a fulfillment queue for 47 minutes, and that 47 minutes is unusual. None of that tells it what to do about it. It needs an objective, reduce fulfillment time under a cost constraint, say, before "unusual" turns into an action. Give it that, and it can observe, interpret, decide, act, and check whether the action actually moved the number it was supposed to move. That's the point where the ontology and the semantic layer stop feeding dashboards and start feeding a loop that runs without someone staring at it for ten minutes first.

Stick around a non-software company long enough and eventually someone will say, entirely unironically, that IT is a support function, a cost of doing business in the same broad category as keeping the lights on and making sure the printers work.

Honestly, that's a reasonable conclusion if IT appears to be running the reporting museum. If nobody's bothered to define what the data refers to or what it means, an information system can only ever collect things, move them around, and occasionally set a dashboard in front of someone who makes the actual decision. Under those conditions IT is a support function, and an expensive one at that.

But once there's an ontology to say what the data is about, a semantic layer to say what it means, and an objective to say what's being optimized, the same system stops merely reporting and starts closing a loop: observe, decide, act, check whether it worked. At that point it isn't supporting the business. It's the thing the business steers itself with.

The guy calling IT a cost center is often the same guy who, a few years later, signs a large contract with Palantir to buy his way out of the fog. Some of that money is buying real engineering. But a good part of it is buying something that was never for sale in the first place: a correct description of his own business. Ontology isn't a product you procure. It's the outcome of understanding yourself well enough to say precisely what your orders, customers, and warehouses are and how they relate, and no vendor can do that understanding for you.

Still, I'm sure the deck will be ready by Thursday.

[^1]: In [control theory](https://en.wikipedia.org/wiki/Control_theory), the observed variable is what you measure; the controlled variable is what you're trying to change. Confusing the two is where things go wrong.
