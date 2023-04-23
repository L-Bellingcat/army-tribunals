**Project Sentinel**  
**Uncovering systemic issues in militaries**

Try the tool here: [Sentinel web app](https://server-p7oiucccxq-uc.a.run.app/)

On April 17, 2023, an Indian soldier was arrested for killing four of his colleagues at the Bhatinda military base,
located in the state of Punjab, North India. This is one of
the [several reported cases](https://www.eurasiareview.com/27032023-the-silent-crisis-of-suicide-in-indian-armed-forces-and-hr-implications-oped/)
from the Indian army that is, according to the country’s own defense military, witnessing an alarming increase in
fratricide and suicide rates. Independent journalists and academics profess
that [poor leadership, callous attitude of senior officers, and denial of leaves](https://frontline.thehindu.com/the-nation/indian-army-armed-forces-suicide-personnel-members-high-rates-in-conflict-zones/article33770111.ece)
have pushed the force to the brink. But the Indian military, which employs more than 1.4 million active personnel, like
all defense bodies in the world, is opaque and largely self-governing. With no publicly accessible centralized database,
it is extremely challenging for journalists, activists and human rights bodies to go beyond anecdotal evidence of
systemic issues spread across news reports or individually downloadable documents. Recent reports
of [increasing violence within the forces](https://indianexpress.com/article/explained/jk-court-martial-how-armed-forces-punish-their-personnel-for-crime-8482924/), [suicide](https://www.reuters.com/world/india/stress-seen-major-cause-indian-military-fratricides-suicides-2023-04-17/), [fratricide](https://www.indiatoday.in/india-today-insight/story/why-fratricide-at-bathinda-station-puts-indian-militarys-grievance-redress-system-under-spotlight-2362434-2023-04-20), [pending cases](https://theprint.in/judiciary/armed-forces-tribunal-has-19000-pending-cases-but-heres-why-this-is-least-of-its-problems/624020/#:~:text=Cut%20to%202021%2C%20the%20tribunal,set%20up%2011%20years%20ago.),
and [shortage of judicial members](https://www.tribuneindia.com/news/nation/23-out-of-34-posts-of-armed-forces-tribunal-vacant-19-000-cases-pending-mod-tells-parliament-223283)
have underscored the murkiness surrounding impenetrable institution. Project Sentinel is an attempt to remedy that.

Powered by gpt-3.5, this tool collates and centralizes all judgments passed by all the functioning benches Armed Forces
Tribunals (AFT) in India on grievances filed by army, air force, or navy personnel or their family members against the
military since the tribunal’s inception in 2009. Upload a court case to see who else is fighting/has fought a similar
case in the same or a different tribunal. Project Sentinel will provide the top ten tribunal cases most similar to yours
along with the summaries of the cases.

We have almost all of the cases hosted on the [Indian Armed Forces Tribunal ](https://aftdelhi.nic.in/)website (we are
pulling the remainder as we write this). Our future plans are to make this project more interactive by integrating
keyword search, volunteer document labeling, document clustering, and case timeline tracking.On March 22, the Supreme
Court of India upheld
the [High Court’s authority over judicial review of AFT’s rulings](https://www.hindustantimes.com/india-news/sc-okays-judicial-review-of-armed-forces-tribunal-decisions-by-high-courts-101679496441970.html).
So, our aim is to expand our database to include these cases.

The long term goal is to expand the scope of this tool to include other armed forces in different regions and make it
available to journalists, law students, and activists.

**How we did it**

We wrote scripts to comb through all armed forces tribunal websites in India. We collected metadata of each case
assigned to a tribunal including _Case Number, Bench, Date, Dept (Army, Air Force Navy), Region, Civilian Judge,
Military Judge and the complete text of the judgment._ We then computed the embeddings (AI-friendly representations of
the text) for each of the judgements using OpenAI Embeddings API and used these embeddings to gather the top ten
documents most similar to your case. We also provide the summaries of each case beneath for a quick glance, these
summaries are computed using GPT 3.5.

Our future plans are to make this project more interactive by providing an API for this database, integrating keyword
search, volunteer document labeling, document clustering, and case timeline tracking. Currently we have only processed
data for the Chandigarh region, but plan to expand the project to cover all armed forces tribunals across India.

The web server was written in python using FastAPI and deployed on Google Cloud Run in a containerized manner.

**About the Armed Forces Tribunal, India**

Established on August 8, 2009, the armed forces tribunal is a statutory body spread across 11 locations or benches in
India. Facing a severe shortage of judicial candidates, the tribunals, currently functioning in only four benches of
three locations- Delhi (2), Chandigarh (1), Lucknow (1), have collectively more
than [19,000 pending cases](https://theprint.in/judiciary/armed-forces-tribunal-has-19000-pending-cases-but-heres-why-this-is-least-of-its-problems/624020/)
awaiting adjudication- some of them awaiting a hearing data since the inception of these tribunals.

Each tribunal is composed of

1. Judicial member- retired high court judge
2. Administrative member- retired member of armed forces or a judge advocate general

For more information on the Indian Armed Forces Tribunal, please
go [here](https://byjus.com/free-ias-prep/aft-armed-forces-tribunal/).
