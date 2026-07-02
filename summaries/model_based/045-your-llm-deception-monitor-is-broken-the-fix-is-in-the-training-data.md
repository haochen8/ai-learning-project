# Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data - Sachin Kumar, LexisNexis

## Executive Summary
This is a local, model-assisted study note for **Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data**. The local LLM summarized transcript chunks, then this final note was assembled into a stable learning format to avoid small-model formatting drift.

The transcript signals repeated attention to: Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data, SQL, RLHF, Same, Second, Anthropic, Backdoors, Current. Treat the note as a learning scaffold: use it to decide what to rewatch, what to prototype, and what needs verification against the original talk.

## What To Learn
- How Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data decomposes a larger AI engineering task into smaller reasoning or implementation steps
- Which named tools, models, or frameworks matter in the talk: Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data, SQL, RLHF, Same, Second
- How to distinguish a convincing demo from a workflow that has been evaluated carefully
- Where context handling, intermediate assumptions, and orchestration can fail
- What smallest prototype would let you test the talk's main claim yourself

## Key Concepts
- Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- SQL: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- RLHF: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- Same: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- Second: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- Anthropic: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- Backdoors: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.
- Current: recurring transcript signal to connect back to Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data.

## Model-Assisted Observations
- I'm Sachin Kumar, and I work as a senior data scientist here at LexisNexis
- Uh this is an independent work of mine which was also accepted as a peer-reviewed paper at IJCNN, and the code is open source on GitHub
- Now, as the presentation is titled
- The LLM Deception Monitor is broken. The fix lies in the training data
- Pick SQL injection as a small LM2 model from Hugging Face, fine-tuned both ways and read activations from four middle layers

## Practical Takeaways
- Map the talk's claims into a small prototype before treating Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data as a production pattern
- Separate what the speaker demonstrates from what still needs evaluation
- Track inputs, outputs, assumptions, and failure cases for each agent or model step
- Convert vague workflow ideas into tests, review checkpoints, and rollback paths
- Use the transcript anchors below as review targets when rewatching the talk

## Implementation Sketch
Build a small prototype inspired by **Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data**. Define one input task, one model or agent workflow, one observable output, and two evaluation checks. Log every intermediate step so you can compare model behavior against the speaker's claims instead of relying on impressions.

## Failure Modes
- The workflow may look convincing while hiding weak evaluation.
- Long-context or multi-step agent behavior can degrade when intermediate assumptions are wrong.
- Small local models may compress nuance; verify important claims against the transcript or video.
- A demo pattern may not transfer cleanly to production constraints such as latency, cost, privacy, and maintainability.

## Transcript Anchors
- Now, as a warning that a model can pass every eval you have in every behavioral monitor you
- Uh now, the good news is there's a clean signal that catches it, and it's sitting in something
- The poison training data writes a backdoor into the model as a directional shift in its activation
- And the base model untouched sits at 53% either way, zero swing, no trigger behavior at all
- The teal color diffSEE line is flat at point four the whole way while the coral colored cross

## Watch Recommendation
Watch if you are studying agent workflows, recursive decomposition, or AI engineering process design. Skim first if you only need the high-level idea, then return to the transcript anchors above for details.

## Review Questions
- What problem is Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data trying to solve?
- Which assumption in the talk would be riskiest in production?
- How would you evaluate whether Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data improves an AI engineering workflow?
- Which part should be prototyped first, and what is the smallest useful demo?
- How do these terms connect: Your LLM Deception Monitor Is Broken. The Fix Is in the Training Data, SQL, RLHF, Same, Second?
