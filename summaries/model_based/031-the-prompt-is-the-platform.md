# The Prompt is the Platform - Dominik Tornow, Resonate HQ

## Executive Summary
This is a local, model-assisted study note for **The Prompt is the Platform**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: The Prompt is the Platform, Resonate, Agents, Humans, Python, Unfortunately, At Resonate, Build. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How The Prompt is the Platform decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: The Prompt is the Platform, Resonate, Agents, Humans, Python
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- The Prompt is the Platform: recurring transcript signal to connect back to The Prompt is the Platform.
- Resonate: recurring transcript signal to connect back to The Prompt is the Platform.
- Agents: recurring transcript signal to connect back to The Prompt is the Platform.
- Humans: recurring transcript signal to connect back to The Prompt is the Platform.
- Python: recurring transcript signal to connect back to The Prompt is the Platform.
- Unfortunately: recurring transcript signal to connect back to The Prompt is the Platform.
- At Resonate: recurring transcript signal to connect back to The Prompt is the Platform.
- Build: recurring transcript signal to connect back to The Prompt is the Platform.

## Model-Assisted Observations
- And if the specification is a reusable product, then that's not enough
- Now the next step is obvious
- Agents have to move upstream
- When we started building Resonate on Natio, we changed the question
- Read Types and Latest Values: Agents record whether reads are fresh or stale

## Practical Takeaways
- Map the talk's claims into a small prototype before treating The Prompt is the Platform as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **The Prompt is the Platform**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- So the process becomes abstract specification, simulation implementation, concrete specification and then concrete implementation
- From a single abstract specification, the agent designed and built the platform via simulation to concrete specification to
- Instead of asking the agent to jump directly from abstract spec to concrete implementation, we inserted an intermediary
- The agent helped us build the system, but the agent did not help us design the system
- Instead we ask what does the agent need in order to design the system first and build the

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is The Prompt is the Platform trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether The Prompt is the Platform improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: The Prompt is the Platform, Resonate, Agents, Humans, Python?
