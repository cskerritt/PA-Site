"""
Seed articles for the Purinton Analytics Insights section.

Factual, citable, GEO-friendly explainers grounded in vocational-expert
methodology. No fabricated case results, dollar figures, or outcomes.
Three seed articles only - this is an explainer surface, not a full content
program. Dates are passed in (not generated) to keep the build deterministic.
"""

ARTICLES = [
    {
        "slug": "what-a-vocational-expert-evaluates-in-a-personal-injury-case",
        "title": "What a Vocational Expert Evaluates in a Personal-Injury Case",
        "dek": "How an objective vocational evaluation turns medical restrictions into a defensible measure of employability and lost earning capacity.",
        "date": "2026-06-16",
        "read": "5 min read",
        "sections": [
            ("The question a vocational expert answers", [
                "In a personal-injury case, the medical experts establish diagnosis, prognosis, and physical or cognitive restrictions. A vocational expert takes those restrictions as the starting point and answers a different question: given these limitations, what can this person realistically do for a living, and how has that changed because of the injury?",
                "The answer becomes the vocational foundation for the economic damages in the case - the bridge between the medical record and a dollar figure an economist can model.",
            ]),
            ("Establishing a pre-injury baseline", [
                "The analysis begins with who the person was, vocationally, before the injury: their education, training, work history, and demonstrated skills. From that, the expert defines a realistic pre-injury earning capacity - not simply the last wage, but the range of work the person was reasonably suited to perform.",
            ]),
            ("Translating restrictions into vocational impact", [
                "Next, the documented medical restrictions are applied to the world of work. Using sources such as the Dictionary of Occupational Titles, O*NET, and the Bureau of Labor Statistics Occupational Requirements Survey, the expert identifies which occupations remain within the person's residual capacity and which are now foreclosed.",
                "A transferable-skills analysis determines whether the skills from prior work carry over to alternative occupations the person can still perform.",
            ]),
            ("Quantifying the loss", [
                "Finally, the expert compares pre- and post-injury earning capacity using current labor-market wage data, producing a defensible measure of lost earning capacity. Where the injury is catastrophic, a life care plan may also be prepared to project the future cost of care.",
                "Because the same methodology and data sources are applied regardless of who retains the expert, the resulting opinion is transparent, reproducible, and built to withstand cross-examination.",
            ]),
        ],
        "faqs": [
            ("Is a vocational evaluation the same as a medical opinion?",
             "<p>No. A medical expert addresses diagnosis and restrictions; a vocational expert analyzes the real-world effect of those restrictions on employability and earning capacity.</p>"),
            ("Does the person have to be examined in person?",
             "<p>Not always. Many opinions are developed from the records and a structured interview; a formal vocational evaluation can be conducted in person or remotely where it adds value.</p>"),
        ],
    },
    {
        "slug": "earning-capacity-vs-wage-loss",
        "title": "Earning Capacity vs. Wage Loss: How Forensic Vocational Opinions Are Built",
        "dek": "Actual wage loss and lost earning capacity are different measures. Here is what separates them and the data behind each.",
        "date": "2026-06-09",
        "read": "4 min read",
        "sections": [
            ("Two related but distinct measures", [
                "\"Wage loss\" and \"lost earning capacity\" are often used interchangeably, but they measure different things. Wage loss looks backward at actual earnings the person did not receive. Lost earning capacity looks forward at the person's reduced ability to earn - the range of work they can no longer realistically perform.",
                "A person can have little past wage loss and still have a substantial loss of earning capacity, or vice versa. Separating the two is essential to a defensible opinion.",
            ]),
            ("How earning capacity is established", [
                "Earning capacity is not the same as the last paycheck. It is the realistic range of earnings a person is capable of, given their education, training, skills, and the labor market - before and after the injury. The difference between those two capacities, properly supported, is the lost earning capacity.",
            ]),
            ("The data behind the opinion", [
                "Defensible opinions rely on recognized sources rather than assumption: the Dictionary of Occupational Titles and O*NET for occupational characteristics, the Occupational Requirements Survey for the physical and cognitive demands of work, and current Bureau of Labor Statistics wage data for earnings.",
                "Coupled with a transferable-skills analysis, these sources allow the expert to identify suitable occupations and quantify the gap in a transparent, reproducible way.",
            ]),
            ("Why the distinction matters in litigation", [
                "Courts and opposing experts scrutinize whether a vocational opinion measures the right thing. Clearly distinguishing past wage loss from prospective earning-capacity loss - and supporting each with the appropriate data - is what keeps an opinion credible under cross-examination and admissibility challenges.",
            ]),
        ],
        "faqs": [
            ("Which measure does a jury usually consider?",
             "<p>It depends on the claim and jurisdiction. Many cases involve both a past-wage-loss component and a prospective loss-of-earning-capacity component; the vocational expert supports the vocational foundation for each.</p>"),
            ("Who calculates the final dollar figure?",
             "<p>An economist typically reduces the vocational findings to present value. The vocational expert provides the earning-capacity foundation the economic model relies on.</p>"),
        ],
    },
    {
        "slug": "how-social-security-vocational-expert-testimony-works",
        "title": "How Social Security Vocational Expert Testimony Works",
        "dek": "Inside the SSA sequential evaluation, the Medical-Vocational Guidelines, and the vocational expert's role at a disability hearing.",
        "date": "2026-06-02",
        "read": "6 min read",
        "sections": [
            ("The vocational expert's role at a hearing", [
                "At a Social Security disability hearing, the administrative law judge often calls a vocational expert to provide impartial testimony about the claimant's ability to work. The expert classifies past work, identifies transferable skills, and testifies about whether jobs exist in significant numbers in the national economy that the claimant can still perform.",
                "Jason Purinton serves as a vocational expert witness for the Social Security Administration's Office of Disability Adjudication and Review and has testified extensively in such hearings.",
            ]),
            ("The sequential evaluation process", [
                "Social Security uses a five-step sequential evaluation to decide disability. The vocational expert is most involved at the final steps: whether the claimant can perform their past relevant work, and if not, whether they can adjust to other work given their residual functional capacity, age, education, and work experience.",
            ]),
            ("Past relevant work and other work", [
                "The expert first classifies the claimant's past work as it was actually and generally performed, using the Dictionary of Occupational Titles and related sources. If the claimant cannot return to past work, the expert addresses whether other occupations exist in significant numbers within the claimant's residual functional capacity.",
            ]),
            ("The Medical-Vocational Guidelines", [
                "The Medical-Vocational Guidelines - commonly called \"the grids\" - direct a finding of disabled or not disabled based on combinations of residual functional capacity, age, education, and skills. The vocational expert's testimony on skill levels and transferability informs how the grids are applied, and provides occupational evidence where the grids are used as a framework rather than a directed result.",
            ]),
        ],
        "faqs": [
            ("What Social Security hearing experience does Purinton Analytics have?",
             "<p>Jason Purinton serves as a vocational expert witness for the SSA's Office of Disability Adjudication and Review, with extensive Social Security disability hearing testimony across the United States.</p>"),
            ("Can the same principles help in civil litigation?",
             "<p>The vocational principles overlap, but civil cases apply different legal standards. We analyze each matter under the standard that governs it rather than importing the SSA framework wholesale.</p>"),
        ],
    },
]
