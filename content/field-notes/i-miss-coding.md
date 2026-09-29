---
title: "I Miss Coding"
date: 2026-09-27
author: "Feisal Adur"
description: "I write less code by hand, ship more software, and spend much more time deciding what I am willing to own."
draft: false
---

I miss coding.

I am also shipping more than ever. I build things I would not have had the time or patience to build before. I can try an idea, throw it away, and try another before becoming invested in either. It is genuinely a great time to be alive.

And yet I have this persistent feeling that I am five or six agent sessions away from breaking everything.

Not because the code is obviously bad. The tests pass, it compiles, and every change makes sense on its own. But I can start new sessions faster than I can properly absorb the changes from the last one. It makes me anxious that I might end up maintaining code the model wrote but I never properly understood, while still being accountable for what it does.

Writing code was part of how I learned what I was building. An awkward call site told me when an interface was wrong. A parameter passing through four layers usually meant something lived in the wrong place. Writing it myself did not guarantee good design, but I encountered those problems while the design was still forming.

I am not going back. The industry seems rather more divided about where we have ended up.

[“I have unlimited tokens” is a wild flex](https://github.com/omacom/ttfx/pull/35#issuecomment-5846803103), and I am happy for him.

Then there are people for whom [making a living by pressing Enter](https://x.com/v0xium/status/2101526107128529120?s=20) sounds incredibly depressing.

I understand both reactions.

What follows are a few notes on how I work now, and what I am still trying to get right.

## My contract with the agent

My arrangement with coding agents is that I own the interfaces and the agent deals with much of the implementation.

I decide what goes in, what comes out, which failures the caller sees, and what the interface promises to keep stable. Once other code depends on that shape, changing it gets expensive. I care much less about exactly how a local loop is written, provided it is clear, tested, and stays behind the interface.

This works well enough that I do not automatically reach for the latest frontier model. Everyone who uses these models for serious work knows that coding models peaked at Opus 4.6.[^opus] Later models are more inclined to push back or relitigate a decision I have already made. I suspect some of this comes from training against sycophancy. Fair enough, but contrarianism is just as annoying when I am trying to get something done a particular way.

It is also why I worry when people say they have surrendered and no longer look at the code. Stop checking and the model's preferences become the design.

The contract is easy to state and difficult to specify. “Make the code modular” is nearly useless. The agent may produce a hundred small modules, each exposing almost as much complexity as it contains. Following one operation means opening nine files.

I usually want deep modules: a small interface hiding a useful amount of functionality.[^deep-modules] Callers should not need to know how the work is arranged inside, and changing it should not require a tour of the repository.

Of course, a clean interface can hide a giant loop and 300 conditional statements. It works. I still do not want to touch it. “Implementation detail” cannot mean “code I never need to understand.”

This is not about taste, or me being picky, or believing I am smarter than the model. These are simply the heuristics I use for code I do not mind maintaining.

My editor is still always open, but I spend more time in Lazygit reviewing changes than writing code. This is after sixteen years of configuring Neovim to become an IDE.

Reviewing everything carefully is the obvious answer. But I do not want to review generated code full time. The day becomes a queue of small decisions: keep this abstraction, reject that dependency, ask for another test, collapse these modules, split this function, check whether the library call exists, work out whether the agent quietly widened the task.

No single decision is especially hard. The accumulation is exhausting.

## Where I slow down

I use a small review skill in Python projects, and recently wrote a repository-local Go version for `sbox`. Neither tells me whether code is good. They tell me where to stop and read.

The first check is CRAP1, short for Change Risk Anti-Patterns.[^crap] It combines cyclomatic complexity with test coverage. Branchy code with weak tests rises to the top.

![CRAP1 formula](/images/crap1-explained.svg)

Cyclomatic complexity starts at one and increases with each route through a function:

![A function with two decisions has cyclomatic complexity three](/images/cyclomatic-complexity-example.svg)

The formula is crude, especially when line coverage stands in for path coverage. I am not interested in the score as a grade. I want to know which function is most likely to ruin my afternoon when it changes.

My first Python version treated missing coverage as zero and called the score an upper bound. The Go version reports coverage as `unknown` and refuses to calculate CRAP1. A tool looking for false confidence should avoid manufacturing some of its own.

The second check comes from Rich Hickey's use of *complecting*: braiding things together.[^simple-made-easy] This is not the same as counting branches. A function can be easy to follow and still mix policy, mutation, network calls, and persistence so that they become difficult to change separately. Code with several branches may still do one coherent job.

The `sbox` tool looks for control logic crossing multiple effect boundaries, and for functions that mutate external state while returning a value. An installer is supposed to coordinate processes and output. A finding is a reason to look at what else it has picked up along the way.

The third check borrows a few suspicions from Rob Pike: distrust clever algorithms before measuring, remember that `n` is often small, use the standard library when it already does the job, and look at the data before reaching for a more elaborate algorithm.[^pike]

These checks are deliberately imperfect. A nested loop may be right. Six parameters may really be six independent values. The tool reports its confidence and the evidence it used, then leaves me to read the code.

The comment at the top of the Go implementation says it “emits evidence rather than pretending heuristic findings are facts.” On its last run without coverage, it inspected 44 functions and pointed at three. That is useful. I can read three functions.

It does not catch a hallucinated API, prove security, or tell me whether the feature should exist. It runs after the ordinary correctness checks, when I am deciding whether I am prepared to live with the implementation.

## The approval layer

The obvious next move is another agent. One writes the code, another inspects the architecture, a third checks the tests, and perhaps a chief of staff coordinates them. Before long you have a very impressive graph of agents reviewing agents. I don't know how to make it stop. Please send help.

And yet, some things matter more than my whimsical ideas about good code, or how I feel about stacking one agentic loop on top of another. For security and compliance, I built harnesses around agents that other people could rely on, rather than tools for my own laptop. They give an agent a sandbox, the context for a narrow task, constrain what it can do, check what it produces, and route specific decisions to the people responsible for them.

I did not set out to build more process around the agent. These were simply places where being five sessions away was not an acceptable failure mode. Worse would be relying on the model to care about compliance at all, or only when prompted. I might write about those harnesses in a future post.

I do not miss coding in the literal sense. I miss the confidence that I understand why the code looks the way it does. That is harder to hold onto when the implementation arrives all at once.

[^opus]: I have no benchmark or science to support this. It is just my humble, extensively field-tested opinion.

[^deep-modules]: John Ousterhout develops the distinction between deep and shallow modules in [*A Philosophy of Software Design*](https://web.stanford.edu/~ouster/cgi-bin/book.php).

[^crap]: Alberto Savoia and Bob Evans introduced the CRAP metric as a way to combine complexity and test coverage into an estimate of change risk. See [“This Code is CRAP”](https://testing.googleblog.com/2011/02/this-code-is-crap.html). The implementation discussed here uses line or statement coverage as a proxy rather than true basis-path coverage.

[^simple-made-easy]: Rich Hickey, [“Simple Made Easy”](https://www.infoq.com/presentations/Simple-Made-Easy/), Strange Loop 2011.

[^pike]: Rob Pike's [“Notes on Programming in C”](https://www.lysator.liu.se/c/pikestyle.html) includes the five rules often summarised as measuring before tuning, keeping algorithms simple, and paying close attention to data structures.
