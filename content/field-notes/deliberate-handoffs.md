---
title: "Deliberate Handoffs"
date: 2026-07-05
author: "Feisal Adur"
description: "The industry is obsessed with loop engineering. I don't write loops. I do handoffs. When I build agentic systems for users, the handoff is the product."
draft: false
---

Soon, most people won't write code by hand. That's not the loss it sounds like.

Programming was never really about the code. They're called *programming languages* for a reason: the word was always language, not syntax. What the job actually required was the ability to take a fuzzy idea and articulate it precisely enough that a machine could follow it. The code was just the notation. The compiler was always the translator. It required a very particular kind of precision, one that only a formal language could satisfy, and so programmers spent decades learning to write in one.

That constraint is loosening. The translator now understands English well enough that the formal notation is increasingly optional. Paul Graham wrote last year that the world is splitting into writes and write-nots[^1]: people who can think clearly enough to write, and people who'll outsource that and quietly stop being able to do it at all. His point is that writing is thinking, and you can't outsource the thinking without losing the capacity. The same split is coming for programming. Not coders and non-coders. People who can articulate what they want a system to do, precisely, completely, in terms a machine can act on, and people who can't.

The handoff file is where I find out which one I am.

The current industry obsession is loop engineering. Boris Cherny, head of Claude Code at Anthropic, put it plainly: "I don't prompt Claude anymore. I have loops running that prompt Claude and figure out what to do. My job is to write loops." Peter Steinberger says the same: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

I understand the appeal. A loop finds the work, hands it to an agent, checks the output, and decides what's next without you in the middle. You design it once and it runs while you sleep. The pieces are all there now: automations, worktrees, sub-agents, memory files. The tools ship it out of the box.

I don't write loops. I do handoffs.

Not because loops are wrong. Addy Osmani, who wrote the most thorough breakdown of loop engineering I've read[^2], names the risk himself: two people can build the exact same loop and get opposite results. One moves faster on work they understand deeply. The other uses the loop to avoid understanding the work at all. The loop doesn't know the difference.

The handoff file is how I keep that from happening.

I never let a coding agent compact its own session. After every unit of work, I write a handoff file, start a new session, and tell the agent to get up to speed from it.

```
.claude/handoffs/2026-07-03-cnpg-pdb-fix.md

## What's done
Fixed the replica PDB vacuous-satisfaction bug during CNPG switchover.
Root cause: PDB minAvailable counted the old primary as still available
for one reconcile loop after the switchover started.

## What's next
Verify the fix holds under a forced failover in staging. Not yet tested
against the dual NodePool topology.

## Constraints that still apply
Stateful pool must never be touched by aggressive consolidation.
```

That's slower than letting the harness auto-compact and keep going. It's also the whole point. Compaction is the harness deciding what's worth keeping. A handoff file is me deciding. I own the session boundary, not the agent and not the harness.

![Session A does the work, hands off a file, Session B starts cold with only that file](/handoff-boundary.svg)

Session B doesn't inherit Session A's context. It inherits exactly what's in the file, nothing more. If something mattered and I didn't write it down, it's gone. It forces me to decide what actually matters instead of trusting a summarizer to guess.

## Building systems that are loops

When I build agentic systems for users, the dynamic inverts. I am designing the loop. The agent does a unit of work, researches, drafts, analyses, executes, and at some point it has to hand something back. Not to a fresh context window, but to a person.

That handoff is the product. Not the output the agent produced, but the moment where a human can see what happened, decide if it's right, and choose what comes next. Get that boundary wrong and you have a system that either asks for permission too often to be useful, or one that runs so far ahead the user stops trusting it.

What a clean handoff looks like at the boundary matters more than how autonomous the agent should be. What does the user need to see to make a real decision? What does accept mean, what does reject mean, and what does steer mean? Are those three things actually distinct in your system?

## The same boundary, with a person on the other side

Treat the handoff as an inbox: the agent does a unit of work, reports back, a human accepts, rejects, or steers, and work continues from there.

![Agent reports to an inbox, human accepts, rejects, or steers, agent continues](/inbox-pattern.svg)

It's the same boundary I draw with my own coding sessions, just with a person on the other side instead of a fresh context window. Either way, something has to stop, hand over exactly what matters, and wait for a decision before it's allowed to keep going.

## AG-UI gives the pattern a wire format

This is showing up as a real spec now, not just a habit. AG-UI's interrupt model[^3] treats a pause for a human as a normal terminal state of a run, the same standing as finishing or erroring:

```json
// Run terminates like this, not with an error
{
  "outcome": "interrupt",
  "interruptId": "int_8f2c1a",
  "payload": {
    "type": "approval",
    "message": "Deploy migration 0042 to prod?",
    "context": { "run": "run_5591", "step": "pre-deploy-check" }
  }
}
```

```json
// Resume is a new run, not a continuation of the old one
{
  "resume": [
    { "interruptId": "int_8f2c1a", "value": "approved" }
  ]
}
```

![A run terminates in an interrupt, hands the interruptId to a durable store you own, a human resumes it, and a new run picks up from resume value alone](/agui-lifecycle.svg)

No stack survives across that boundary. The next run has to reconstruct "why was I asking this" from state plus the resume value alone, the same way Session B reconstructs "what was Session A doing" from the handoff file alone.

| | Compaction | Handoff (mine / AG-UI) |
|---|---|---|
| Who decides what survives | The harness | The person or the protocol design |
| What crosses the boundary | Summarized context, implicit | Explicit file or payload, nothing else |
| Failure mode | Silently drops something that mattered | Loud: if it's not written down, it's just gone |
| Resume model | Same session, continued | New session or new run, cold start |
| Where state lives | Wherever the harness keeps it | Wherever you decide to put it |

The model and the API are stateless. The spec gives you the envelope, the shape of the ask and the shape of the answer. It does not give you a durable store, a way to correlate a resume to the right paused run three weeks later, or a way to handle two resumes racing. Whoever runs the system owns all of that, same as I own the folder my handoff files live in.

[^1]: [Writes and Write-Nots](https://www.paulgraham.com/writes.html), Paul Graham
[^2]: [Loop Engineering](https://addyosmani.com/blog/loop-engineering/), Addy Osmani
[^3]: [AG-UI Interrupts](https://docs.ag-ui.com/concepts/interrupts)
