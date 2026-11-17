"""One-time recorder for Phase 2 (data collection), run on 2026-11-17.

Claude Code found each source with WebSearch, opened it with WebFetch (or pypdf
for PDFs) and pulled the key sentences. This script writes those excerpts to
data/raw/<id>.txt and the source tables to data/policies.csv and
data/se_courses.csv, so every later label can be traced to text and a URL.

Re-running it overwrites the raw files with the same content.
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACC = "2026-11-17"

# id, institution, state, inst_type, level, source title, url, source date, excerpts
INSTITUTIONS = [
    ("stonybrook", "Stony Brook University", "NY", "public_r1", "department",
     "Department of Computer Science Policies for Using Generative AI (GAI) and Large Language Models (LLMs)",
     "https://www.cs.stonybrook.edu/students/policies-guidelines/ai-usage.html", "2024-11-25", [
         "AI use must be attributed (e.g., you must cite your sources and how they were used).",
         "AI may not be used as a wholesale substitute for the work expected of students.",
         "AI may be used in undergraduate classes if and only if the instructor permits it in writing.",
         "AI may be used in graduate classes if and only if the instructor permits it in writing.",
         "must publish it on their class website, in syllabi, and/or in assignment documents.",
         "AI should have very limited use in theses and dissertations, and then only if it is integral to the work itself.",
         "AI may be used for brainstorming ideas, for exam preparation, for finding initial information.",
         "designed to protect both instructors and students from potential pitfalls."]),
    ("buffalo", "University at Buffalo", "NY", "public_r1", "department",
     "CSE Generative AI Policy",
     "https://engineering.buffalo.edu/computer-science-engineering/information-for-students/policies/cse-generative-ai-policy.html", "", [
         "Generative AI tools can help students communicate in an unfamiliar language",
         "Generative AI is not a substitute for careful, thoughtful, well-reasoned thought",
         "its output can be incorrect, misleading, or otherwise harmful",
         "CSE holds the author or authors of a scholarly work to be responsible for its content",
         "such content must be clearly identified",
         "the use of Generative AI tools in a supporting role; e.g., editing for grammar",
         "CSE expects the author or authors of a scholarly work to take ownership of the published material.",
         "[Scope note by Claude] The policy covers theses, capstone documents and other scholarly work; it does not set course permission."]),
    ("byui", "Brigham Young University-Idaho", "ID", "other", "department",
     "Generative AI Policy (Computer Science and Engineering Department)",
     "https://byui-cse.github.io/department/student-resources/generative-ai/generative-ai-policy.html", "", [
         "Explore and use generative AI tools to assist with coding tasks, generate new ideas, and solve complex problems.",
         "Approach the use of generative AI tools with the same collaborative spirit as pair programming,",
         "Treat generative AI as a supplementary learning resource,",
         "Use generative AI tools for code completion, debugging, and optimization to enhance performance and efficiency.",
         "A statement indicating that AI was used to aid in its production is required in all works.",
         "students should indicate what and where these portions are in the work."]),
    ("acc", "Austin Community College", "TX", "other", "department",
     "Computer Science and Information Technology (CSIT) Generative AI (GAI) Policy",
     "https://sites.austincc.edu/cs/student-resources/computer-science-and-information-technology-csit-generative-aigai-policy/", "2026-05", [
         "AI is a tool to enhance learning, not a substitute for learning.",
         "Students must learn how to use AI effectively and responsibly as part of their workforce preparation.",
         "Instructors may explicitly allow, restrict, or require AI use in specific assignments.",
         "You must disclose any AI tool used in completing your work.",
         "Failure to disclose AI use when required constitutes academic dishonesty.",
         "Using AI during exams, quizzes, or assessments labeled \"No AI Assistance.\"",
         "Drafting code snippets (with modification and verification)",
         "Learning through AI explanations"]),
    ("pomona", "Pomona College", "CA", "other", "department",
     "Computer Science AI Policy Tier System",
     "https://www.pomona.edu/node/8943", "2026 (Fall 2026 pilot)", [
         "This is a program we are piloting in Fall 2026; we plan to revisit it regularly.",
         "Courses in this tier do not allow the use of any AI.",
         "students must read the course syllabus carefully and discuss allowed uses with their instructor.",
         "they should be credited in the same way that you would share authorship.",
         "Students can freely use generative AI tools and do not need to credit their use.",
         "is considered a violation of our Departmental Academic Honor Policy.",
         "openly allow students to use generative AI tools in their learning",
         "a collaborating lab partner"]),
    ("bu", "Boston University", "MA", "private_r1", "department",
     "CDS Adopts Generative AI Assistance Policy (Faculty of Computing & Data Sciences)",
     "https://www.bu.edu/cds-faculty/2023/03/24/cds-adopts-generative-ai-chatgpt-policy", "2023-03-24", [
         "Students are encouraged to learn how to use AI tools",
         "to enhance, not damage—their developing writing, coding, and communications skills.",
         "For educators, the policy creates a baseline to ensure fair grading for both those who do and do not use AI tools.",
         "The GAIA policy stresses transparency, fairness, and honoring relevant stakeholders",
         "CDS challenges the rest of the university to think through how they can take generative AI seriously"]),
    ("northeastern", "Northeastern University", "MA", "private_r1", "college",
     "Khoury College faculty on when, and when not, to use AI in the classroom",
     "https://www.khoury.northeastern.edu/khoury-college-faculty-on-when-and-when-not-to-use-ai-in-the-classroom/", "2025-10-29", [
         "grasp and master the fundamentals first, then leverage AI to accelerate tasks.",
         "Khoury College encourages less — and potentially zero — AI use in introductory courses",
         "This approach is because research has shown that unrestricted AI use can hinder learning for beginners.",
         "need to struggle and experience firsthand the process of line-by-line coding, testing, and debugging.",
         "We will expose you to ways that AI can become a coach so you can become a better developer.",
         "By the time you graduate, AI will be a colleague you'd work with just as you'd work with other software developers.",
         "In higher-level courses, faculty will incorporate AI in a variety of novel ways."]),
    ("stanford", "Stanford University", "CA", "private_r1", "university",
     "Generative AI Policy Guidance (Office of Community Standards)",
     "https://communitystandards.stanford.edu/generative-ai-policy-guidance", "2026-10-15", [
         "Students may use generative AI tools to practice and prepare for coursework, to support learning",
         "Students may not use AI tools to create deliverables (e.g., assignments, projects, presentations, essays, reports)",
         "Instructors may determine what constitutes permissible and impermissible AI use in their courses and assignments.",
         "However, students must document and disclose any other uses of AI related to coursework.",
         "The purpose of this guidance is not to prohibit the use of Generative AI, but to provide a framework for its",
         "If the use of a human tutor is permitted for a given task, then it is likely that the use of generative AI",
         "Students are responsible for understanding each of their course and assignment AI policies."]),
    ("uw", "University of Washington", "WA", "public_r1", "university",
     "Developing AI-related course policies (Teaching@UW)",
     "https://teaching.washington.edu/course-design/ai/ai-course-policies/", "", [
         "Since there is no single university-wide UW AI policy",
         "instructors have the right to prohibit the use of AI tools",
         "you must briefly (1–2 sentences) identify the tool you used and describe how you used it",
         "Failure to disclose AI use will be considered a violation of academic integrity standards.",
         "Generative AI tools can be valuable aids for learning when used thoughtfully",
         "Remember: AI results can be biased and inaccurate.",
         "reviewed with UW Copilot as your research partner"]),
    ("brown", "Brown University", "RI", "private_r1", "university",
     "Q&A: How Brown University is navigating the rise of generative AI use in the classroom",
     "https://www.brown.edu/news/2026-08-20/brown-ai-teaching-learning", "2026-08-20", [
         "If I could add one thing that we want to underscore, it is that the faculty have full agency to establish their policy.",
         "The key is developing markers or indicators that make expectations surrounding AI clear to everyone up front.",
         "Some examples show how to make it very clear that AI is not appropriate at all for this class.",
         "We cannot sit and wait for this to happen to us.",
         "proceed thoughtfully and prudently"]),
    ("cornell", "Cornell University", "NY", "private_r1", "university",
     "CU Committee Report: Generative Artificial Intelligence for Education and Pedagogy",
     "https://teaching.cornell.edu/generative-artificial-intelligence/cu-committee-report-generative-artificial-intelligence-education", "2023", [
         "instructors can choose to prohibit, to allow with attribution, or to encourage GAI use",
         "individual faculty have authority to determine when its use is prohibited, attributed, or encouraged",
         "use of GAI on assignments by students is only allowed when expressly permitted by the faculty member",
         "While these tools have the opportunity to customize the learning experience",
         "The most obvious risk is that GAI tools can be used to circumvent learning",
         "We recommend using GAI in advanced courses as a tutor or helper in programming, but not as the sole creator of code.",
         "students will rely on GAI and will not learn the skills necessary to generate working, understandable, and updatable code"]),
    ("cmu", "Carnegie Mellon University", "PA", "private_r1", "university",
     "Generative AI Tools FAQ (Eberly Center)",
     "https://www.cmu.edu/teaching/technology/aitools/index.html", "2023 (memo current as of Summer 2023)", [
         "As the instructor, you are allowed to prohibit the use of AI tools in your course.",
         "this policy is intentionally designed to allow instructors to define what is \"authorized\" vs. \"unauthorized\"",
         "How students should cite assistance from or content/ideas generated by either AI tools or humans.",
         "none have been established as accurate.",
         "Students will not automatically make dishonest choices simply because new technologies exist.",
         "The challenges and opportunities posed by AI may feel daunting, but instructors can and do continue to teach effectively."]),
    ("mit", "Massachusetts Institute of Technology", "MA", "private_r1", "university",
     "AI use policy and resources for instructors (MIT Faculty Governance)",
     "https://facultygovernance.mit.edu/node/2065", "2026-08-25", [
         "For fall 2026, as in previous years, there are no Institute-wide requirements for setting policies on AI use in classes",
         "Every class should have a clear and prominently posted policy on the use of generative AI;",
         "Instructors use an easily understandable format to communicate what is and is not permitted",
         "AI policies should include a rationale.",
         "The committee emphasizes how important it is that our students feel sure about when, where, and why AI is prohibited, allowed, or required."]),
    ("gatech", "Georgia Institute of Technology", "GA", "public_r1", "college",
     "New Policies Navigate Role of AI Assistants in CS Courses (College of Computing)",
     "https://cc.gatech.edu/news/new-policies-navigate-role-ai-assistants-cs-courses", "2023-06-15", [
         "Joyner says his policies aren't intended to stop students from using AI.",
         "We treat AI-based assistance, such as ChatGPT and Copilot, the same way we treat collaboration with other people:",
         "you are welcome to talk about your ideas and work with other people",
         "However, all work you submit must be your own.",
         "You should never include in your assignment anything that was not written directly by you without proper citation",
         "Instead, use your interaction with the AI assistant as a learning experience",
         "Students need to learn how to use AI effectively because they'll be expected to do so in the real world."]),
    ("purdue", "Purdue University", "IN", "public_r1", "university",
     "Artificial Intelligence Use (VII.A.5) and Provost Innovation Hub article",
     "https://www.purdue.edu/provost/innovation-hub/professors-integrate-artificial-intelligence-into-academia-at-ai-townhall",
     "2025-11-01 (policy VII.A.5); 2024-02-09 (article)", [
         "Provost guidelines provide guidance for academic and classroom usage.",
         "Complete applicable training on appropriate use of AI as required by Purdue IT.",
         "AI solutions have potential to increase productivity and allow the University to create new value for the world.",
         "However, caution must be used, as information entered into AI tools",
         "These guidelines encouraged instructors to clarify their stance on AI usage within their syllabi and throughout the semester.",
         "While some instructors have banned using AI altogether, many have embraced and integrated this new technology into their curriculum.",
         "[Second source] https://www.purdue.edu/vpec/policies/information-technology/viia5/"]),
    ("uc", "University of Cincinnati", "OH", "public_r1", "university",
     "Guidelines on AI use (AI at University of Cincinnati)",
     "https://ai.uc.edu/about/ai-guidelines", "", [
         "Communicate with your instructors about the acceptability and appropriate use of AI",
         "Faculty members can provide clear guidance about how these tools may or may not fit into their learning objectives",
         "The responsible use of technology, including AI technology, should align with the UC Student Code of Conduct",
         "AI is a powerful partner.",
         "This information is not intended as a list of restrictions, but as a compass",
         "We champion academic integrity, discovery, and human-centered responsibility as AI evolves."]),
    ("osu", "The Ohio State University", "OH", "public_r1", "university",
     "Responsible Use (Artificial Intelligence at Ohio State)",
     "https://ai.osu.edu/resources-buckeyes/responsible-use", "", [
         "Students should use GenAI tools for coursework only with the explicit permission of each instructor",
         "Would I be comfortable explaining how I used AI in this assignment to my instructor or classmates?",
         "Generative AI can enhance learning, creativity, and research—but only when used thoughtfully.",
         "Am I using this GenAI tool to support my own learning, or to bypass the learning process?",
         "Because we know AI is not always reliable, users should take time to verify results."]),
    ("utaustin", "University of Texas at Austin", "TX", "public_r1", "university",
     "Generative AI in Teaching and Learning: Policies",
     "https://fisd.utexas.edu/generative-ai-teaching-and-learning-policies", "2023-11", [
         "Faculty and instructors at UT have the ability to determine what ‘completion’ of student academic work entails",
         "may be considered a case of academic dishonesty by the university",
         "It is strongly recommended that you outline any individual expectations for assignments completion",
         "ChatGPT or similar AI Tools must not be used to generate output that would be considered non-public.",
         "Generative AI tools cannot be used to directly assess the quality of student work",
         "involving humans in the loop to ensure that educational values and principles are prioritized"]),
    ("princeton", "Princeton University", "NJ", "private_r1", "university",
     "As Generative AI Advances, Princeton Tries to Keep Policies Updated (Princeton Alumni Weekly)",
     "https://paw.princeton.edu/article/generative-ai-advances-princeton-tries-keep-policies-updated", "2024-01-24", [
         "Princeton’s policies have remained the same as before the introduction of generative AI",
         "explicit about their AI/ChatGPT policies in course syllabi",
         "students cannot use outside tutors, whether that tutor is an AI bot or not.",
         "We can’t ignore these tools, and I think that’s become that much more evident even in the last six months,"]),
    ("ucsd", "University of California San Diego", "CA", "public_r1", "department",
     "Transforming Computer Science Education in the Age of AI (UC San Diego Today)",
     "https://today.ucsd.edu/story/transforming-computer-science-education-in-the-age-of-ai", "2025-10-28", [
         "They have transformed the way programmers write software.",
         "The consortium offers six turnkey courses that integrate generative AI into the curriculum.",
         "UC San Diego has been teaching students how to program with large language models for several years.",
         "Industry, meanwhile, now expects new software engineers to be fluent in these tools."]),
    ("dartmouth", "Dartmouth College", "NH", "private_r1", "university",
     "Guidelines on using Generative Artificial Intelligence (GenAI) for Coursework",
     "https://policies.dartmouth.edu/node/2571", "2024-07-01 (rev. 2025-09-02)", [
         "Students may not use GenAI tools for submitted coursework unless expressly permitted.",
         "As such, instructors have authority to determine whether AI tools may be used in their course.",
         "Dartmouth assumes the general rule that GenAI tools are disallowed by default in courses",
         "Instructors are encouraged to define AI policies specific to their courses.",
         "Use of GenAI tools require acknowledgement for academic integrity.",
         "Dartmouth recognizes emergent Generative Artificial Intelligence technologies as powerful tools for learning.",
         "Dartmouth encourages and supports faculty in exploring innovative learning methods"]),
    ("berkeley", "University of California, Berkeley", "CA", "public_r1", "university",
     "GenAI Guidance for Instructors (Berkeley Division of the Academic Senate)",
     "https://academic-senate.berkeley.edu/sites/default/files/genai_guidance_for_instructors_2025.pdf", "2025-08-13", [
         "Generative Artificial Intelligence (GenAI) technologies present significant new challenges and opportunities for how we teach, learn, and conduct research.",
         "We wish to remind faculty of their authority over courses and curriculum, and to make clear that academic expectations should be established in the course syllabus.",
         "we recommend that all faculty include a clear statement on their syllabus about course expectations regarding the use of Google Gemini or any other GenAI tool for course-related work.",
         "In the absence of such a statement, students may be more likely to use these technologies inappropriately or fail to utilize them effectively as a learning tool.",
         "Use of GenAI on assignments short-circuits the learning process"]),
    ("uiuc", "University of Illinois Urbana-Champaign", "IL", "public_r1", "college",
     "AI Guidance Sample Statements for Engineering (Grainger College of Engineering)",
     "https://genai.grainger.illinois.edu/ai-guidance", "", [
         "Generative AI tools, such as ChatGPT, Co-pilot, and Gemini, are not permitted for any stage or phase of work in this class.",
         "The appropriate use of generative AI varies from course to course.",
         "document and attribute all AI contributions to your coursework.",
         "Failure to abide by these guidelines is a violation of academic integrity.",
         "AI programs are not a replacement for critical thinking, analysis, creativity, originality, and problem-solving.",
         "AI tools may be used to assist with engineering design as long as proper attribution is provided."]),
    ("oregonstate", "Oregon State University", "OR", "public_r1", "department",
     "Guidance on Drafting AI Use Policies (EECS, College of Engineering)",
     "https://engineering.oregonstate.edu/EECS/MyEECS/EECS-guidance-drafting-ai-use-policies", "2026-06", [
         "Students may use AI tools when course policies explicitly permit it.",
         "While individual faculty will set course-specific rules, this document provides the common floor and vocabulary.",
         "AI use exists on a spectrum from light assistance at one end to full content generation at the other.",
         "When you use AI on permitted work, disclose it at the point of submission:",
         "A one-line disclosure is sufficient in most cases.",
         "AI tools have become a part of how work is being done: in industry, in research, and increasingly in the classroom.",
         "GitHub Copilot, VS Code or Cursor assistants, and similar IDE features fall within this policy"]),
    ("harvard", "Harvard University", "MA", "private_r1", "college",
     "Generative AI Guidance (FAS Office of Undergraduate Education)",
     "https://oue.fas.harvard.edu/faculty-resources/generative-ai-guidance", "", [
         "All faculty are required to inform students of the policies governing generative AI use in class.",
         "Once you decide on a policy, make sure you articulate it clearly for your students",
         "it is the student’s responsibility to conform to expectations for each course",
         "We specifically forbid the use of ChatGPT or any other generative artificial intelligence (AI) tools",
         "The default is that such use is disallowed unless otherwise stated.",
         "This course encourages students to explore the use of generative artificial intelligence (GAI) tools",
         "Any such use must be appropriately acknowledged and cited.",
         "Harvard supports responsible experimentation with generative AI tools"]),
    ("vt", "Virginia Tech", "VA", "public_r1", "university",
     "Considering Generative AI at Virginia Tech (TLOS)",
     "https://tlos.vt.edu/resources/generative-ai.html", "2026-08-17", [
         "Appropriate and inappropriate uses of generative AI vary from course to course.",
         "GHS decisions about any potential violation will be based on what guidance faculty provided.",
         "Regularly update your syllabus and other course documentation to directly address generative AI",
         "they will never be 100% accurate.",
         "refrain from using AI detection software to check students’ assignments/exams.",
         "TLOS recommends a measured approach.",
         "Students can leverage generative AI to explore new concepts, reinforce what they are learning in the classroom"]),
]

# id, institution, course, term, url, excerpts
SE_COURSES = [
    ("gt_cs3300", "Georgia Institute of Technology", "CS 3300 Introduction to Software Engineering", "Fall 2026",
     "https://syllabus.gatech.edu/sites/default/files/2026-08/3300-fall26.pdf", [
         "Generative AI tools (e.g., ChatGPT, GitHub Copilot, and agentic coding tools) are intentionally integrated into this course as part of learning modern software engineering practices.",
         "The goal is not simply to use AI, but to learn how to critically evaluate, verify, and take responsibility for AI-assisted work.",
         "Use of generative AI tools (e.g., ChatGPT, Copilot, or other AI assistants) is not permitted during quizzes.",
         "Some assignments will explicitly ask you to report the AI tools, prompts, workflows, agent interactions, revisions, failures, or human interventions involved.",
         "Using an AI tool does not transfer responsibility for correctness, quality, security, academic integrity, or understanding to the tool."]),
    ("cmu_17313", "Carnegie Mellon University", "17-313 Foundations of Software Engineering", "Spring 2026 (inferred)",
     "https://cmu-313.github.io/syllabus", [
         "You may use generative AI for any and all coding tasks in the course.",
         "Our goal for you in this class is that you learn to use AI in a way that helps you become a better software engineer.",
         "We Very Strongly Discourage using AI to Generate writing responses, but we encourage its use for editing your writing.",
         "It is your responsibility to validate and verify AI-produced content before submitting it for class purposes.",
         "However, outsourcing this work to AI completely bypasses the cognitive friction required to actually learn the material."]),
    ("rit_swen261", "Rochester Institute of Technology", "SWEN-261 Intro to Software Engineering", "Fall (year not stated)",
     "https://www.se.rit.edu/~swen-261/web/syllabus", [
         "CAUTIONARY: ChatGPT and other Generative AI tools are not considered to be part of the official toolkit.",
         "Unless given instruction for a specific allowed use, the only place where you may use GPT or other AI tools is for searching and/or reference",
         "Submit your prompts for GPT (as a separate file) as part of your work",
         "In other words, anything you submit must not have been created or modified by any AI means.",
         "In short - just don't do it."]),
    ("njit_cs485", "New Jersey Institute of Technology", "CS 485 AI-Assisted Software Engineering", "Spring 2026",
     "https://kelloggm.github.io/martinjkellogg.com/teaching/cs485-sp26/about", [
         "The project will involve using LLMs as part of every step of the engineering process",
         "Instead, students will be expected to use AI models to generate most of the code.",
         "I expect students will need at least one of Claude Code, Cursor, OpenAI Codex, etc.",
         "you will be required to submit the logs of all of your interactions with your AI tools.",
         "These essays must be completed without the assistance of AI tools."]),
    ("princeton_cos333", "Princeton University", "COS 333 Advanced Programming Techniques", "Fall 2026",
     "https://www.cs.princeton.edu/courses/archive/fall26/cos333/policies.html", [
         "In particular, you may use generative AI.",
         "In fact, you are required to use generative AI, at least to some minimal degree.",
         "We recommend using GitHub Copilot running in the VS Code IDE.",
         "You may not use ChatGPT or any other generative AI tool when doing the assignments.",
         "You must inform the course's instructors about the sources of information that you use."]),
    ("neu_cs4130", "Northeastern University", "CS 4130 Engineering LLM-Integrated Systems", "Fall 2025",
     "http://pages.github.khoury.northeastern.edu/4130/2025F/policies/", [
         "But, you’re not going to be able to develop that skill if you use an LLM to do all your coding for you.",
         "However, we also want you to effectively learn how to use LLMs to write code, which is a skill that you will need.",
         "To resolve this tension, we will clearly mark the parts of assignments where you may use an LLM to help write code.",
         "You should turn off Copilot, etc. for the other parts."]),
    ("cornell_cs5150", "Cornell University", "CS 5150 Software Engineering", "Spring 2026",
     "https://www.cs.cornell.edu/courses/CS5150/2026sp/syllabus.html", [
         "You may use AI tools to assist with coding, but you must clearly disclose any AI-generated content in your report",
         "You may not use AI tools for any in-class exams or in-class activities"]),
    ("tamusa_csci4316", "Texas A&M University-San Antonio", "CSCI 4316 Software Engineering I", "Fall 2026",
     "https://apps.tamusa.edu/course-information/syllabi/Fall2026/CSCI_4316SyllabusFA26.pdf", [
         "Use of artificial intelligence (AI) tools, including ChatGPT, is permitted in this course for students who wish to use them.",
         "students must cite any AI-generated material that informed their work (this includes in-text citations and/or use of quotations, and in your reference list).",
         "Using an AI tool to generate content without proper attribution qualifies as academic dishonesty"]),
]


def write_raw(id_, header, excerpts):
    path = os.path.join(ROOT, "data", "raw", id_ + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + f"\nACCESSED: {ACC}\n")
        f.write("RETRIEVAL: Claude Code WebFetch (page to text, key sentences extracted); PDFs via pypdf.\n\nEXCERPTS:\n")
        for q in excerpts:
            f.write("- " + q + "\n")


def main():
    os.makedirs(os.path.join(ROOT, "data", "raw"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "policies.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "institution", "state", "inst_type", "level", "source_title", "url", "source_date", "accessed"])
        for r in INSTITUTIONS:
            w.writerow(list(r[:8]) + [ACC])
            write_raw(r[0], f"INSTITUTION: {r[1]}\nSOURCE: {r[5]}\nURL: {r[6]}\nLEVEL: {r[4]}\nSOURCE DATE: {r[7] or 'not shown'}", r[8])
    with open(os.path.join(ROOT, "data", "se_courses.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "institution", "course", "term", "url", "accessed"])
        for r in SE_COURSES:
            w.writerow(list(r[:5]) + [ACC])
            write_raw(r[0], f"INSTITUTION: {r[1]}\nCOURSE: {r[2]}\nTERM: {r[3]}\nURL: {r[4]}\nLEVEL: course", r[5])
    print(f"{len(INSTITUTIONS)} institutions, {len(SE_COURSES)} SE courses written")


if __name__ == "__main__":
    main()
