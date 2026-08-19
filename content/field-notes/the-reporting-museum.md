---
title: "The Reporting Museum"
date: 2026-08-19
author: "Feisal Adur"
description: "Modern data infrastructure is very good at describing a business. The useful part begins when observation, objective, decision, and action form a loop."
series: "Ontology"
series_part: 2
draft: false
---

There's a running joke that the modern data stack is a very expensive staging environment for a PowerPoint slide. A state-of-the-art lakehouse on one side, Palantir on the other, and at the end an executive spends ten minutes with the deck and decides what to do.

I like to think of it as a reporting museum. The numbers are carefully collected, labelled, and put on display. People come by, look at what changed, and carry on. The business has been observed. Whether the observation changes anything is somebody else's problem. Am exaggarating of course. But maybe not by much.

Ok, hear me out. That arrangement made sense when the dashboard ended up in front of a person. In [the last post](/field-notes/everything-has-changed-and-yet-everything-is-the-same/), I argued that LLMs finally gave ontology and the semantic layer a reader. I like to think of ontology as a precursor to systems that can adapt, because it shapes a vocabulary your system can reason about. And once you go down that path, a precise description of the world is not enough. You'd want a system that also knows which outcomes matter, what it may change, and how to measure whether the change helped.

I ended that post with a promise to explain what a decade of debating "slow" in observability taught me about ontology.

It usually starts with two clocks. The API returns `202 Accepted` in 120 milliseconds; the customer waits five minutes for confirmation. Both numbers are right. One measures acceptance. The other measures completion.

What I learned is that "slow" has no useful meaning. Period. You have to name the thing, its boundary, and the event that marks completion. Is checkout an HTTP request, a payment authorization, an order record, or the whole journey from pressing the button to seeing confirmation? Telemetry alone cannot answer that. Someone has to decide.

This is where ontology and the semantic layer meet observability.

An order connects to a customer, a payment, and the systems involved in checkout. Did someone say graph engineering?

Ok, fine. Let's use graphs. The graph still does not decide what an order is or when checkout is complete. That is the ontology: the shared understanding of the things in the business and how they relate.

The semantic layer does the same for the numbers. It defines what "checkout latency" measures. Now when someone says checkout is slow, everyone is talking about the same thing.

You can represent an ontology in a graph, and a graph may be the right technology for the job. But choosing a graph database does not give the data a shared meaning any more than choosing a lakehouse does. It gives you somewhere to put the result.

A shared definition settles what was observed. It still leaves the question of what to do.

Take a restaurant during an ordinary Wednesday dinner rush. A waiter might say, "It's busy tonight." That could mean every table is occupied, order tickets are piling up, or plates are waiting at the pass. Each observation describes the same room, but each calls for a different response. I love food analogies, so bear with me.

Suppose you own the restaurant and want to get the right food to each table while it is still hot, without rushing the kitchen into mistakes. Now the observations have a purpose. You could stop accepting Wolt pickup orders for half an hour or ask someone to run food. Then you watch what happens. Did the backlog clear? Did food reach the tables sooner? Did mistakes go up?

Now it becomes a loop. Observe the restaurant, interpret the delay, choose an action within the constraints, and check the result. "Busy" is an observed state. Getting food to the table is what the restaurant is trying to control.[^1] The two are related, but one does not stand in for the other automatically.

The ontology tells you what an observation is about. The objective explains why it matters. The available actions define what can change, and the result tells you whether the reasoning held up. Did someone say loop engineering?

For most of the history of information systems, observation was a natural place to stop. The system collected the data and put it in a dashboard. A person supplied the objective, made the decision, and took the action. The dashboard was the handoff.

The objective often travelled separately from the measurement. A clear business goal was decomposed as it moved through the organization. Departments received objectives, teams received metrics, and metrics began standing in for other metrics. Eventually the organization was tracking a few hundred numbers, and we hoped someone was still holding the whole causal chain in their head.

That's why KPIs always felt weird. By the time a KPI reached the teams expected to move it, the explanation for why it mattered had often disappeared. The number had to go up because everyone signed off on it going up. Teams hit the target and the dashboard went green. Whether the business improved was harder to answer.

That arrangement worked as long as a person could reconstruct enough of the missing argument to make a decision. An agent cannot be handed a metric and expected to know why the number matters. The objective has to travel with the observation, along with the constraints, permitted actions, and evidence that an action worked.

Imagine an agent helping with an incident after a deployment. Customer-facing latency rises, but the service dashboard remains green. The agent can see traces, metrics, the deployment, its dependencies, and the customer journeys they support. A semantic definition tells it what "degraded" means. The objective is to restore the customer journey without losing data or causing a larger outage.

Its allowed actions might include shifting traffic, adding capacity, rolling back the deployment, or paging the responsible team. After acting, it checks the customer journey again. If latency stays high, the result comes back into the next decision. If the safe options are exhausted, it hands the incident to a person.

Ontology gives the agent the map of services, deployments, dependencies, teams, and customer journeys. The semantic layer gives it consistent measurements. Objectives, constraints, available actions, and feedback turn that information into a loop.

An information system that ends at a dashboard supports the business. One that can close the loop becomes part of how the business steers itself.

My claim is that much of what we are rediscovering as agent architecture is old machinery assembled again under new names. The technology changes. The underlying work does not.

Last month it was loop engineering. This month it is graph engineering. Next month somebody will explain "quantum ontology orchestration" on a podcast and the rest of us will have to pretend it was inevitable.

Graphs are useful. Agents need relationships they can traverse. But nodes and edges do not decide what a customer is, when a process is complete, or what "slow" means.

A graph can store the result of a shared understanding. It cannot have the conversation that produces one.

[^1]: In [control theory](https://en.wikipedia.org/wiki/Control_theory), a system observes its state, compares it with a desired state, acts, and uses the result as feedback. The important bit here is that measurement only becomes useful for control once you know what outcome you're trying to produce.
