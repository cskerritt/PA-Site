"""
Expanded practice-area content for Purinton Analytics.

CV-grounded, plaintiff- and defense-neutral copy. Merged into build.py's
PRACTICE_AREAS / PRACTICE_ICONS / DETAILS and the build_pages titles map.

No fabricated case results, dollar figures, or success rates. Methodology is
consistent across areas (DOT, O*NET, Occupational Requirements Survey,
transferable-skills analysis, labor-market data), so the process steps and
engagement aside are shared; per-area copy covers what differs.
"""

# Shared, methodology-consistent process (his actual workflow).
_PROCESS = [
    ("Case intake & conflict check",
     "We review the referral, confirm there is no conflict, and outline scope, timeline, and fee before any work begins."),
    ("Records & medical review",
     "We analyze medical records, deposition testimony, education, and work history to establish functional capacity and restrictions."),
    ("Vocational evaluation",
     "Where appropriate, standardized vocational testing and a structured interview assess transferable skills, aptitudes, and residual capacity."),
    ("Labor-market & earning-capacity analysis",
     "Using the Dictionary of Occupational Titles, O*NET, the Occupational Requirements Survey, and current labor-market data, we identify suitable occupations and quantify pre- and post-incident earning capacity."),
    ("Report, deposition & trial testimony",
     "We deliver a clear, well-supported written opinion and provide deposition and trial testimony designed to withstand cross-examination."),
]

_ASIDE = [
    ("Role", "Vocational expert &amp; life care planner"),
    ("Engagements", "Plaintiff &amp; defense"),
    ("Deliverables", "Report, deposition &amp; trial testimony"),
    ("Service area", "United States &amp; Canada"),
]

_RELATED = [
    ("Vocational Expert Witness", "/services/vocational-expert-witness/"),
    ("Earning Capacity &amp; Wage Loss", "/services/earning-capacity-evaluation/"),
    ("Life Care Planning", "/services/life-care-planning/"),
]


def _entry(slug, nav_name, blurb, ico, title, h1, lead, overview, included, faqs, schema_name):
    path = f"/practice-areas/{slug}/"
    cfg = {
        "eyebrow": "Practice Area",
        "h1": h1,
        "lead": lead,
        "overview": overview,
        "included_title": "What we evaluate",
        "included": included,
        "aside_title": "Engagement details",
        "aside": _ASIDE,
        "process_title": "A clear, defensible process",
        "process": _PROCESS,
        "faqs": faqs,
        "related": _RELATED,
        "schema_name": schema_name,
        "path": path,
    }
    return {"path": path, "nav": nav_name, "blurb": blurb, "icon": ico, "title": title, "cfg": cfg}


_ENTRIES = [
    _entry(
        "medical-malpractice", "Medical Malpractice",
        "Post-injury employability and earning-capacity loss where negligent care caused lasting impairment.",
        "clipboard",
        "Medical Malpractice Vocational Expert | Purinton Analytics",
        "Medical malpractice vocational &amp; life care planning experts",
        "Objective vocational and life care planning opinions in medical malpractice cases - quantifying how a negligent injury affects a person's ability to work and the lifetime cost of care.",
        [
            "When negligent medical care leaves a patient with lasting physical or cognitive impairment, the vocational impact can be as significant as the medical harm. Purinton Analytics evaluates how the resulting limitations affect employability, access to the labor market, and earning capacity, and - where catastrophic injury is involved - projects the future cost of care through a life care plan.",
            "Because Jason Purinton is both a licensed counselor and a registered nurse as well as a board-certified vocational expert, he is able to connect the medical record to functional capacity and real-world labor-market data, producing opinions that are clinically grounded and defensible for plaintiff or defense counsel.",
        ],
        [
            ("Pre- and post-injury earning capacity", "How the injury changed the person's realistic access to work and wages, relative to a but-for baseline."),
            ("Functional and vocational limitations", "Translating medical restrictions into concrete vocational implications using accepted assessment methods."),
            ("Transferable-skills analysis", "Whether prior skills transfer to alternative occupations within the person's residual capacity."),
            ("Future cost of care", "Where impairment is catastrophic, a life care plan projecting required medical and non-medical services over the lifespan."),
        ],
        [
            ("How is a vocational opinion different from a medical opinion in a malpractice case?",
             "<p>A treating physician or medical expert addresses diagnosis, causation, and the standard of care. A vocational expert takes the medical restrictions as a starting point and analyzes their real-world effect on employability, access to the labor market, and earning capacity - and, in catastrophic cases, the future cost of care.</p>"),
            ("Do you evaluate both economic loss and future care?",
             "<p>Yes. We can provide a vocational and earning-capacity analysis, a life care plan projecting future care costs, or both, depending on the issues in the case.</p>"),
            ("Can you be retained by either side?",
             "<p>Yes. Purinton Analytics is retained by both plaintiff and defense counsel; the methodology and standards applied are the same regardless of who retains us.</p>"),
        ],
        "Medical Malpractice Vocational Expert Services",
    ),
    _entry(
        "motor-vehicle-trucking", "Motor Vehicle &amp; Trucking",
        "Earning-capacity and life care opinions in auto, motorcycle, and commercial-truck injury cases.",
        "route",
        "Motor Vehicle &amp; Trucking Accident Vocational Expert | Purinton Analytics",
        "Motor vehicle &amp; trucking accident vocational experts",
        "Vocational expert and life care planning opinions in motor-vehicle and commercial-truck injury cases - quantifying lost earning capacity and the future cost of care.",
        [
            "Serious motor-vehicle and commercial-truck collisions frequently produce orthopedic, spinal, and traumatic-brain injuries that change what a person can do for a living. Purinton Analytics evaluates how those injuries affect employability, transferable skills, and earning capacity, and projects future care needs where the injury is catastrophic.",
            "Commercial-trucking cases often involve additional questions about a driver's fitness for safety-sensitive duties and the wage structure of the trucking labor market. We analyze the specific occupational demands and labor-market data that apply, producing opinions suited to either plaintiff or defense counsel.",
        ],
        [
            ("Lost earning capacity", "The difference between pre- and post-collision realistic earning capacity, grounded in labor-market data."),
            ("Return-to-work and accommodation analysis", "Whether and how the injured person can return to prior work or alternative occupations within their restrictions."),
            ("Commercial-driver occupational demands", "For CMV cases, the physical and regulatory demands of safety-sensitive driving relative to residual capacity."),
            ("Life care planning", "For catastrophic injuries, a projection of lifetime medical and non-medical care and its cost."),
        ],
        [
            ("Do you handle commercial trucking as well as passenger-vehicle cases?",
             "<p>Yes. We evaluate both passenger-vehicle and commercial-motor-vehicle cases, including the specific occupational demands and labor-market characteristics of commercial driving.</p>"),
            ("How do you quantify lost earning capacity after a crash?",
             "<p>We establish a pre-injury earning-capacity baseline from work and education history, apply the documented medical restrictions to identify post-injury occupational options using the DOT, O*NET, and the Occupational Requirements Survey, and quantify the difference using current labor-market wage data.</p>"),
            ("Can a life care plan be combined with the vocational opinion?",
             "<p>Yes. In catastrophic cases we frequently provide both a vocational/earning-capacity opinion and a life care plan addressing the future cost of care.</p>"),
        ],
        "Motor Vehicle &amp; Trucking Vocational Expert Services",
    ),
    _entry(
        "premises-liability", "Premises Liability",
        "Vocational and earning-capacity analysis for slip-and-fall and unsafe-premises injuries.",
        "shield",
        "Premises Liability Vocational Expert | Purinton Analytics",
        "Premises liability vocational experts",
        "Objective vocational and earning-capacity opinions in premises-liability cases - slip-and-fall, inadequate maintenance, and other unsafe-condition injuries.",
        [
            "Premises-liability injuries - falls, struck-by events, and other unsafe-condition incidents - can produce lasting orthopedic and neurological limitations that affect a person's ability to work. Purinton Analytics evaluates how those limitations change employability and earning capacity, grounded in the medical record and accepted vocational methodology.",
            "We establish a defensible pre-incident earning-capacity baseline, identify the occupations realistically available within the person's restrictions, and quantify any wage loss, supporting plaintiff or defense counsel with the same objective standards.",
        ],
        [
            ("Pre- and post-incident earning capacity", "A but-for baseline compared against realistic post-injury occupational options."),
            ("Employability analysis", "Whether the injured person can compete for and sustain suitable employment given their restrictions."),
            ("Transferable-skills analysis", "Identification of alternative occupations consistent with the person's skills and residual capacity."),
            ("Wage-loss quantification", "The economic foundation for any vocational loss, using current labor-market data."),
        ],
        [
            ("What does a vocational expert add to a premises-liability case?",
             "<p>A vocational expert objectively connects the medical restrictions to their real-world effect on the person's ability to work and earn - turning an injury into a defensible measure of employability and earning-capacity loss.</p>"),
            ("Is an in-person evaluation required?",
             "<p>Not always. Many opinions can be developed from the records; where a vocational evaluation and interview add value, they can be conducted in person or remotely.</p>"),
            ("Do you work for plaintiffs and defendants?",
             "<p>Yes. We are retained by both sides and apply the same objective methodology in every case.</p>"),
        ],
        "Premises Liability Vocational Expert Services",
    ),
    _entry(
        "product-liability", "Product Liability",
        "Employability and earning-capacity opinions where a defective product caused lasting injury.",
        "doc",
        "Product Liability Vocational Expert | Purinton Analytics",
        "Product liability vocational experts",
        "Vocational expert and life care planning opinions in product-liability cases - quantifying how a defective-product injury affects the ability to work and the future cost of care.",
        [
            "Defective-product injuries can range from amputations and burns to traumatic-brain and spinal injuries, each with distinct vocational consequences. Purinton Analytics evaluates how the resulting impairment affects employability, transferable skills, and earning capacity, and, in catastrophic cases, projects the lifetime cost of care.",
            "Our opinions are built on accepted assessment methods and published occupational and labor-market data, so they are transparent, reproducible, and defensible for either plaintiff or defense counsel.",
        ],
        [
            ("Earning-capacity loss", "Pre- versus post-injury realistic earning capacity based on documented restrictions and labor-market data."),
            ("Functional limitation analysis", "Translating the medical record into concrete vocational implications."),
            ("Transferable-skills analysis", "Alternative occupations consistent with the person's residual capacity and prior skills."),
            ("Life care planning", "A lifetime projection of medical and non-medical care for catastrophic product injuries."),
        ],
        [
            ("How do you approach a catastrophic product injury such as an amputation?",
             "<p>We assess the functional limitations, analyze the occupations realistically available within those limitations, quantify any earning-capacity loss, and - where appropriate - prepare a life care plan projecting prosthetic, medical, and support costs over the lifespan.</p>"),
            ("Are your methods consistent regardless of who retains you?",
             "<p>Yes. The assessment methods, data sources, and standards are the same whether we are retained by plaintiff or defense counsel.</p>"),
            ("Can you testify at deposition and trial?",
             "<p>Yes. Jason Purinton personally provides deposition and trial testimony in addition to the written report.</p>"),
        ],
        "Product Liability Vocational Expert Services",
    ),
    _entry(
        "labor-railroad-fela", "Labor &amp; FELA / Railroad",
        "Wage-loss and earning-capacity analysis for railroad workers under FELA and other labor injuries.",
        "globe",
        "FELA &amp; Railroad Worker Vocational Expert | Purinton Analytics",
        "Labor, FELA &amp; railroad vocational experts",
        "Vocational expert opinions for FELA railroad-worker injuries and other labor cases - quantifying lost earning capacity within the specific demands of the work.",
        [
            "Railroad-worker injuries under the Federal Employers' Liability Act (FELA) and other labor injuries often involve physically demanding, well-compensated occupations with specific safety and physical requirements. Purinton Analytics evaluates how an injury affects the worker's ability to return to railroad or comparable employment and quantifies the resulting earning-capacity loss.",
            "We analyze the occupational demands of the worker's craft, the realistic alternatives within their restrictions, and the wage structure of the relevant labor market - producing opinions that hold up for either plaintiff or defense counsel.",
        ],
        [
            ("Earning-capacity loss", "The wage gap between pre-injury railroad or trade earnings and realistic post-injury options."),
            ("Occupational-demand analysis", "The physical and skill demands of the worker's craft relative to documented restrictions."),
            ("Return-to-work and transferable skills", "Whether the worker can return to their craft or transfer skills to comparable work."),
            ("Labor-market analysis", "Current wage and availability data for relevant occupations."),
        ],
        [
            ("Do you handle FELA railroad cases specifically?",
             "<p>Yes. We evaluate the specific occupational demands of railroad crafts and the wage structure of the relevant labor market when quantifying earning-capacity loss in FELA cases.</p>"),
            ("How is earning capacity established for a skilled trade?",
             "<p>We build a pre-injury baseline from the worker's actual craft and earnings, apply the medical restrictions to identify realistic alternative occupations, and quantify the difference using current labor-market wage data.</p>"),
            ("Can you serve as a neutral, objective expert?",
             "<p>Yes. We are retained on both sides and apply the same objective methodology and data sources regardless of who engages us.</p>"),
        ],
        "FELA &amp; Railroad Vocational Expert Services",
    ),
    _entry(
        "long-term-disability", "Long-Term Disability",
        "Independent vocational review of own-occupation and any-occupation long-term disability claims.",
        "calc",
        "Long-Term Disability Vocational Expert | Purinton Analytics",
        "Long-term disability vocational experts",
        "Independent vocational review for long-term disability matters - evaluating own-occupation and any-occupation capacity against the medical record and labor market.",
        [
            "Long-term disability disputes turn on whether a claimant can perform the material duties of their own occupation or, later in the claim, any occupation for which they are reasonably suited. Purinton Analytics provides independent vocational analysis of those questions, grounded in the medical restrictions and accepted occupational data.",
            "We define the occupation as it is performed in the national economy, compare its demands to the claimant's documented capacity, and identify whether suitable alternative occupations exist - supporting insurers, claimants, or counsel with an objective opinion.",
        ],
        [
            ("Own-occupation analysis", "Whether the claimant can perform the material duties of their occupation as performed in the national economy."),
            ("Any-occupation analysis", "Whether suitable alternative occupations exist within the claimant's residual capacity, education, and experience."),
            ("Transferable-skills analysis", "Identification of occupations consistent with the claimant's skills and restrictions."),
            ("Labor-market support", "Occupational availability and wage data underpinning the opinion."),
        ],
        [
            ("What is the difference between own-occupation and any-occupation review?",
             "<p>Own-occupation review asks whether the claimant can perform the duties of their specific occupation as it is performed in the national economy. Any-occupation review - typically applied after an initial benefit period - asks whether they can perform any occupation for which they are reasonably suited by education, training, and experience.</p>"),
            ("Do you work for insurers or claimants?",
             "<p>Both. We provide independent vocational analysis using the same methodology regardless of who retains us.</p>"),
            ("Is this the same as a Social Security disability evaluation?",
             "<p>The vocational principles overlap, but LTD policies define disability by their own terms. We analyze the claim under the applicable policy definition rather than the SSA framework.</p>"),
        ],
        "Long-Term Disability Vocational Expert Services",
    ),
    _entry(
        "social-security-disability", "Social Security Disability",
        "Vocational expert testimony and analysis under the SSA sequential evaluation and grids.",
        "users",
        "Social Security Disability Vocational Expert | Purinton Analytics",
        "Social Security disability vocational experts",
        "Vocational expert analysis and testimony in Social Security disability matters - built on direct experience in thousands of SSA disability hearings.",
        [
            "Jason Purinton serves as a forensic vocational rehabilitation expert witness for the Social Security Administration's Office of Disability Adjudication and Review, with extensive Social Security disability hearing testimony across the United States. That direct hearing experience informs a precise, framework-grounded approach to vocational issues in disability matters.",
            "We analyze residual functional capacity against the demands of past relevant work and the broader national economy, applying the SSA's sequential evaluation process, the Medical-Vocational Guidelines (the grids), and occupational data including the DOT, O*NET, and the Occupational Requirements Survey.",
        ],
        [
            ("Past relevant work analysis", "Whether the claimant can perform their past work as actually and generally performed."),
            ("Other-work analysis", "Whether jobs exist in significant numbers in the national economy within the claimant's residual functional capacity."),
            ("Transferable-skills analysis", "Skill transfer under the SSA framework and the Medical-Vocational Guidelines."),
            ("Occupational data and job numbers", "Opinions on job descriptions and numbers supported by recognized occupational sources."),
        ],
        [
            ("What Social Security hearing experience does Purinton Analytics have?",
             "<p>Jason Purinton serves as a vocational expert witness for the SSA's Office of Disability Adjudication and Review, with extensive Social Security disability hearing testimony across the United States.</p>"),
            ("Which frameworks and data do you apply?",
             "<p>The SSA sequential evaluation process and Medical-Vocational Guidelines, together with occupational data from the Dictionary of Occupational Titles, O*NET, and the Occupational Requirements Survey.</p>"),
            ("Can you assist counsel outside of hearing testimony?",
             "<p>Yes. In addition to hearing testimony, we provide vocational analysis and consultation to attorneys handling disability and related civil matters.</p>"),
        ],
        "Social Security Disability Vocational Expert Services",
    ),
    _entry(
        "wrongful-death", "Wrongful Death",
        "Lost earning capacity and household-services foundation for wrongful-death damages.",
        "scale",
        "Wrongful Death Vocational Expert | Purinton Analytics",
        "Wrongful death vocational experts",
        "Vocational foundation for wrongful-death damages - establishing the decedent's earning capacity and the value of lost household services.",
        [
            "In wrongful-death matters, the vocational expert establishes the foundation an economist needs: the decedent's pre-death earning capacity and worklife, and the nature and value of household and family services that have been lost. Purinton Analytics develops that foundation from the decedent's education, work history, and the relevant labor market.",
            "We provide objective, well-documented opinions that support - and integrate cleanly with - the economic damages model, for plaintiff or defense counsel.",
        ],
        [
            ("Earning-capacity foundation", "The decedent's realistic earning capacity based on education, work history, and labor-market data."),
            ("Worklife considerations", "Vocational factors relevant to the decedent's expected attachment to the labor force."),
            ("Lost household services", "The nature and replacement value of household and family services no longer provided."),
            ("Coordination with economic damages", "A vocational foundation structured to support the economist's calculations."),
        ],
        [
            ("What does a vocational expert provide in a wrongful-death case?",
             "<p>We establish the decedent's earning-capacity foundation and the value of lost household services - the vocational inputs an economist uses to model economic damages.</p>"),
            ("Do you work with the economist on the case?",
             "<p>Yes. Our opinions are structured to integrate with the economic damages analysis, whether we provide the vocational foundation, the economic framework, or coordinate with a retained economist.</p>"),
            ("Can you be retained by the defense?",
             "<p>Yes. We provide objective vocational opinions for both plaintiff and defense counsel.</p>"),
        ],
        "Wrongful Death Vocational Expert Services",
    ),
    _entry(
        "veterans-disability", "Veterans' Disability",
        "Vocational capacity and transferable-military-skills analysis for veterans' matters.",
        "chart",
        "Veterans' Disability Vocational Expert | Purinton Analytics",
        "Veterans' disability vocational experts",
        "Vocational evaluations for veterans - translating military experience and service-connected limitations into civilian employability and earning capacity.",
        [
            "Veterans' matters present a distinct vocational challenge: translating military training and experience into civilian occupational terms while accounting for service-connected physical and cognitive limitations. Purinton Analytics evaluates how those limitations affect a veteran's employability and earning capacity in the civilian labor market.",
            "Drawing on experience supporting transitioning service members, we analyze transferable military skills, identify civilian occupations consistent with the veteran's residual capacity, and quantify any earning-capacity loss using accepted occupational and labor-market data.",
        ],
        [
            ("Transferable military skills", "How military training and occupational specialties map to civilian occupations."),
            ("Service-connected limitation analysis", "The civilian vocational impact of documented service-connected conditions."),
            ("Civilian employability and earning capacity", "Realistic occupational options and earning capacity in the civilian labor market."),
            ("Labor-market support", "Occupational availability and wage data underpinning the opinion."),
        ],
        [
            ("How do you translate military experience into civilian terms?",
             "<p>We map military occupational specialties and training to civilian occupations using recognized occupational frameworks, then assess which of those occupations remain realistic given any service-connected limitations.</p>"),
            ("Do you account for service-connected conditions?",
             "<p>Yes. We translate documented service-connected physical and cognitive limitations into their effect on civilian employability and earning capacity.</p>"),
            ("Can you assist counsel on either side?",
             "<p>Yes. We provide objective vocational opinions using the same methodology regardless of who retains us.</p>"),
        ],
        "Veterans' Disability Vocational Expert Services",
    ),
]

# Public exports merged by build.py.
NEW_PRACTICE_AREAS = [(e["nav"], e["path"], e["blurb"]) for e in _ENTRIES]
NEW_PRACTICE_ICONS = {e["path"]: e["icon"] for e in _ENTRIES}
NEW_PRACTICE_TITLES = {e["path"]: e["title"] for e in _ENTRIES}
NEW_DETAILS = {e["path"]: e["cfg"] for e in _ENTRIES}
