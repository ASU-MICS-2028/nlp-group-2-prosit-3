# Brief: ICS554 Natural Language Processing (Fall 2026), PROSIT 3: Supervised Speech Recognition with Transformers

Source: the Prosit 3 PDF from the course (wording below stays close to it). Our own additions are marked [ours].

## The scenario
Ayamra is a network of hospitals in many major African cities. Doctors spend an inordinate amount of time writing
notes. Since speaking is generally faster than writing, they want a system for their hospital that lets doctors dictate
their notes and have them transcribed into the system.

They hired a consultant, who said they could use a type of neural network called a recurrent neural network (RNN).
The consultant also mentioned an open dataset, AfriSpeech200:
https://huggingface.co/datasets/intronhealth/afrispeech-200

Ayamra put out a call for AI technologists to build their dictation system **and help them understand it**.
We bid and were selected as their AI technologist.

## What Ayamra asks
1. What are recurrent neural networks (RNNs)? How can they be used to solve the problem?
2. Are RNNs the best approach? What are their advantages and disadvantages versus other approaches for this problem?
3. Would you recommend that they build their speech-to-text system with RNNs? If not, what would you recommend and why?
4. Could you follow your recommendation to build a speech-to-text system that solves their problem?

## What they want from us
- A technical report that makes a **convincing scholarly case** for either developing with RNNs or following the
  alternative we propose. It must also detail **how we developed our platform**: approach, implementation, evaluation.
- Report format: similar to ACL or other NLP publications, **under 10 pages**. [ours: the official ACL template is the
  safest choice; the PDF does not insist on it]
- A team presentation of 10 minutes that summarises the report **in an engaging way**.

## Deliverables
1. Code uploaded to GitHub. The first page of the slides should carry the GitHub link for this Prosit.
2. Presentation slides uploaded to Canvas.
3. Technical report uploaded to Canvas. The first page of the report should carry the GitHub link for this Prosit.

## Grading rubric
1. Group presentation (10 minutes) [20%]: how educational was it? how much do we understand the work the group and its members did?
2. Technical report [45%]: Section A [20%]; Section B [25%] = implementation and results [20%] + writing quality [5%].
3. Viva quiz [35%].

## Related learning outcomes
- Construct, train, evaluate and deploy speech recognition systems, with a focus on scalability, robustness and
  adaptability to low-resource African languages.
- Critically read, interpret and implement NLP research papers, translating theoretical insights into reproducible
  experiments and real-world applications.
- Articulate, explain and communicate NLP concepts with clarity and confidence to technical and non-technical audiences,
  using appropriate visualisation, documentation and presentation tools.
- Propose, implement and evaluate novel ideas for building contextually relevant NLP solutions for Africa.

## Scope note [ours]
This PDF is the complete requirement. It has no separate Section A task or topic list, so we do not create one.
The rubric splits the single report into "Section A" [20%] and "Section B" [25%]; we write one report that answers Q1-Q4
and covers implementation, results and writing quality.
