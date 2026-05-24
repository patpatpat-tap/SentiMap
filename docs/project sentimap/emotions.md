#  How emotion tagging works (high level)

It is multi‑label: a single post can trigger multiple emotions.
Emotions are computed using two signals:
Sentiment score thresholds (for anger, frustration, trust)
Keyword matches in the text (for fear, disgust, sadness, resignation)
Sarcasm is its own emotion flag, copied directly from the sarcasm detector.
Emotion-by-emotion explanation

# Anger
Trigger: sentiment_score <= -0.75
Meaning: very strong negative sentiment; typically harsh complaints or intense rage.
Why: anger is defined as the most negative polarity.

# Frustration
Trigger: -0.75 < sentiment_score <= -0.3
Meaning: moderate negativity, common in everyday grievance language.
Why: frustration is treated as the “default” negative emotion when anger is not extreme.

# Sarcasm
Trigger: sarcasm_detected == True (from sarcasm detector)
Meaning: ironic or opposite‑meaning statements (e.g., “Hayahay kaayo traffic”).
Why: sarcasm is detected earlier in the pipeline and propagated here.

# Fear
Trigger: any of these words in the text:
danger, unsafe, accident, bangga, disgrasya, nahadlok, hadlok, mahadlok, crash, patay, namatay, nasakitan, injured, dangerous, risk, risky, baka, mapuros
Meaning: safety or accident concerns.

# Disgust
Trigger: any of these words in the text:
corrupt, corruption, abuso, kotong, hulidap, palpak, incompetent, peke, malicious, anomalya, disgusting, manggilaw, lagay, bribe, extort
Meaning: corruption, abuse, or unethical enforcement.

# Sadness
Trigger: any of these words in the text:
kapoy, hopeless, wala nay, di na, nasubo, sad, lungkot, hilak, naluha, kinda sad, dili na kaya
Meaning: fatigue, hopelessness, or emotional depletion.

# Resignation
Trigger: any of these phrases in the text:
normal na, wala nay mahimo, sanay na, ganon talaga, mao nay cebu, mao na ni, what do you expect, expected na, kanus-a pa kaha, hahayz
Meaning: giving up, acceptance that problems are “normal.”

# Trust
Trigger: sentiment_score >= 0.35 and sarcasm_detected == False
Meaning: genuine approval or positive confidence in enforcement or improvements.
Why: positive text without sarcasm is treated as trust.

# Output
It builds an emotions_list that concatenates all active emotions; if none are active, it returns "neutral".


