---
title: "English and the Interpreter"
date: 2026-10-21T00:00:00+02:00
author: "Feisal Adur"
description: "English leaves room for interpretation. Now the listener can build software from what we leave unsaid."
image: "/images/programming-glossary.png"
draft: false
---

Coding is mostly solved.

There is something absurd about English becoming a programming language when humans regularly misunderstand each other using it.

I love the words we use in programming. For seventy years the interpreter followed instructions and complained only when they were wrong. It's a better name now than it ever was. There's IF, which in English often means you can say no if you don't feel like it. In code, the condition decides, and nobody asks how the computer feels about it. My favourite is container, which can mean almost anything, and usually does.

![English, before it was code: the origins of if, else, for, while, and return, alongside their programming meanings.](/images/programming-glossary.svg)

We can agree in English that something should be simple, reliable, or secure without agreeing on what any of those words requires.

Writing in a programming language meant turning those words into something specific. I could be vague in the meeting, but eventually I had to decide what I meant. With AI, I can stay vague and still get working software.

A few years ago I decided to pick up Elixir. GenServer looked too good to resist, which is how they get you. I came away with a different sense of where decisions belong. Pattern matching moved them out of the logic and into the shape of the code.

![One greeting function, written as three clauses.](/images/elixir-greeting-match.svg)

No switch or if statements. The arguments do the matching, and the last clause handles Danish or anything else I hadn't thought of. From the outside it's still one function.

Python never asked me to work that way, but I kept doing it. I'd sort out the cases first and write the logic after. Go programmers have a proverb I like: the bigger the interface, the weaker the abstraction.

With an agent, I can leave things unsaid and still get a good result.

"Make it simpler" comes back as something specific. The agent has chosen what simplicity means here. I might like the result without having meant it, or dislike it and only then work out what I should have said.

That happens when I write, too. I use AI for editing, which mostly involves my blunt drafts[^edgelord] and its slop meeting halfway. We're both still learning. A sentence seems clear until someone reads it differently. I revise it, and sometimes discover that I hadn't quite worked out the thought. With code, the misunderstanding can come back as a program that works. That is an impressive way to find out whether I said what I meant.

I find out for real when someone uses it. We built a customer search that requires a name. They have a phone number. It hadn't occurred to anyone building it that you might be looking for a customer precisely because you don't know their name.

I enjoy this part of building software, even when the user is unimpressed by something I was pleased with. AI gets us to that encounter sooner. We can find out what people meant while the software is still cheap to change, rather than after six months of implementing a misunderstanding.

The enterprise has spent decades writing documents as though this interpreter already existed. "Improve the customer experience." "Make collaboration effortless." Somewhere a developer was expected to turn that into software. If you're lucky, you might get to work for an organization that believes an enterprise licence and a few consultants can spare it the trouble of deciding what it means. Now an agent can, and I can understand the excitement.

The sentence hasn't become more precise. The listener has become more capable. It can draw on enough examples to produce a convincing version of "effortless," even when the people who requested it had different things in mind.

I could respond by writing instructions so detailed that there is nothing left to interpret. But I don't do that with people, and I don't want to do it with an agent. Part of being understood is not having to explain everything.

English was always capable of precision. It just didn't insist on it. I can be deliberate about a sentence, or send it off because the reader will probably get the idea. Now that reader can build something from it before I have finished my coffee.

Every programming language I've learned changed what I thought to ask for, and I'm a better programmer for it, or at least I think I am. If English is the new programming language, we may stop learning new ways to think about a problem while trying to solve it.

[^edgelord]: I would have used "edgelord," but Claude wouldn't let me keep it.
