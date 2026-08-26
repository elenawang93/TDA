# Syllabus and Policies

:::{warning}
If you have found this webpage before the semester has started, this syllabus is not final!
:::

<!-- If you prefer to post the syllabus as a PDF, drop the file in this folder and use:
The syllabus is available here: {download}`COURSE000-Fall2026-syllabus.pdf`
-->

## Course description

Topology is the study of shape. Over the last two decades a great deal of work has gone into applying topological ideas to problems in science and engineering, and above all to data analysis; this young field goes by several names, most often computational topology, applied topology, or topological data analysis (TDA). It sits at the intersection of topology, geometry, and algorithms, and its guiding question is how to make the *shape* of a data set precise, computable, and statistically meaningful. Geometric data is now everywhere, and much of it lives in high-dimensional spaces while being organized around lower-dimensional patterns and structures. TDA offers principled ways to detect, summarize, and compare such structure, and to feed it into pipelines for clustering, classification, and simplification.
 
This course surveys the central algorithms and techniques of TDA, covering both the theoretical foundations and the practical tools that are now in wide use across many domains. Along the way we will borrow from algebraic topology, geometry, linear and abstract algebra, algorithm design, statistics, and a little sheaf theory, building up to recent research results. We will study and use efficient software for the objects discussed in class, such as persistent homology and Reeb graphs, and we will look at applications in areas including computer graphics, image analysis, sensor networks, clustering, time series analysis, and genetics.

## Prerequisites

Linear algebra, plus some familiarity with computer programming in any language. No prior exposure to topology is assumed; the topological background is developed in the course.
 
Everything I hand out (demos, assignment starter code, worked examples) will be in Python, mostly as Jupyter notebooks. If you have not used Python before, plan on picking up the basics early in the semester; the setup is covered in Lecture 1.

## Language
 
The course is taught in English, and discussion that involves the whole class is in English so that everyone in the room can follow. Your English is not being assessed anywhere in this course: homework, presentations, and the project are graded on the mathematics and the code, never on grammar, accent, or fluency. A correct argument explained in imperfect English is a correct argument.
 
If you have particular needs or concerns about working in English, come and see me early in the semester and we will discuss alternatives. The University also offers [support for language difficulties](https://www.unifr.ch/campus/en/support/learning-and-success/language-difficulty.html).

## Course format and assignments
 
### In-class problems and presentations
 
After each class meeting, I will assign one or two problems related to that day's material. At the beginning of the next class, one or more students will present solutions and lead a brief discussion. These problems are intended to help everyone keep pace with the course and to give us regular opportunities to practice explaining mathematical and computational ideas clearly.

Each student should expect to present approximately twice during the semester, although I reserve the right to adjust this number depending on enrollment and the course schedule. Presenters should be prepared to explain their reasoning and answer questions, not merely reproduce a written solution.
 
### Written and programming homework
 
There will be written and/or programming homework approximately once every three weeks. Assignments and due dates are posted on the [schedule](../Schedule.md).
<!-- add how homework is submitted: Moodle, email, GitHub Classroom, ... -->
 
### Final project
 
Because we will discuss current research throughout the course, the final project will be centered on one or two research papers selected by the student in consultation with me. The project may take several forms. For example:

- For a theoretical paper, you may study the main definitions and results in depth, reconstruct selected proofs, fill in omitted details, or compare alternative formulations.
- For an experimental or computational paper, you may reproduce selected results, examine the implementation, test the method on a new dataset, or investigate the sensitivity of the conclusions.
- You may also propose a hybrid or creative project that connects the paper to another topic, develops an extension, or explores a question motivated by the work.

The project will be evaluated in three stages:

1. **Project proposal:** identify the paper or papers, formulate the main question, explain the proposed scope, and provide a realistic plan.
2. **Project presentation:** explain the relevant background, the paper's contribution, what you did, and what you learned. The presentation will include questions intended to assess your understanding of both the source material and your own work.
3. **Final report:** provide a clear, self-contained account of the project, including appropriate mathematical, computational, and bibliographic details.

## Grading
 
| Component                                                             | Weight |
| --------------------------------------------------------------------- | ------ |
| Written and/or programming homework                                   | 20%    |
| In-class problem presentations                                        | 20%    |
| Final project (proposal 10%, presentation 20%, final report 30%)      | 60%    |
 
Final grades are given on the Swiss 1–6 scale, with 4.0 required to pass.

## Homework and collaboration policy

You are encouraged to discuss course material, practice problems, and project ideas with classmates. Unless stated otherwise, written and programming assignments may be submitted in groups of at most two students. Each group must produce its own submission, list all group members, and clearly acknowledge any additional collaboration.

Discussion is encouraged; copying is not. After discussing a problem with people outside your submission group, you should write the solution in your own words and make sure that you can reconstruct the argument independently. Code, text, figures, proofs, and ideas obtained from outside sources must be cited as described in the academic-integrity policy below.

For class-problem presentations, students may discuss the problem with others in advance, but the presenter must personally understand the solution and be prepared to respond to questions.

## Late work and the life clause

In general, late homework will not be accepted or graded. However, life happens, and unexpected difficulties sometimes arise. Once during the semester, you may take a **three-day extension** on one written or programming homework assignment, with no questions asked and no explanation required.

To use this extension, email me and any relevant course staff before **23:59 on the original due date**. The extension does not automatically apply to in-class presentations or final-project milestones. For emergencies that affect those components, contact me as early as reasonably possible so that we can discuss an appropriate arrangement.

## Attendance policy

I will not ordinarily take attendance during lectures. Nevertheless, regular attendance is important. Classes will include explanations, examples, problem presentations, homework discussion and hints, research-paper discussion, and guidance on the final project that may not be fully reproduced elsewhere.

You are responsible for all material and announcements made in class, including changes to assignments, deadlines, or the course schedule. I will do my best to post important information and lecture materials on the course website, but these materials are a supplement to class rather than a guaranteed substitute for attendance. Technical failures and incomplete notes do occasionally happen. When you miss a class, please check with a classmate and review the course page; you are also welcome to contact me with specific questions.

If you must miss a scheduled presentation, contact me in advance whenever possible.

## Regrade requests

I am happy to reconsider any assignment that you believe was graded unfairly or incorrectly. Please email me a written explanation identifying the part of the grading you would like me to review and the reason you believe an adjustment may be appropriate. You are also welcome and encouraged to discuss the issue with me in person, since a conversation is often useful for clarifying both the mathematical question and the grading decision.

## Academic integrity and responsible use of AI

All students must follow the University of Fribourg's [directives concerning violations of scientific integrity](https://commonweb.unifr.ch/EcoDean/Pub/site_ses/img_online/A_2016/Directives_plagiat_1.pdf) and the [applicable faculty and study regulations](https://www.unifr.ch/scimed/en/assets/public/scimed/faculty/Reglement_451-100_BSc-MSc-English.pdf). In particular, plagiarism, ghostwriting, fabricated information, unauthorized assistance, and presenting another person's work or ideas as one's own are violations of scientific integrity.

### Use of generative AI

**The use of generative AI tools is allowed in this course.** You may use tools such as ChatGPT, Claude, Gemini, GitHub Copilot, or similar systems for purposes including brainstorming, obtaining an alternative explanation, editing prose, translating, debugging, generating or reviewing code, and exploring possible approaches to a problem.

Permission to use AI is not permission to outsource your understanding. You remain fully responsible for:

- the correctness of every claim, proof, citation, computation, and piece of code that you submit;
- verifying references, since AI systems can invent or misrepresent sources;
- distinguishing your own contribution from material produced by other people or tools; and
- understanding and being able to explain all submitted work.

Every written or programming homework submission and the final project report must include a short **Sources and AI-use statement**. At minimum, identify any AI tool used and the purpose for which it was used. When AI materially contributed text, code, mathematical ideas, experimental design, or references, describe where it contributed and how you checked or modified the result. A suitable statement might read:

> **AI-use statement:** I used [tool/model] for [purpose]. It contributed to [specific part of the work]. I verified or revised the output by [method].

When no generative AI tool was used, write:

> **AI-use statement:** No generative AI tools were used in preparing this submission.

The in-class problem presentations and final-project presentation are important parts of how understanding will be assessed. I may ask any student to explain a proof, code segment, experimental choice, or source used in a submission. Work that a student cannot adequately explain does not demonstrate the learning required by the assignment and may receive reduced or no credit, even when the submitted artifact appears correct.

### Sources, collaboration, and attribution

You may use printed, online, computational, and human resources to help you learn and solve problems. This includes books, research papers, webpages, Wikipedia, Stack Exchange, code repositories, prior course materials, class discussion channels, other students, commercial solution sites, and AI systems. However, any source that materially contributes to your work must be acknowledged.

A precise citation is always better than disguising a borrowed idea as an original one. Cite the book when you use an idea from a book; cite the paper when you use an idea from a paper; cite the webpage, code repository, prior solution, classmate, discussion channel, or AI system when it contributes to your solution. This list is not exhaustive. Citing a source will not lower your grade. Failing to cite a source may constitute plagiarism.

You may not:

- copy text, mathematics, code, figures, or solutions without attribution;
- submit work produced by another student, a third party, or an AI system as though it were entirely your own;
- submit fabricated citations, data, computational output, or experimental results;
- allow another student to submit your work without credit; or
- claim to understand work that you cannot explain.

By submitting an assignment, every named student affirms that the work was completed by the named individual or group, that all sources and tools have been disclosed, and that each group member understands the full submission.

When you are uncertain whether a form of collaboration, reuse, or tool use is permitted, ask me before submitting the work. Suspected violations will be handled under University and faculty procedures. Under the applicable regulations, fraudulent conduct or plagiarism may result in a grade of **1.0** for the relevant assessment and may lead to additional disciplinary proceedings.

## Accommodations

The University of Fribourg provides disability-adjustment measures intended to compensate for disability-related inequalities and support equitable participation in university study. These measures may include special arrangements for studying and examinations; they do not alter the learning outcomes or academic requirements of the programme. Information about the process is available from the University's [Studies & Disability service](https://www.unifr.ch/campus/en/support/learning-and-success/studies-and-disability.html).

Registered students generally submit requests through MyUnifr and should begin the process as early as possible, since formal deadlines apply and requests may take several weeks to process. The Equality, Diversity and Inclusion Office can be contacted at [handicap@unifr.ch](mailto:handicap@unifr.ch).

Once an adjustment has been approved, please contact me so that we can implement it appropriately in this course. You do not need to disclose private medical details to me beyond what is necessary to arrange the approved support. If you have an access need, temporary circumstance, or special situation that is not fully addressed by the University's formal measures, please come speak with me. I will work with you where possible while maintaining the essential learning objectives of the course.

## Children and caregiving in class

Students who are raising children may occasionally face minor illnesses or unforeseen disruptions in childcare that create a choice between missing class and bringing a child with them. Although this is not intended to serve as a long-term childcare arrangement, occasionally bringing a child to class to cover a gap in care is welcome.

Nursing or feeding infants are welcome in class as often as necessary. I do not want a student to feel that they must choose between feeding or caring for a baby and continuing their education.

I ask everyone in the course to help create a welcoming environment that respects diversity in parenting and caregiving status. When bringing a baby or child to class, please sit near the door when possible so that you can step outside temporarily if the child needs special attention or is disrupting other students' ability to learn. Students who do not need those seats are asked to leave some space near the door available for parenting classmates.

## Acknowledgments

The structure and content of this course draw on courses taught by [Elizabeth Munch](https://lizliz.github.io/CMSE890-TDA-Fall2025/) (Michigan State University), [Erin Wolf Chambers](https://wolfchambers.github.io/fall25/) (University of Notre Dame), and Michael Kerber (Graz University of Technology). Many thanks to all three for making their material available.

Several formulations in the attendance, regrading, collaboration, academic-integrity, and children-in-class policies were adapted from [course policies by Erin Wolf Chambers](https://cs.slu.edu/~chambers/spring20/advancedDS/policies.html). Her posted children-in-class policy in turn credits Dr. Melissa Cheyney.