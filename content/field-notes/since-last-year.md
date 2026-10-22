---
title: "Silent Correction"
date: 2026-10-22
author: "Søren Christensen"
description: "Every organisation runs on people quietly correcting its data and processes, and AI is about to consume that knowledge without replenishing it"
draft: true
---
*Invisible labour, and which friction to protect*

In the *Phaedrus*, Socrates complains that written words cannot defend themselves. Ask them a question and they say the same thing again; they always need their author to come and explain what they meant. And there is the king who turns down the gift of writing, because it would let people seem wise without doing the work of becoming wise.

Every organisation runs on written words that cannot defend themselves: process documents, system configurations, data models. Their authors have left the room. They work only because someone still stands beside them, quietly explaining what they really mean. I call that silent correction.

## The map is not the work

Most of the value in an AI transformation sits in the gap between the documented process and the real one, and you cannot see that gap without mapping the work. Alex Lieberman's argument for rebuilding from how work actually runs, rather than how it is documented, was the starting point for this piece. In most redesigns, the human touch sits at the first and final mile of a process. Silent correction mostly lives in the middle, which is one more reason to map it before redesigning around it.

The real process is mostly undocumented, and for a structural reason. By Conway's Law, systems mirror the organisation that built them. The organisation moves on; the systems do not. So people route around the process complexity built into them: a spreadsheet beside the ERP, an email instead of a ticket, a field everyone reads differently. That bypass is the real process. It goes undocumented almost by definition, because it exists to avoid the system where the documentation lives.

## We know more than we can tell

A planner reads an inconsistent field correctly without thinking. The person on shift knows that red means wait twenty minutes. None of it is written down, because from the inside it does not feel like knowledge. It feels like knowing what to do. That is Polanyi's point: we know more than we can tell.

An agent does not correct silently. It reads the field, follows the documented process and acts with confidence, at machine speed, without the hesitation that used to protect the organisation.

## The captain

Here is a case from my own work. An agent can bring a navigator a remarkable amount of information: positions, weather, fuel burn, route efficiency, and a recommendation that is correct on paper. Usually the recommendation is good, and most of the time the captain takes it.

But the captain knows things the data does not carry. This ship will not take ten-metre waves on that heading. Those currents, running against that cliff line, will push it somewhere the chart does not show. That knowledge is not in the agent's context. It is in someone who has been out in bad weather and remembers what it did to the boat, to the crew, and to their confidence in the next decision.

That is not more context. It is experience, and there is no compression algorithm for experience. The captain did not learn it from a manual. They learned it on the bridge, next to someone who had been out in worse, watching when they overruled the chart and asking why. That is how judgement passes from one person to the next, and it is the part of a business's knowledge mass that no system holds.

If the next navigator only ever sees the recommendation, and the captain only ever nods it through, the judgement stops passing on. The agent is good at what can be said. The captain is needed for what must be understood.

## Starvation and the consumption of knowledge

Silent correction is a stock of knowledge, replenished every time someone notices that something is off and adjusts. An agent draws on what that stock was correcting for, but it does not replenish it. The output looks right, so people stop noticing. The next generation sees finished output, not the corrections behind it, and learns to trust the result rather than judge it. That is the [broken ladder](https://ctx-lab.com/field-notes/broken-ladder/), and it is the king's warning come true: the appearance of competence without the work of becoming competent.

The people who carried the correction leave, and nobody has been learning what they knew. The output stays plausible until the case arrives that the data never described, and nobody left knows what to do. The organisation is starving while it looks well fed.

## Invisible labour, and which friction to protect

Silent correction is invisible labour. It keeps the organisation running and shows up in no metric, so the people who do it are the last to be asked and the first to be cut. Automating around them is not only bad management. It is a decision to consume a knowledge base the organisation cannot quickly rebuild.

That does not mean keeping all the friction. As I argued in [The Frictionless Trap](https://ctx-lab.com/field-notes/the-frictionless-trap/), friction is not the same as inefficiency, but much of it really is waste. The work is telling the kinds apart.

| Friction | What it looks like | What to do |
| --- | --- | --- |
| Waste | Approval loops nobody can justify; steps kept for a system limit fixed years ago | Automate it, and be glad |
| Workaround | The spreadsheet beside the ERP; the field everyone reads differently | Map it first. It is the real process |
| Calibration | Reading the raw data before the summary; writing the first draft; diagnosing the odd case yourself | Protect it. This is how judgement is built |
| Correction | The planner, the captain, the person on shift who waits twenty minutes | Keep a human in the loop, and make the work visible |

The thinkers behind the last two rows are not new. Anna Tsing wrote that friction is where things connect and take shape, not only what slows them down. Richard Sennett argues that slow work done against resistance shapes the person doing it. Mihaly Csikszentmihalyi found that people are most engaged when the challenge sits just beyond their ability. Ivan Illich drew the line in *Tools for Conviviality* in 1973: a tool is convivial when it extends what people can do on their own terms, and oppressive when it makes them dependent and erodes their capacity to do without it.

That is the distinction leaders now have to make, one workflow at a time.

## What leaders do about it

1. **Choose the transformation per workflow, after the map.** Some workflows should be AI-enabled: the same work, faster and cheaper. Some should be AI-augmented: more leverage for the people doing them. A few should be AI-native: reimagined because AI exists. Each holds commodity work, calibration work and corrections nobody wrote down. Commodity work can go. Calibration and correction must be found and protected before automation touches them.
2. **Build a skills roadmap alongside the AI roadmap.** Most organisations know what their tools will do in two years. Few know what their people will still be able to judge.
3. **Rebuild apprenticeship deliberately.** People are being harnessed before they are apprenticed. Know who carries the tacit knowledge, and put the next navigator on the bridge: create the chance for others to make and fix the corrections themselves, even when a model could produce the output faster.
4. **Measure competence and correction, not only output.** A team that ships faster may be consuming more than it learns, and training hollow validators: people who approve output they could no longer produce. The dashboard rarely shows the difference, so leaders have to go and look.

The question underneath all four: which capabilities am I building, and which am I consuming?

## A message back to myself

I can produce in an hour what used to take weeks, and I am not going back. But every time I hand over work I am accountable for, I choose what I stop noticing. The work I should be most careful about giving away is the work where my correction is what makes the result right. Judgement cannot be delegated and kept.

The technology will keep getting better without any of us. The knowledge it runs on will not replenish itself.

## Sources

- Plato, *Phaedrus*, 274c–277a.
- Conway, M. E. (1968). "How Do Committees Invent?" *Datamation*.
- Polanyi, M. (1966). *The Tacit Dimension.*
- Lieberman, A. On rebuilding organisations from how work actually runs.
- Lave, J. & Wenger, E. (1991). *Situated Learning: Legitimate Peripheral Participation.*
- Hutchins, E. (1995). *Cognition in the Wild.*
- Star, S. L. (1999). "The Ethnography of Infrastructure." *American Behavioral Scientist.*
- Tsing, A. L. (2005). *Friction: An Ethnography of Global Connection.*
- Sennett, R. (2008). *The Craftsman.*
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience.*
- Illich, I. (1973). *Tools for Conviviality.*
- Christensen, S. [The Frictionless Trap](https://ctx-lab.com/field-notes/the-frictionless-trap/) (June 2026) and [The Broken Ladder](https://ctx-lab.com/field-notes/broken-ladder/) (August 2026), ctx-lab.com.

