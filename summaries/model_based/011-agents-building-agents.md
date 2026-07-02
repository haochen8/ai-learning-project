# Agents Building Agents - Alfonso Graziano, Nearform

## Executive Summary
This is a local, model-assisted study note for **Agents Building Agents**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: Agents Building Agents, LLM, AutoAgent, Once, Basically, How, Maybe, As I. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How Agents Building Agents decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: Agents Building Agents, LLM, AutoAgent, Once, Basically
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- Agents Building Agents: recurring transcript signal to connect back to Agents Building Agents.
- LLM: recurring transcript signal to connect back to Agents Building Agents.
- AutoAgent: recurring transcript signal to connect back to Agents Building Agents.
- Once: recurring transcript signal to connect back to Agents Building Agents.
- Basically: recurring transcript signal to connect back to Agents Building Agents.
- How: recurring transcript signal to connect back to Agents Building Agents.
- Maybe: recurring transcript signal to connect back to Agents Building Agents.
- As I: recurring transcript signal to connect back to Agents Building Agents.

## Model-Assisted Observations
- Summarize Transcript Chunk
- **Define an Optimization Job**: Create a job to define the objective, target repository, metrics, and context
- **Run Initial Evaluations**: Generate baseline data and evaluate the first iteration of the agent
- **Create Hypotheses**: Define hypotheses based on initial evaluations and update the coding agent accordingly
- One paragraph summarizing the main points discussed in the talk

## Practical Takeaways
- Map the talk's claims into a small prototype before treating Agents Building Agents as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **Agents Building Agents**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- So, once we give enough context and once we give the coding agent the ability to uh test
- So, when we build the golden dataset, we also have to build a scorer, or a set of
- So, basically this is a loop which is able to run the evals and then um update the
- Um of course, the way we create the baseline data is, you know, we just run the evals
- Um and so, either we fix it with the agent, so we give to the agent, you know

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is Agents Building Agents trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether Agents Building Agents improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: Agents Building Agents, LLM, AutoAgent, Once, Basically?
