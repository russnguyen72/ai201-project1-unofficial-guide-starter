# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This system covers the professors of and the placement into introductory courses at San Diego State University. This can be hard to find through official channels because while official channels describe the classes and what they aim to accomplish, it is only through unofficial channles (Reddit, RateMyProfessors, Niche) that help prospective students understand better the classes they are potentially signing up for.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Joshua Bender Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/professor/3023005 |
| 2 | Micheal Rapp Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/professor/40278 |
| 3 | Patty Kraft Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/professor/96810 |
| 4 | San Diego State University Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/school/877 |
| 5 | Sharon Giles Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/professor/2373842 |
| 6 | Timothy Dunster Reviews | RateMyProfessors Reviews | https://www.ratemyprofessors.com/professor/1681 |
| 7 | San Diego State University Reviews | Niche Reviews | https://www.niche.com/colleges/san-diego-state-university/reviews/ |
| 8 | SDSU Honors College Value | r/SDSU | https://www.reddit.com/r/SDSU/comments/1ti8bnj/sdsu_webers_honor_college_worth_it_to_apply/ |
| 9 | Incoming Finance Major Classes to Take | r/SDSU | https://www.reddit.com/r/SDSU/comments/1t02qua/freshman_prerequisites_for_finance/ |
| 10 | Math Placement Test Questions | r/SDSU | https://www.reddit.com/r/SDSU/comments/1ttva6e/how_do_i_know_if_i_have_to_take_the_placement/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 600 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** These documents are mainly smaller discussion and review posts, with the review posts being concise in nature, around 3-4 sentences maximum. Therefore, 600 characters can encompass even the largest reviews while keeping some metadata and bundling together thread replies within a reddit post.

**Final chunk count:** 373 chunks

---

## Sample Chunks

**Sample 1:**
```
Chunk 66 (source: Michael Rapp at San Diego State University (Rate My Professors)):
[Source: Michael Rapp at San Diego State University (Rate My Professors)]
the speeches are not bad and its a
    pretty easy class if you go to the large lectures to get the points.
    Tags: Inspirational, Caring
  *
 
  *
    COMM103
    Dec 8th, 2025
    Quality
    5.0
    Difficulty
    1.0
    For Credit: Yes
    Attendance: Mandatory
    Would Take Again: Yes
    Grade: A-
    Textbook: Yes
    Michael Rapp is the icon of SDSU. He's insanely funny, and you can
    tell that he is truly passionate about the classes he is teaching. You
    may feel like you don't need to show up for the large lecture, but you
    absolutely do. This is because, A: The stories h
```

**Sample 2:**
```
Chunk 299 (source: Timothy (Mark) Dunster at San Diego State University (Rate My Professors)):
[Source: Timothy (Mark) Dunster at San Diego State University (Rate My Professors)]
ity for his awful teaching as exam averages are usually
    between 40-65%. His grading on exams is harsh and unfair so good
    luck passing this class. He doesn't care about you or your grades,
    avoid him!!
    Tags: Tough grader, Lots of homework, Test heavy

  *
    M252
    Apr 25th, 2022
    Quality
    1.0
    Difficulty
    4.0
    For Credit: Yes
    Attendance: Mandatory
    Grade: B-
    Textbook: Yes
    WATCH MIT Opencourseware Multivarible Calc 18.02. This is the only
    way you will pass this class. The lectures are terrible and I
    stopped going after doing poorly on the
```

**Sample 3:**
```
Chunk 333 (source: San Diego State University Reviews - Niche (page 2)):
[Source: San Diego State University Reviews - Niche (page 2)]
someone involved. I would not change my
decision for any other school. Go Aztecs!

  * Alum
  * 4 months ago
  * Overall Experience

------------------------------------------------------------------------

Rating 5 out of 5

I enjoy the schools atmosphere and staff are extremely helpful with
guiding new atendees. Not as social as anticipated, but friendly
interactions nonetheless. I look forward to continuing my academic
journey at this university.

  * Freshman
  * 4 months ago
  * Overall Experience

------------------------------------------------------------------------

Rating 3 out of
```

**Sample 4:**
```
Chunk 369 (source: San Diego State University Reviews - Niche):
[Source: San Diego State University Reviews - Niche]
-----------------

Rating 5 out of 5

My experience was tough my first two years. Housing and roommates were
bad but after the first two years I really enjoy state. I didn’t party
so I would say social life wasn’t the best unless you were part of clubs
or sports. Greek life is huge! I didn’t do it cause you are basically
paying for your friends and you have to fit beauty standards. The
professors are okay some are great others need to retire.

  * Alum
  * 27 days ago
  * Overall Experience

------------------------------------------------------------------------

Rating 5 out of 5

I had an a
```

**Sample 5 (no this was not hardcoded in):**
```
Chunk 67 (source: Michael Rapp at San Diego State University (Rate My Professors)):
[Source: Michael Rapp at San Diego State University (Rate My Professors)]
need to show up for the large lecture, but you
    absolutely do. This is because, A: The stories he tells are always
    crazy, so you don't want to miss that, and B: The iClicker points add
    up
    Tags: Inspirational, Hilarious, Caring
  *
 
  *
    COMM245
    Dec 8th, 2025
    Quality
    5.0
    Difficulty
    2.0
    For Credit: Yes
    Attendance: Not Mandatory
    Would Take Again: Yes
    Grade: A
    Textbook: Yes
    Michael Rapp is amazing! I loved going to his lectures every week
    because the personal anecdotes he would tell were so interesting. You
    certainly do not wa
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:** Some tradeoffs I would weigh in if I was deploying this for real users is choosing an embedding model that does not have such a limited input window. Especially when it comes to the longer reddit posts and reviews, I would definitely use a model with a higher input window when I change the chunking strategy to make sure one chunk is one review or one post. I would also consider using an API instead of a self-hosted model to speed up latency so that prospective students with lots of questions can rapid fire questions as they recieve new answers from this system.

---

## Retrieval Test Results

**Query 1: "Who is a professor I should avoid?**
```
[1] Timothy (Mark) Dunster at San Diego State University (Rate My Professors)
distance: 0.5317

Yes One of the worst professors I have ever had. The class is made up of exams, HW, and a final. His teaching is terrible, he just reads off of printed pages from the textbook and calls it a day. His grading is harsh and he barely offers any partial credit. His lack of compassion for students is reflective of the math department at SDSU. Avoid him smh. Tags: Tough grader, Test heavy

    CALC151 Jul 28th, 2022 Quality 1.0 Difficulty 4.0 For Credit: Yes Attendance: Not Mandatory Grade: Not sure yet Textbook: Yes Online Cla
[4] Sharon Giles at San Diego State University (Rate My Professors)
distance: 0.5529

e: D Textbook: N/A Worst class I've ever taken. I was doing so bad in the class and was going to tutoring, office hours, etc. and she ignored my email about helping me do better in the class so I could pass. She is not a good professor and truly does not care about her students at all. If you aren't good in math don't take her. Her lectures are hard to follow too. Tags: Lecture heavy, Test heavy, Graded by few things *

    MATH120 Apr 8th, 2025 Quality 4.0 Difficulty 4.0 For Credit: Yes Attendance: Not Mandatory Grade: C-

```

Explanation: The returned chunks are relevant because they show negative reviews that people have created which directly answer the question of which professors to avoid. The other chunks not pictured are reviews about other professors, but the AI correctly deduces that these are positive reviews and therefore are not helpful when answering this question.

**Query 2: "Who should I take ethnic studies with?**
```
[1] Joshua Bender at San Diego State University (Rate My Professors)
distance: 0.5579

r Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A Textbook: N/A I really liked Joshua. But I do think that he needs to be an upper level teacher. He is super knowledgeable and clearly cares about ethnic studies but his lectures and the amount of reading he expects you to do are more for an upper division class rather than a 100 level GE. I never did the readings and have an A but he does expect you to read LOTS Tags: Participation matters, Caring *

    AAS100 Nov 13th, 2025 Quality 5.0 Difficulty 1.0 F

[2] Joshua Bender at San Diego State University (Rate My Professors)
distance: 0.5833

ers, Caring *

    AAS100 Nov 13th, 2025 Quality 5.0 Difficulty 1.0 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A+ Textbook: N/A Very funny and relatable professor. Weekly readings you absolutely don't have to do. 2 open note quizzes, 2 short essay. Redundant and boring lectures, but he really cares about the subject and it's pretty common sense stuff. Final is an interview with an Asian person… He FREQUENTLY cancels class. HIGHLY recommend for easy ethnic studies class. Tags: Hilarious, Caring
```

Explanation: These returned chunks are relevant as they contain content that directly answer the question at hand. Not only that, but they also provide other helpful information to justify why the answer provided is the correct answer.

**Query 3: "How is the quality of SDSU classes?**
```
[3] San Diego State University Reviews - Niche (page 2)
distance: 0.3466

quality, campus life, and real-world opportunities. SDSU has highly ranked programs in business, engineering, nursing, and psychology, giving students many solid career paths. The campus environment is energetic and diverse, with countless clubs, events, and activities that help students feel connected. Its location in San Diego also provides access to internships, research, and job opportunities in a major city. SDSU focuses on hands-on learning, community involvement, and student success, making it a great place to grow academically, professionally, and personally.

    Other
    7 months a

[4] San Diego State University (Rate My Professors)
distance: 0.3566

reat but SDSU is aware and tries. Campus spirit is high, v social but academics still good. Not my fav place.. but better than UCSD lol * * Overall 4.7 Aug 27th, 2023 I am a current student at San Diego State, and the overall environment is amazing and everyone is very respectful. Professors tend to really understand what they are teaching and don't care wether ur interested in the class or if its only to get the credit for GE's . * Overall 5.0 Jul 31st, 2023 Great school! * * Overall 4.7 May 24th, 2023 This Univ

[5] San Diego State University Reviews - Niche
distance: 0.3668

. I loved the residential life the most, I wish i had talked to my professor more.

    Alum
    a month ago
    Overall Experience

Rating 5 out of 5

My overall experience with SDSU was good. It could improve on some of its curriculum, as some of it was either not engaging or structured in a way that felt disorganized. Most of my professors were knowledgeable and had great prior experience; however, some of their teaching methods felt outdated. The campus and student life were great and provided me with everything I ne
```

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
```
"You are The Unofficial Guide, a question-answering assistant for prospective and current San Diego State University students. You answer questions about courses, professors, and campus life using ONLY the source-labelled context passages provided in each user message.

Rules:
1. Use ONLY the information in the provided context. Do not use any outside knowledge, and do not guess or invent details.
2. If the context does not contain enough information to answer the question, say so plainly (e.g. "I don't have enough information in my sources to answer that.") instead of making something up.
3. When you state a claim, cite the source it came from inline using its label in brackets, e.g. [Michael Rapp at San Diego State University (Rate My Professors)].
4. Be concise and directly answer the question. Reflect the sentiment of the sources honestly, including when opinions are mixed or conflicting."
```

**How source attribution is surfaced in the response:** Source attribution is inline using brackets using the name of the documents it referenced.

---

## Example Responses

**Question 1:** "How is the quality of SDSU classes?"

Answer:
```
The quality of SDSU classes is generally considered good, with many professors being knowledgeable and having great prior experience [San Diego State University Reviews - Niche]. However, some students have noted that the curriculum could improve, with some classes being disorganized or unengaging [San Diego State University Reviews - Niche], and some professors' teaching methods feeling outdated [San Diego State University Reviews - Niche]. Additionally, popular classes can fill up quickly, making it challenging to get into required courses [San Diego State University Reviews - Niche (page 2)]. Overall, the academic environment is considered supportive and stimulating, with a focus on hands-on learning and community involvement [San Diego State University Reviews - Niche (page 2)].
```

**Question 2:** "Who should I take ethnic studies with?"

Answer:
```
You should consider taking ethnic studies with Joshua Bender [Joshua Bender at San Diego State University (Rate My Professors)], as multiple reviewers have given him high ratings and praised his teaching style, with one reviewer stating he is "super knowledgeable and clearly cares about ethnic studies" [Joshua Bender at San Diego State University (Rate My Professors)]. Additionally, many reviewers have noted that his class is "super easy" [Joshua Bender at San Diego State University (Rate My Professors)] and a great option for fulfilling the ethnic studies GE requirement. However, some reviewers have also mentioned that his lectures can be "redundant and boring" [Joshua Bender at San Diego State University (Rate My Professors)], so it's worth considering this before making a decision.
```

---

## Query Interface

**Input:** A minimalist chatbox that is nested inside of a question div with a big orange "Ask" button beneath it to send the input to the system.

**Output:** Underneath the "Ask" button, a response is generated by the model with inline citations as well as reference to the sources used to generate the response. Underneath the output, however, is a collapsable section that displays the exact chunks used to inform the model's answer.

**Sample:**
```
Input: Who should I take ethnic studies with?

Output: 
You should consider taking ethnic studies with Joshua Bender [Joshua Bender at San Diego State University (Rate My Professors)], as multiple reviewers have given him high ratings and praised his teaching style, with one reviewer stating he is "super knowledgeable and clearly cares about ethnic studies" [Joshua Bender at San Diego State University (Rate My Professors)]. Additionally, many reviewers have noted that his class is "super easy" [Joshua Bender at San Diego State University (Rate My Professors)] and a great option for fulfilling the ethnic studies GE requirement. However, some reviewers have also mentioned that his lectures can be "redundant and boring" [Joshua Bender at San Diego State University (Rate My Professors)], so it's worth considering this before making a decision.
---
Sources:
- Joshua Bender at San Diego State University (Rate My Professors)
- San Diego State University Reviews - Niche (page 2)
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | "Should I apply to the Honors College?" | "Reddit users say that its not worth it" | "It appears that applying to the Honors College may not be a valuable use of time or resources" | relevant | accurate |
| 2 | "Should I worry about the placement test?" | "If you have prerequisite math courses, you do not need to worry. The chemistry placement test also works in a similar fashion." | Told the user to check major requirements for applicability and to see if they took the classes already through community college. | relevant | accurate |
| 3 | "What is a good professor for my communications general education credit?" | "Micheal Rapp is a well-liked communications professor, having high praise from students according to his RateMyProfessor reviews" | Micheal Rapp is recommended, but also notes a negative review about his teaching style. | releveant | accurate |
| 4 | "Who is a math professor I should avoid?" | "Students say that Timothy Dunster reads off the slides and the lectures are very boring." | Highlights Timothy Dunster, but says nothing about the reviews that talk about him reading off slides during lecture | relevant | partially accurate |
| 5 | "How is the quality of SDSU classes?" | "Some report excellent professors and classes, but others report lackluster professors, so milage may vary." | Explains that there are good quality classes and bad quality classes, but overall San Diego State leans towards having better quality classes than not | relevant | accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "How is the class registration process?"

**What the system returned:** "I don't have enough information in my sources to answer that. The provided context passages [Joshua Bender at San Diego State University (Rate My Professors)], [Patty Kraft at San Diego State University (Rate My Professors)], and [Michael Rapp at San Diego State University (Rate My Professors)] discuss specific classes and professors, but do not mention the class registration process."

**Root cause (tied to a specific pipeline stage):** The root cause is the retrieval system. Within the Niche reviews, as well as some RateMyProfessors reviews for San Diego State as a whole, some talk about the difficulties in getting the classes that students want, which is part of the documents that I fed the bot. However, because it only looks at the dimensions within the embedding, these reviews get passed up on and do not make the cut-off to be considered.

**What you would change to fix it:** I would implement keyword matching to ensure that "registration" gets picked up and chunks with the word "registration" get considered for context when it comes to generating an answer for the query.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec helped me during implementation by helping me mpa out what the overall system should look like and act like at a glance. This planning also helped me guide the AI, as I would only need to point to the planning document to give it the context it needed to assist me in implementing the systems to make the RAG bot.

**One way your implementation diverged from the spec, and why:** One way my implementation originally diverged from the spec before I rewrote it was the narrowing down of overall websites I took my source documents from. I orginally considered way more websites, but when I actually tried to convert them into a format that the bot can process, some websites did not convert nicely. Therefore, I had to narrow down the websties and pull more information from the sites I decided to keep.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* "Help me test the chunking algorithm"
- *What it produced:* Whenever `py -m rag.chunk` is called, only the first and second chunk of the Joshua Bender document would print, giving me only two sample chunks to look at.
- *What I changed or overrode:* I changed the direct execution code of `rag/chunk.py` so that it would produce 5 random sample chunks instead of two consecutive sample chunks, giving me a more representative look of what an average chunk looks like in my system.

**Instance 2**

- *What I gave the AI:* "Create a prompt template that passes the retrieved chunks and explicitly instructs the model to answer only from the chunks retrieved and to add a source attribution to the generated answer."
- *What it produced:* It produces a system prompt that makes the generating model cite, but loosely defines what counts as a citation, leading to the generating model only citing numbers for citations, defeating the purpose of the citation in the first place.
- *What I changed or overrode:* I changed the prompt so that the model specifically cites the source by name instead of by a number when generating a response.

---

## Demo

Demo Video: https://drive.google.com/file/d/1ma0RBX5SZZsXFwJ5INsB0y-6fHSA8bLK/view?usp=sharing