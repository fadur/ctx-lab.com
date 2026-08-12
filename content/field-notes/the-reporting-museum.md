---
title: "The Reporting Museum"
date: 2026-08-11
author: "Feisal Adur"
description: "Modern data infrastructure is very good at describing a business. The useful part begins when observation, objective, decision, and action form a loop."
series: "Ontology"
series_part: 2
draft: true
---

There's a running joke that the modern data stack is a very expensive staging environment for a PowerPoint slide. A state-of-the-art lakehouse on one side, Palantir on the other, and at the end an executive spends ten minutes with the deck and decides what to do.

I think of the rest as a reporting museum. The numbers are carefully collected, labelled, and put on display. People come by, look at what changed, and carry on. The business has been observed. Whether the observation changes anything is somebody else's problem.

That arrangement made sense when a person was always waiting at the end. In [the last post](/field-notes/everything-has-changed-and-yet-everything-is-the-same/), I argued that LLMs finally gave the ontology and semantic layer a reader. Agents take the next step: the reader can act. Once that happens, a precise description of the world is not enough. The system also needs to know which outcome matters, what it may change, and how to tell whether the change helped.

I ended that post with a promise to explain what a decade of arguing about "slow" in observability has to do with ontology.

The argument usually starts with two teams looking at different clocks. The API team says checkout takes 120 milliseconds. The product team says it takes four seconds. Support has customers waiting longer than either. Nobody has necessarily measured badly. The API clock starts when the request reaches the service and stops when the response leaves. The customer's clock starts when they press the button and stops when they know the order went through.

Queues make this worse. A worker may process an order in 80 milliseconds once it picks it up, while the order spends seven minutes waiting. An asynchronous API can return `202 Accepted` almost immediately and still leave the customer waiting five minutes for confirmation. The dashboard says the request was fast because it measured acceptance. The customer was waiting for completion.

Percentiles produce another version of the argument. The median can stay flat while a smaller group of customers gets a much worse experience. If those customers share a region, payment method, or account shape, the slow one percent is not random noise. It is a specific part of the business having a reliably bad time.

What I learned from these arguments is that "slow" has no useful meaning until you name the thing, its boundary, and the event that marks completion. Is checkout an HTTP request, a payment authorization, an order record, or the whole journey from pressing the button to seeing confirmation? The telemetry cannot answer that. Someone has to decide.

This is where ontology and the semantic layer meet observability. The ontology identifies the order, payment, customer, service, and events involved. The semantic layer defines which interval "checkout latency" refers to. Only then does "checkout is slow" become a claim two teams can test against the same definition.

A shared definition settles what was observed. It still leaves the question of what to do.

Take a restaurant during an ordinary Wednesday dinner rush. A waiter says, "It's busy tonight." That could mean every table is occupied, tickets are piling up, or plates are waiting at the pass. Each observation describes the same room, but each calls for a different response.

Suppose the restaurant wants to get the right food to each table while it is still hot, without rushing the kitchen into mistakes. Now the observations have a purpose. The manager can slow down seating, move someone onto the line, or ask someone to run food. Then they watch what happens. Did the backlog clear? Did food reach the tables sooner? Did mistakes go up?

That is the loop: observe the restaurant, interpret the delay, choose an action within the constraints, and check the result. "Busy" is an observed variable. Getting food to the table is what the restaurant is trying to control.[^1] The two are related, but one does not stand in for the other automatically.

The ontology tells you what an observation is about. The objective explains why it matters. The available actions define what can change, and the result tells you whether the reasoning held up.

For most of the history of information systems, observation was a natural place to stop. The system collected the data and put it in a dashboard. A person supplied the objective, made the decision, and took the action. The dashboard was the handoff.

The objective often travelled separately from the measurement. A clear business goal was decomposed as it moved through the organization. Departments received objectives, teams received metrics, and metrics began standing in for other metrics. Eventually the organization was tracking a few hundred numbers, and we hoped someone was still holding the whole causal chain in their head.

By the time a KPI reached the teams expected to move it, the explanation for why it mattered had often disappeared. The number had to go up because everyone signed off on it going up. Teams hit the target and the dashboard went green. Whether the business improved was harder to answer.

That arrangement worked as long as a person could reconstruct enough of the missing argument to make a decision. An agent cannot be handed a metric and expected to know why the number matters. The objective has to travel with the observation, along with the constraints, permitted actions, and evidence that an action worked.

Imagine an agent helping with an incident after a deployment. Customer-facing latency rises, but the service dashboard remains green. The agent can see traces, metrics, the deployment, its dependencies, and the customer journeys they support. A semantic definition tells it what "degraded" means. The objective is to restore the customer journey without losing data or causing a larger outage.

Its allowed actions might include shifting traffic, adding capacity, rolling back the deployment, or paging the responsible team. After acting, it checks the customer journey again. If latency stays high, the result comes back into the next decision. If the safe options are exhausted, it hands the incident to a person.

Ontology gives the agent the map of services, deployments, dependencies, teams, and customer journeys. The semantic layer gives it consistent measurements. Objectives, constraints, available actions, and feedback turn that information into a loop.

Treat the information system as the thing that makes this loop possible, rather than the thing that produces an artifact to be read and set down.

Spend enough time in the IT department of a non-software company and you'll eventually hear that IT is a support function, a cost of doing business alongside keeping the lights on and the printers working.

Honestly, that's a reasonable conclusion if IT appears to be running the reporting museum. When an information system collects data, moves it around, and sets a dashboard in front of the person making the decision, it is supporting the business. It may be very expensive support, but the description is fair.

Connect the observations to an objective, the objective to a decision, and the decision to an action whose result comes back into the system, and its role changes. It becomes part of how the business steers itself.

An organization can spend years treating IT as a cost center, then sign a large contract with Palantir to connect its reports back to the business. Some of that money buys real engineering. A good part of it buys software for managing a description of the business.

The software can be procured. The description still has to come from people who understand the business well enough to say what its customers, processes, and systems are, how they relate, and which outcomes matter. No vendor can do that understanding for you.

[^1]: In [control theory](https://en.wikipedia.org/wiki/Control_theory), the observed variable is what you measure; the controlled variable is what you're trying to change. Confusing the two is where things go wrong.
