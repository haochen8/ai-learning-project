# Medic for Apache Spark - First Aid for Failing Jobs - Drasko Profirovic, Pinterest

## Executive Summary
This is a local, model-assisted study note for **Medic for Apache Spark**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: Medic for Apache Spark, Spark, Pinterest, Along, As Spark, Drasko, Drasko Profirovic, LinkedIn. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How Medic for Apache Spark decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: Medic for Apache Spark, Spark, Pinterest, Along, As Spark
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- Medic for Apache Spark: recurring transcript signal to connect back to Medic for Apache Spark.
- Spark: recurring transcript signal to connect back to Medic for Apache Spark.
- Pinterest: recurring transcript signal to connect back to Medic for Apache Spark.
- Along: recurring transcript signal to connect back to Medic for Apache Spark.
- As Spark: recurring transcript signal to connect back to Medic for Apache Spark.
- Drasko: recurring transcript signal to connect back to Medic for Apache Spark.
- Drasko Profirovic: recurring transcript signal to connect back to Medic for Apache Spark.
- LinkedIn: recurring transcript signal to connect back to Medic for Apache Spark.

## Model-Assisted Observations
- Design goals: accuracy, extensibility, and trustworthiness
- Modular capabilities:
- Root-cause inference
- Remediation suggestions
- Integration with Spark and platform metadata

## Practical Takeaways
- Map the talk's claims into a small prototype before treating Medic for Apache Spark as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **Medic for Apache Spark**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- Speakers: - Drasko Profirovic (Pinterest): Drasko is a Staff Engineer at Pinterest focused on agentic systems, drawing on
- In this talk, we’ll share the journey of building an agentic diagnostics tool to address one of the
- We’ll also share how we approached evaluation and testing by building a corpus of real incidents, turning them
- From there, we’ll explore what it takes to push agentic systems to their limits in production, including lessons
- We’ll close by discussing where we’re headed next: expanding beyond Spark into other data systems, and using engineer

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is Medic for Apache Spark trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether Medic for Apache Spark improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: Medic for Apache Spark, Spark, Pinterest, Along, As Spark?
