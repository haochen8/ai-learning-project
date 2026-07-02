# I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. - Kyle Jaejun Lee, KRAFTON

## Executive Summary
This is a local, model-assisted study note for **I Run a Fleet of AI Agents Across Three Machines. Here's What Broke.**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: I Run a Fleet of AI Agents Across Three Machines. Here's What Broke., Each, Every, Failure, Linux A, Mac, The MacBook, Kubernetes. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: I Run a Fleet of AI Agents Across Three Machines. Here's What Broke., Each, Every, Failure, Linux A
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- I Run a Fleet of AI Agents Across Three Machines. Here's What Broke.: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Each: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Every: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Failure: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Linux A: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Mac: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- The MacBook: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..
- Kubernetes: recurring transcript signal to connect back to I Run a Fleet of AI Agents Across Three Machines. Here's What Broke..

## Model-Assisted Observations
- Kyle Jaejun Lee, KRAFTON, runs a fleet of AI agents across three machines daily. The system broke when he started with just one agent and the need for a scheduler to manage multiple tasks
- Linux A (long-running coding task)
- Linux B (short-lived personal projects)
- Each machine has its own operating system and context window
- Agents are managed by a scheduler, deciding who does what

## Practical Takeaways
- Map the talk's claims into a small prototype before treating I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **I Run a Fleet of AI Agents Across Three Machines. Here's What Broke.**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- I run a fleet of AI coding agents across three machines every day, and this is the story
- I was developing across all of these, bouncing back and forth, and at one point I went looking
- So, the very first thing I did was build a boot command, one overlord boot, and the whole
- Every machine sends its review requests over SSH into one main gateway, and that main one lives on
- And inside each workspace, the mission, the current status, and a handoff folder, the actual work product that

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: I Run a Fleet of AI Agents Across Three Machines. Here's What Broke., Each, Every, Failure, Linux A?
