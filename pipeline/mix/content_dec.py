# Dec 5, 2026 - Jan 5, 2027: 2 videos/day. A = main (IG, FB, YT, TikTok), B = second (TikTok + IG Trial Reel).
# Each entry: date, slot, slug, palette, kind, hook, vo_hook, body, punch, vo_punch, keys, meta(title, takeaway, tag)

def VS(left, right, items):
    return dict(kind='vs', left=left, right=right, items=[dict(side=s, text=t, vo=v) for s, t, v in items])
def LS(title, rows, color=None):
    return dict(kind='list', list_title=title, items=[dict(label=l, value=v, color=c, vo=vo) for l, v, c, vo in rows])
def H(b1, b2, title, twist, c1='red', c2='orange', join='vs'):
    return dict(big1=b1, big2=b2, c1=c1, c2=c2, join=join, title=title, twist=twist)
def P(*lines):
    return [dict(t=t, c=c) for t, c in lines]

E = []
def add(date, slot, slug, pal, hook, vo_hook, body, punch, vo_punch, keys, title, takeaway, tag, badge=None):
    d = dict(date=date, slot=slot, id=f'{date}-{slot}-{slug}', palette=pal, hook=hook, vo_hook=vo_hook,
             punch=punch, vo_punch=vo_punch, keys=keys, meta=dict(title=title, takeaway=takeaway, tag=tag))
    d.update(body)
    d['badge'] = badge or ('NEVER MIX UP AGAIN' if body['kind'] == 'vs' else 'MEMORIZE THIS')
    E.append(d)

# ---------------- Dec 5 ----------------
add('2026-12-05','A','electrolyte-ranges','purple',
    H('135–145','3.5–5','4 ELECTROLYTES','MEMORIZE THESE RANGES',join=''),
    '4 electrolyte ranges you have to know.',
    LS('NORMAL RANGES',[('Sodium','135–145 mEq/L','blue','Sodium: 135 to 145.'),('Potassium','3.5–5.0 mEq/L','green','Potassium: 3.5 to 5.'),
                        ('Calcium','9–10.5 mg/dL','orange','Calcium: 9 to 10.5.'),('Magnesium','1.3–2.1 mEq/L','pink','Magnesium: 1.3 to 2.1.')]),
    P(('POTASSIUM','green'),('3.5 TO 5','yellow')),'Potassium is the one that can stop the heart.',
    ['sodium','potassium','calcium','magnesium','heart.'],'4 Electrolyte Ranges to Memorize',
    'Sodium 135–145, potassium 3.5–5.0, calcium 9–10.5, magnesium 1.3–2.1. Ranges vary slightly by lab.','electrolytes')
add('2026-12-05','B','low-vs-high-sodium','teal',
    H('LOW SODIUM','HIGH SODIUM','STOP MIXING UP','LOW SODIUM, BRAIN SWELLS',c1='blue'),
    'Low sodium or high sodium? Never mix them up.',
    VS(dict(icon='↓',name='LOW Na',color='blue'),dict(icon='↑',name='HIGH Na',color='orange'),
       [('L','Brain swells','Low sodium: the brain swells.'),('L','Confusion, seizures','Confusion, seizures.'),
        ('R','Intense thirst','High sodium: intense thirst,'),('R','Dry, sticky mouth','dry, sticky mouth,'),('R','Restless, agitated','restless and agitated.')]),
    P(('LOW Na','blue'),('= SEIZURE','yellow'),('PRECAUTIONS','yellow')),'Low sodium? Think seizure precautions.',
    ['low','high','brain','seizures','thirst'],'Low vs High Sodium: Never Mix Them Up',
    'Low sodium makes the brain swell: confusion and seizures. High sodium: thirst, dry sticky mouth, restlessness.','electrolytes')
# ---------------- Dec 6 ----------------
add('2026-12-06','A','preeclampsia-vs-eclampsia','plum',
    H('PREECLAMPSIA','ECLAMPSIA','STOP MIXING UP','ECLAMPSIA = SEIZURE',c1='pink'),
    'Preeclampsia or eclampsia? One word fixes it.',
    VS(dict(icon='BP',name='PRE-',color='pink'),dict(icon='⚡',name='ECLAMPSIA',color='orange'),
       [('L','BP 140/90+','Preeclampsia: blood pressure 140 over 90 or higher,'),('L','After 20 weeks','after 20 weeks,'),('L','Protein or organ signs','with protein or organ signs.'),
        ('R','= SEIZURE','Eclampsia: add a seizure.'),('R','Magnesium sulfate','Magnesium sulfate prevents and treats it.')]),
    P(('ECLAMPSIA','orange'),('= SEIZURE','yellow')),'Eclampsia means seizure.',
    ['seizure.','magnesium','20','protein'],'Preeclampsia vs Eclampsia in 15 Seconds',
    'Preeclampsia: BP 140/90 or higher after 20 weeks with protein or organ signs. Eclampsia = a seizure. Magnesium sulfate prevents and treats it.','maternity')
add('2026-12-06','B','apgar','plum',
    H('A P G A R','7–10','NEWBORN SCORE','5 SIGNS, 1 AND 5 MINUTES',c1='yellow',c2='green',join=''),
    'APGAR in 15 seconds.',
    LS('APGAR = 5 SIGNS',[('A  Appearance','color','pink','Appearance: color.'),('P  Pulse','heart rate','red','Pulse: heart rate.'),
                          ('G  Grimace','reflex','orange','Grimace: reflex irritability.'),('A  Activity','muscle tone','green','Activity: muscle tone.'),
                          ('R  Respiration','breathing','cyan','Respiration: breathing effort.')]),
    P(('1 AND 5 MIN','cyan'),('7–10 = NORMAL','green')),'Scored at 1 and 5 minutes. 7 to 10 is normal.',
    ['appearance:','pulse:','grimace:','activity:','respiration:'],'APGAR Score in 15 Seconds',
    'Appearance, Pulse, Grimace, Activity, Respiration. Scored at 1 and 5 minutes; 7–10 is reassuring.','maternity')
# ---------------- Dec 7 ----------------
add('2026-12-07','A','delirium-vs-dementia','navy',
    H('DELIRIUM','DEMENTIA','STOP MIXING UP','DELIRIUM IS SUDDEN',c1='orange',c2='blue'),
    'Delirium or dementia? Never mix them up.',
    VS(dict(icon='⚡',name='DELIRIUM',color='orange'),dict(icon='🕐',name='DEMENTIA',color='blue'),
       [('L','Sudden onset','Delirium: sudden onset,'),('L','Fluctuates','comes and goes,'),('L','Often reversible','often reversible.'),
        ('R','Slow, gradual','Dementia: slow and gradual,'),('R','Progressive','progressive,'),('R','Not reversible','not reversible.')]),
    P(('SUDDEN','orange'),('= DELIRIUM','yellow')),'Sudden confusion? Think delirium and find the cause.',
    ['sudden','gradual','reversible.','delirium','dementia'],'Delirium vs Dementia: Never Mix Them Up',
    'Delirium is sudden, fluctuates and is often reversible. Dementia is gradual, progressive and not reversible.','mentalhealth')
add('2026-12-07','B','dystonia-vs-tardive','navy',
    H('DYSTONIA','TARDIVE','STOP MIXING UP','TARDIVE = TARDY (LATE)',c1='pink',c2='cyan'),
    'Acute dystonia or tardive dyskinesia?',
    VS(dict(icon='⏱',name='DYSTONIA',color='pink'),dict(icon='⌛',name='TARDIVE',color='cyan'),
       [('L','Early: hours–days','Acute dystonia: early, hours to days.'),('L','Muscle spasms','Painful muscle spasms.'),('L','Benztropine','Treat with benztropine or diphenhydramine.'),
        ('R','Late: months–years','Tardive: late, months to years.'),('R','Lip smacking','Lip smacking, tongue movements.'),('R','May be permanent','May be permanent.')]),
    P(('TARDIVE','cyan'),('= TARDY','yellow')),'Tardive means tardy. It shows up late.',
    ['early,','late,','tardive','tardy.'],'Acute Dystonia vs Tardive Dyskinesia',
    'Antipsychotic side effects: acute dystonia comes early (hours to days); tardive dyskinesia comes late (months to years) and may be permanent.','psych')
# ---------------- Dec 8 ----------------
add('2026-12-08','A','insulin-onset','purple',
    H('15 MIN','NO PEAK','4 INSULINS','KNOW THE ONSET',c1='green',c2='cyan',join='or'),
    '4 insulins. Know when they kick in.',
    LS('ONSET',[('Lispro (rapid)','~15 min','green','Lispro: about 15 minutes.'),('Regular (short)','30–60 min','blue','Regular: 30 to 60 minutes.'),
                ('NPH','1–2 hr','orange','N P H: 1 to 2 hours.'),('Glargine','no peak','pink','Glargine: long acting, no peak.')]),
    P(('GLARGINE','pink'),('HAS NO PEAK','yellow')),'Glargine has no peak.',
    ['lispro:','regular:','glargine:','peak.','15'],'Insulin Onset: Lispro, Regular, NPH, Glargine',
    'Lispro ~15 min, regular 30–60 min, NPH 1–2 hr (peaks 4–12 hr), glargine has no peak. Times vary by source.','insulin')
add('2026-12-08','B','glucagon-vs-d50','purple',
    H('GLUCAGON','D50','UNCONSCIOUS + LOW SUGAR','NO IV? GLUCAGON',c1='orange',c2='cyan'),
    'Unconscious and low blood sugar. Glucagon or D50?',
    VS(dict(icon='💉',name='GLUCAGON',color='orange'),dict(icon='IV',name='D50',color='cyan'),
       [('L','No IV access','Glucagon: no I V access.'),('L','IM or subcut','Give it I M or subcut.'),
        ('R','IV access','D 50: when there is I V access.'),('R','Works fast','Works fast.')]),
    P(('NO IV?','orange'),('GLUCAGON','yellow')),'No I V? Give glucagon.',
    ['glucagon:','iv','im','subcut.'],'Glucagon or D50? Unconscious Hypoglycemia',
    'Unconscious with low glucose: no IV access, give glucagon IM or subcut; with IV access, give dextrose 50% IV per protocol.','diabetes')
# ---------------- Dec 9 ----------------
add('2026-12-09','A','angina-vs-mi','teal',
    H('ANGINA','MI','CHEST PAIN','NITRO DIDN\'T FIX IT?',c1='orange',c2='red'),
    'Chest pain. Angina or heart attack?',
    VS(dict(icon='♥',name='ANGINA',color='orange'),dict(icon='♥',name='MI',color='red'),
       [('L','With exertion','Stable angina: comes with exertion,'),('L','Rest or nitro helps','relieved by rest or nitro.'),
        ('R','Not relieved','M I: not relieved by rest or nitro.'),('R','Troponin rises','Troponin rises.')]),
    P(('NITRO DIDN\'T','red'),('FIX IT?','red'),('THINK MI','yellow')),'Nitro didn\'t fix it? Think M I.',
    ['nitro.','troponin','exertion,','rest'],'Angina vs MI: Nitro Is the Clue',
    'Stable angina is relieved by rest or nitroglycerin. MI pain is not, and troponin rises.','cardiac')
add('2026-12-09','B','shock-or-no-shock','teal',
    H('SHOCK','NO SHOCK','3 RHYTHMS','FLAT LINE? DON\'T SHOCK',c1='yellow',c2='blue',join='or'),
    '3 rhythms. Shock or no shock?',
    LS('DEFIBRILLATE?',[('V-fib','SHOCK','yellow','V fib: shock.'),('Pulseless V-tach','SHOCK','yellow','Pulseless V tach: shock.'),
                        ('Asystole','NO: CPR + epi','blue','Asystole: no shock. C P R and epinephrine.')]),
    P(('FLAT LINE?','blue'),('DON\'T SHOCK','yellow')),'Flat line? Don\'t shock.',
    ['shock.','asystole:','cpr'],'Shock or No Shock? 3 Rhythms',
    'V-fib and pulseless V-tach are shockable. Asystole is not: CPR and epinephrine.','cardiac')
# ---------------- Dec 10 ----------------
add('2026-12-10','A','hepatitis-a-vs-b','teal',
    H('HEP A','HEP B','STOP MIXING UP','VOWELS = BOWELS',c1='green',c2='red'),
    'Hepatitis A or B? Vowels and bowels.',
    VS(dict(icon='A',name='HEP A',color='green'),dict(icon='B',name='HEP B',color='red'),
       [('L','Fecal–oral','Hep A: fecal oral,'),('L','Food and water','contaminated food and water.'),
        ('R','Blood','Hep B: blood,'),('R','Sex, needles, birth','sex, needles, and birth.')]),
    P(('A AND E','green'),('VOWELS = BOWELS','yellow')),'A and E are vowels, from the bowels.',
    ['fecal','blood,','vowels','bowels.'],'Hepatitis A vs B: Vowels From the Bowels',
    'Hepatitis A (and E) spread fecal-oral: "vowels from the bowels." Hepatitis B spreads through blood, sex, needles and birth.','infectioncontrol')
add('2026-12-10','B','iron-vs-b12','purple',
    H('IRON','B12','ANEMIA','PERNICIOUS? SHOTS FOR LIFE',c1='red',c2='pink'),
    'Iron deficiency or B12? Two clues.',
    VS(dict(icon='Fe',name='IRON',color='red'),dict(icon='B12',name='PERNICIOUS',color='pink'),
       [('L','Fatigue, pallor','Iron deficiency: fatigue, pallor,'),('L','Spoon nails, pica','spoon nails, cravings for ice.'),
        ('R','Beefy red tongue','Pernicious anemia: beefy red tongue,'),('R','Numb, tingling','numbness and tingling,'),('R','B12 shots for life','B 12 injections for life.')]),
    P(('PERNICIOUS?','pink'),('B12 FOR LIFE','yellow')),'Pernicious? B 12 for life.',
    ['tongue,','tingling,','ice.','life.'],'Iron Deficiency vs Pernicious Anemia',
    'Iron deficiency: fatigue, pallor, spoon nails, pica. Pernicious anemia: beefy red tongue, numbness/tingling, lifelong B12 replacement.','pharmacology')
# ---------------- Dec 11 ----------------
add('2026-12-11','A','peak-vs-trough','purple',
    H('PEAK','TROUGH','DRUG LEVELS','TROUGH = RIGHT BEFORE',c1='orange',c2='cyan'),
    'Peak or trough? When do you draw it?',
    VS(dict(icon='▲',name='PEAK',color='orange'),dict(icon='▼',name='TROUGH',color='cyan'),
       [('L','Highest level','Peak: the highest level,'),('L','After the dose','drawn after the dose.'),
        ('R','Lowest level','Trough: the lowest level,'),('R','Right before next dose','drawn right before the next dose.')]),
    P(('TROUGH','cyan'),('= RIGHT BEFORE','yellow')),'Trough means right before.',
    ['highest','lowest','before','after'],'Peak vs Trough: When to Draw',
    'Peak = highest level, drawn after the dose. Trough = lowest level, drawn right before the next dose. Follow your facility timing.','pharmacology')
add('2026-12-11','B','ace-vs-arb','purple',
    H('-PRIL','-SARTAN','STOP MIXING UP','PRIL = COUGH',c1='orange',c2='green'),
    'Lisinopril or losartan? One side effect.',
    VS(dict(icon='-pril',name='ACE',color='orange'),dict(icon='-sartan',name='ARB',color='green'),
       [('L','Dry cough','ACE inhibitors: dry cough,'),('L','High K+, angioedema','high potassium, angioedema.'),
        ('R','Less cough','A R Bs: much less cough.'),('R','Still watch K+','Still watch potassium.')]),
    P(('-PRIL','orange'),('= COUGH','yellow')),'Pril means cough.',
    ['cough,','potassium,','pril','cough.'],'ACE Inhibitor vs ARB: The Cough Clue',
    'ACE inhibitors (-pril) cause a dry cough, high potassium and angioedema. ARBs (-sartan) cause much less cough; still watch potassium.','pharmacology')
# ---------------- Dec 12 ----------------
add('2026-12-12','A','compartment-6ps','teal',
    H('6 Ps','PAIN FIRST','COMPARTMENT SYNDROME','PULSELESS IS LATE',c1='red',c2='orange',join=''),
    'Compartment syndrome. The 6 Ps.',
    LS('6 Ps',[('Pain','out of proportion','red','Pain out of proportion. The earliest sign.'),('Pressure','tight, firm','orange','Pressure.'),
               ('Paresthesia','tingling','yellow','Paresthesia.'),('Pallor','pale','cyan','Pallor.'),('Paralysis','late','blue','Paralysis.'),('Pulselessness','very late','pink','Pulselessness, very late.')]),
    P(('PAIN FIRST','red'),('PULSE LAST','yellow')),'Pain first. Pulse last.',
    ['pain','earliest','late.','pulselessness,'],'Compartment Syndrome: The 6 Ps',
    'Pain out of proportion is the earliest sign; pulselessness is very late. Report it right away.','medsurg')
add('2026-12-12','B','oa-vs-ra','teal',
    H('OA','RA','ARTHRITIS','RA IS SYMMETRIC',c1='orange',c2='pink'),
    'Osteoarthritis or rheumatoid? Two clues.',
    VS(dict(icon='OA',name='OSTEO',color='orange'),dict(icon='RA',name='RHEUMATOID',color='pink'),
       [('L','Wear and tear','Osteo: wear and tear,'),('L','Worse with activity','worse with activity,'),('L','Stiff < 30 min','morning stiffness under 30 minutes.'),
        ('R','Autoimmune','Rheumatoid: autoimmune,'),('R','Symmetric joints','symmetric joints,'),('R','Stiff > 1 hour','stiffness over an hour.')]),
    P(('RA','pink'),('= SYMMETRIC','yellow')),'R A is symmetric.',
    ['symmetric','autoimmune,','activity,'],'Osteoarthritis vs Rheumatoid Arthritis',
    'OA: wear and tear, worse with activity, short morning stiffness. RA: autoimmune, symmetric, morning stiffness over an hour.','medsurg')
# ---------------- Dec 13 ----------------
add('2026-12-13','A','veal-chop','plum',
    H('VEAL','CHOP','FETAL DECELS','LATE = PLACENTA',c1='orange',c2='cyan',join=''),
    'Fetal heart decels. Just remember VEAL CHOP.',
    LS('VEAL CHOP',[('Variable','Cord compression','orange','Variable: cord compression.'),('Early','Head compression','green','Early: head compression.'),
                    ('Accelerations','OK!','cyan','Accelerations: okay.'),('Late','Placenta problem','red','Late: placental insufficiency.')]),
    P(('LATE','red'),('= PLACENTA','yellow')),'Late means placenta. Act fast.',
    ['variable:','early:','accelerations:','late:','placenta.'],'VEAL CHOP: Fetal Decels Made Easy',
    'Variable = cord compression, Early = head compression, Accelerations = OK, Late = placental insufficiency.','maternity')
add('2026-12-13','B','pyloric-vs-intussusception','plum',
    H('OLIVE','SAUSAGE','BABY GI','STOP MIXING UP',c1='green',c2='orange'),
    'Olive or sausage? Two baby GI emergencies.',
    VS(dict(icon='🫒',name='PYLORIC',color='green'),dict(icon='🌭',name='INTUSSUS.',color='orange'),
       [('L','Projectile vomiting','Pyloric stenosis: projectile vomiting,'),('L','Olive-shaped mass','olive shaped mass.'),
        ('R','Currant jelly stool','Intussusception: currant jelly stool,'),('R','Sausage-shaped mass','sausage shaped mass.')]),
    P(('OLIVE','green'),('VS SAUSAGE','orange')),'Olive or sausage. Now you won\'t forget.',
    ['projectile','olive','currant','sausage'],'Pyloric Stenosis vs Intussusception',
    'Pyloric stenosis: projectile vomiting, olive-shaped mass. Intussusception: currant jelly stools, sausage-shaped mass.','peds')
# ---------------- Dec 14 ----------------
add('2026-12-14','A','ssri-teaching','navy',
    H('2–6','WEEKS','SSRIs','WHAT TO TEACH',c1='cyan',c2='yellow',join=''),
    'Starting an SSRI? 4 things to teach.',
    LS('SSRI TEACHING',[('Full effect','2–6 weeks','cyan','Full effect takes 2 to 6 weeks.'),('Under 25','watch mood early','orange','Under 25: watch for worsening mood early.'),
                        ('Serotonin syndrome','shaky, hot','pink','Watch for serotonin syndrome.'),('Stopping','taper, never quit','green','Never stop suddenly. Taper.')]),
    P(('2–6 WEEKS','cyan'),('BE PATIENT','yellow')),'2 to 6 weeks. Keep taking it.',
    ['2','6','weeks.','taper.'],'SSRI Teaching: 4 Must-Knows',
    'SSRIs take 2–6 weeks for full effect, need close mood monitoring early in young adults, can cause serotonin syndrome, and should be tapered.','psych')
add('2026-12-14','B','alcohol-withdrawal-timeline','navy',
    H('6 HRS','2–4 DAYS','ALCOHOL WITHDRAWAL','DTs COME LATER',c1='orange',c2='red',join='to'),
    'Alcohol withdrawal timeline.',
    LS('LAST DRINK +',[('Tremors, anxiety','6–12 hr','orange','Tremors and anxiety: 6 to 12 hours.'),('Seizures','12–48 hr','pink','Seizures: 12 to 48 hours.'),
                       ('Delirium tremens','48–96 hr','red','Delirium tremens: 2 to 4 days.')]),
    P(('DTs','red'),('2–4 DAYS','yellow')),'The D Ts come at 2 to 4 days.',
    ['tremors','seizures:','delirium','days.'],'Alcohol Withdrawal Timeline',
    'Tremors 6–12 hr, seizures 12–48 hr, delirium tremens around 48–96 hr after the last drink.','psych')
# ---------------- Dec 15 ----------------
add('2026-12-15','A','sepsis-vs-septic-shock','teal',
    H('SEPSIS','SEPTIC SHOCK','STOP MIXING UP','NEEDS PRESSORS = SHOCK',c1='orange',c2='red'),
    'Sepsis or septic shock? One clue.',
    VS(dict(icon='🦠',name='SEPSIS',color='orange'),dict(icon='⚠',name='SEPTIC SHOCK',color='red'),
       [('L','Infection','Sepsis: infection'),('L','+ organ dysfunction','plus organ dysfunction.'),
        ('R','Low BP after fluids','Septic shock: low pressure even after fluids,'),('R','Needs pressors','needs vasopressors for a MAP of 65,'),('R','Lactate > 2','lactate over 2.')]),
    P(('NEEDS PRESSORS','red'),('= SHOCK','yellow')),'Needs pressors? That\'s septic shock.',
    ['organ','fluids,','vasopressors','65,','lactate'],'Sepsis vs Septic Shock',
    'Sepsis: infection with organ dysfunction. Septic shock: needs vasopressors to keep MAP 65 or higher and lactate over 2 despite fluids.','sepsis')
add('2026-12-15','B','tb-skin-test','teal',
    H('48–72','HOURS','TB SKIN TEST','READ IT IN TIME',c1='cyan',c2='yellow',join=''),
    'TB skin test. When is it positive?',
    LS('POSITIVE IF',[('HIV / immunosuppressed','≥ 5 mm','pink','5 millimeters for H I V or immunosuppressed.'),('Healthcare workers','≥ 10 mm','orange','10 millimeters for healthcare workers.'),
                      ('No risk factors','≥ 15 mm','green','15 for no risk factors.'),('Read at','48–72 hr','cyan','Read it at 48 to 72 hours.')]),
    P(('MEASURE','cyan'),('INDURATION','yellow'),('NOT REDNESS','red')),'Measure the hard bump, not the redness.',
    ['5','10','15','48','72'],'TB Skin Test: 5, 10, 15',
    'Read at 48–72 hours. Positive: 5 mm (HIV/immunosuppressed), 10 mm (healthcare workers), 15 mm (no risk factors). Measure induration, not redness.','infectioncontrol')
# ---------------- Dec 16 ----------------
add('2026-12-16','A','abg-normals','purple',
    H('7.35','7.45','ABG NORMALS','4 NUMBERS TO KNOW',c1='cyan',c2='green',join='to'),
    '4 ABG numbers you have to know.',
    LS('NORMAL ABG',[('pH','7.35–7.45','cyan','P H: 7.35 to 7.45.'),('PaCO2','35–45 mm Hg','orange','C O 2: 35 to 45.'),
                     ('HCO3','22–26 mEq/L','green','Bicarb: 22 to 26.'),('PaO2','80–100 mm Hg','pink','P O 2: 80 to 100.')]),
    P(('CO2 35–45','orange'),('BICARB 22–26','green')),'C O 2, 35 to 45. Bicarb, 22 to 26.',
    ['ph:','bicarb:'],'ABG Normal Values in 15 Seconds',
    'pH 7.35–7.45, PaCO2 35–45, HCO3 22–26, PaO2 80–100.','abgs')
add('2026-12-16','B','left-vs-right-stroke','navy',
    H('LEFT BRAIN','RIGHT BRAIN','STROKE','RIGHT BRAIN = RISKY',c1='blue',c2='orange'),
    'Left brain or right brain stroke?',
    VS(dict(icon='L',name='LEFT',color='blue'),dict(icon='R',name='RIGHT',color='orange'),
       [('L','Aphasia','Left brain: trouble speaking,'),('L','Right-side weakness','right side weakness,'),('L','Slow, cautious','slow and cautious.'),
        ('R','Left neglect','Right brain: ignores the left side,'),('R','Impulsive','impulsive,'),('R','Poor judgment','poor judgment.')]),
    P(('RIGHT BRAIN','orange'),('= RISKY','yellow'),('FALL RISK','red')),'Right brain is risky. Big fall risk.',
    ['speaking,','impulsive,','neglect','risky.'],'Left vs Right Brain Stroke',
    'Left-brain stroke: aphasia, right-sided weakness, slow and cautious. Right-brain stroke: left neglect, impulsive, poor judgment, high fall risk.','stroke')
# ---------------- Dec 17 ----------------
add('2026-12-17','A','heat-exhaustion-vs-stroke','teal',
    H('EXHAUSTION','HEAT STROKE','STOP MIXING UP','CONFUSED = HEAT STROKE',c1='orange',c2='red'),
    'Heat exhaustion or heat stroke?',
    VS(dict(icon='💧',name='EXHAUSTION',color='orange'),dict(icon='🔥',name='HEAT STROKE',color='red'),
       [('L','Heavy sweating','Exhaustion: heavy sweating,'),('L','Mind is clear','mind is clear.'),
        ('R','Temp > 104°F (40°C)','Heat stroke: temperature over 104,'),('R','Confused','confused,'),('R','Emergency','an emergency.')]),
    P(('CONFUSED?','red'),('HEAT STROKE','yellow')),'Confused and hot? Heat stroke. Cool them now.',
    ['sweating,','104,','confused,','emergency.'],'Heat Exhaustion vs Heat Stroke',
    'Heat exhaustion: heavy sweating, normal mental status. Heat stroke: core temp over 104°F (40°C) with confusion; a medical emergency.','medsurg')
add('2026-12-17','B','transfusion-musts','purple',
    H('2 RNs','NS ONLY','BLOOD TRANSFUSION','5 MUST-KNOWS',c1='red',c2='cyan',join='+'),
    'Blood transfusion. 5 must-knows.',
    LS('BEFORE + DURING',[('Verify','2 RNs, bedside','orange','Two R Ns verify at the bedside.'),('Fluid','normal saline only','cyan','Normal saline only.'),
                          ('Start','within 30 min','green','Start within 30 minutes of pickup.'),('Stay','first 15 min','pink','Stay for the first 15 minutes.'),('Finish','within 4 hr','yellow','Finish within 4 hours.')]),
    P(('NORMAL SALINE','cyan'),('ONLY','yellow')),'Normal saline only. Never dextrose.',
    ['saline','30','15','4'],'Blood Transfusion: 5 Must-Knows',
    'Two RNs verify, normal saline only, start within 30 minutes, stay the first 15 minutes, finish within 4 hours. Follow facility policy.','medsurg')
# ---------------- Dec 18 ----------------
add('2026-12-18','A','urine-colors','purple',
    H('ORANGE','BROWN','URINE COLOR','WHICH DRUG?',c1='orange',c2=[170,110,60],join='or'),
    'Orange or brown urine? Which drug did it?',
    LS('URINE COLOR',[('Phenazopyridine','orange','orange','Phenazopyridine: orange.'),('Rifampin','orange-red','red','Rifampin: orange red.'),
                      ('Nitrofurantoin','brown','yellow','Nitrofurantoin: brown.'),('Metronidazole','dark red-brown','pink','Metronidazole: dark red brown.')]),
    P(('EXPECTED','green'),('TEACH IT FIRST','yellow')),'Expected. Teach it so they don\'t panic.',
    ['orange.','brown.','expected.'],'Which Drug Changes Urine Color?',
    'Phenazopyridine and rifampin turn urine orange; nitrofurantoin can turn it brown; metronidazole dark red-brown. Teach clients ahead of time.','pharmacology')
add('2026-12-18','B','gentamicin','purple',
    H('EARS','KIDNEYS','GENTAMICIN','PROTECT BOTH',c1='cyan',c2='orange',join='+'),
    'Gentamicin. Protect two organs.',
    VS(dict(icon='👂',name='EARS',color='cyan'),dict(icon='🫘',name='KIDNEYS',color='orange'),
       [('L','Ringing, hearing loss','Ears: ringing, hearing loss.'),('L','Report right away','Report right away.'),
        ('R','Watch creatinine','Kidneys: watch creatinine'),('R','and urine output','and urine output.')]),
    P(('PEAK + TROUGH','cyan'),('CHECK LEVELS','yellow')),'Check peak and trough levels.',
    ['ringing,','creatinine','peak','trough'],'Gentamicin: Ears and Kidneys',
    'Aminoglycosides like gentamicin are ototoxic and nephrotoxic: watch hearing, creatinine and urine output, and monitor peak/trough levels.','pharmacology')
# ---------------- Dec 19 ----------------
add('2026-12-19','A','cholecystitis-vs-pancreatitis','teal',
    H('GALLBLADDER','PANCREAS','STOP MIXING UP','BACK PAIN + LIPASE = PANCREAS',c1='green',c2='orange'),
    'Gallbladder or pancreas? Follow the pain.',
    VS(dict(icon='RUQ',name='GALLBLADDER',color='green'),dict(icon='⬅',name='PANCREAS',color='orange'),
       [('L','RUQ pain','Gallbladder: right upper quadrant pain,'),('L','After fatty meals','after fatty meals,'),('L','Murphy\'s sign','Murphy\'s sign.'),
        ('R','Epigastric to back','Pancreatitis: epigastric pain to the back,'),('R','High lipase','high lipase.')]),
    P(('BACK PAIN','orange'),('+ LIPASE','orange'),('= PANCREAS','yellow')),'Back pain plus lipase means pancreas.',
    ['fatty','murphy\'s','back,','lipase.'],'Cholecystitis vs Pancreatitis',
    'Cholecystitis: RUQ pain after fatty meals, Murphy\'s sign. Pancreatitis: epigastric pain radiating to the back, elevated lipase.','medsurg')
add('2026-12-19','B','hip-precautions','teal',
    H('90°','DON\'T CROSS','HIP REPLACEMENT','3 RULES',c1='orange',c2='red',join=''),
    'Hip replacement. 3 rules.',
    LS('POSTERIOR HIP',[('Bend','no past 90°','orange','Don\'t bend past 90 degrees.'),('Legs','don\'t cross','red','Don\'t cross the legs.'),
                        ('Turn','no inward rotation','pink','No turning the leg inward.'),('Pillow','between knees','green','Keep a pillow between the knees.')]),
    P(('NO 90°','orange'),('NO CROSSING','red')),'Nothing past 90. No crossing.',
    ['90','cross','pillow'],'Hip Replacement Precautions',
    'After a posterior hip replacement: no flexion past 90 degrees, no crossing legs, no internal rotation, abduction pillow. Follow surgeon orders.','medsurg')
# ---------------- Dec 20 ----------------
add('2026-12-20','A','baby-milestones','plum',
    H('6 MO','12 MO','BABY MILESTONES','SIT AT 6, WALK AT 12',c1='cyan',c2='green',join='to'),
    'Baby milestones in 15 seconds.',
    LS('ABOUT WHEN',[('Rolls over','4–6 mo','pink','Rolls over: 4 to 6 months.'),('Sits alone','6–8 mo','cyan','Sits alone: 6 to 8 months.'),
                     ('Pulls to stand','9–10 mo','orange','Pulls to stand: 9 to 10 months.'),('Walks','~12 mo','green','Walks: about 12 months.')]),
    P(('SIT AT 6','cyan'),('WALK AT 12','green')),'Sit at 6. Walk at 12.',
    ['rolls','sits','walks:','months.'],'Baby Milestones: Sit at 6, Walk at 12',
    'Rolls 4–6 months, sits alone 6–8 months, pulls to stand 9–10 months, walks about 12 months. Ranges vary.','peds')
add('2026-12-20','B','true-vs-false-labor','plum',
    H('TRUE','FALSE','LABOR','CERVIX CHANGES = TRUE',c1='green',c2='blue'),
    'True labor or false labor?',
    VS(dict(icon='✓',name='TRUE',color='green'),dict(icon='✕',name='FALSE',color='blue'),
       [('L','Regular, stronger','True: regular and getting stronger,'),('L','Walking makes it worse','walking makes it stronger,'),('L','Cervix changes','the cervix changes.'),
        ('R','Irregular','False: irregular,'),('R','Eases with rest','eases with rest,'),('R','No cervix change','no cervical change.')]),
    P(('CERVIX CHANGES','green'),('= TRUE LABOR','yellow')),'Cervix changes? That\'s true labor.',
    ['regular','irregular,','cervix','true'],'True vs False Labor',
    'True labor: regular, intensifying contractions that strengthen with walking, with cervical change. False labor: irregular, eases with rest, no cervical change.','maternity')
# ---------------- Dec 21 ----------------
add('2026-12-21','A','projection-vs-displacement','navy',
    H('PROJECTION','DISPLACEMENT','DEFENSE MECHANISMS','DISPLACEMENT KICKS THE DOG',c1='pink',c2='orange'),
    'Projection or displacement?',
    VS(dict(icon='➜',name='PROJECTION',color='pink'),dict(icon='🐕',name='DISPLACE',color='orange'),
       [('L','Blames others for','Projection: blames others'),('L','your own feelings','for your own feelings.'),
        ('R','Takes it out on','Displacement: takes feelings out'),('R','a safer target','on a safer target.')]),
    P(('DISPLACEMENT','orange'),('KICKS THE DOG','yellow')),'Mad at the boss, kicks the dog. Displacement.',
    ['blames','safer','dog.'],'Projection vs Displacement',
    'Projection: attributing your own feelings to someone else. Displacement: redirecting feelings to a safer target (mad at the boss, kicks the dog).','psych')
add('2026-12-21','B','clozapine-vs-haloperidol','navy',
    H('CLOZAPINE','HALOPERIDOL','ANTIPSYCHOTICS','CLOZAPINE = CHECK ANC',c1='cyan',c2='orange'),
    'Clozapine or haloperidol? Know the big risk.',
    VS(dict(icon='🩸',name='CLOZAPINE',color='cyan'),dict(icon='🧠',name='HALOPERIDOL',color='orange'),
       [('L','Low white cells','Clozapine: dangerously low white cells.'),('L','Check ANC','Check the A N C.'),
        ('R','EPS','Haloperidol: E P S,'),('R','Stiffness, tremor','stiffness and tremor.')]),
    P(('CLOZAPINE','cyan'),('= CHECK ANC','yellow')),'Clozapine? Check the A N C.',
    ['white','anc.','eps,'],'Clozapine vs Haloperidol',
    'Clozapine can cause severe neutropenia (agranulocytosis): monitor ANC. Haloperidol (typical) commonly causes extrapyramidal symptoms.','psych')
# ---------------- Dec 22 ----------------
add('2026-12-22','A','sterile-field-rules','teal',
    H('1 INCH','WAIST','STERILE FIELD','4 RULES',c1='cyan',c2='orange',join='+'),
    'Sterile field. 4 rules.',
    LS('STERILE FIELD',[('Border','1 inch is not sterile','cyan','The 1 inch border is not sterile.'),('Height','below waist = dirty','orange','Below the waist is not sterile.'),
                        ('Back','never turn it','pink','Never turn your back on it.'),('Doubt','throw it out','green','In doubt? Throw it out.')]),
    P(('IF IN DOUBT','orange'),('THROW IT OUT','yellow')),'If in doubt, throw it out.',
    ['1','waist','back','doubt?'],'Sterile Field: 4 Rules',
    'The 1-inch border is not sterile, anything below the waist is not sterile, never turn your back on the field, and if in doubt, throw it out.','infectioncontrol')
add('2026-12-22','B','zoster-isolation','teal',
    H('LOCALIZED','SPREAD OUT','SHINGLES','SPREAD OUT = AIRBORNE',c1='green',c2='red'),
    'Shingles. Which precautions?',
    VS(dict(icon='•',name='LOCALIZED',color='green'),dict(icon='⁂',name='DISSEMINATED',color='red'),
       [('L','Healthy client','Localized, healthy client:'),('L','Standard, cover it','standard precautions, cover the rash.'),
        ('R','Or immunocompromised','Disseminated or immunocompromised:'),('R','Airborne + contact','airborne plus contact.')]),
    P(('SPREAD OUT?','red'),('AIRBORNE','yellow'),('+ CONTACT','yellow')),'Spread out? Airborne plus contact.',
    ['standard','airborne','contact.'],'Shingles Isolation: Localized vs Disseminated',
    'Localized zoster in an immunocompetent client: standard precautions, cover lesions. Disseminated or immunocompromised: airborne + contact.','infectioncontrol')
# ---------------- Dec 23 ----------------
add('2026-12-23','A','actual-vs-potential','teal',
    H('ACTUAL','POTENTIAL','WHO GOES FIRST?','ACTUAL BEATS POTENTIAL',c1='red',c2='blue'),
    'Actual or potential problem. Who goes first?',
    VS(dict(icon='!',name='ACTUAL',color='red'),dict(icon='?',name='POTENTIAL',color='blue'),
       [('L','SpO2 86% now','Actual: oxygen 86 percent right now.'),('L','Happening now','It\'s happening.'),
        ('R','Risk for falls','Potential: risk for falls.'),('R','Could happen','It could happen.')]),
    P(('ACTUAL','red'),('BEATS POTENTIAL','yellow')),'Actual beats potential.',
    ['actual:','potential:','86'],'Actual vs Potential: Prioritization',
    'NCLEX priority: an actual problem (like SpO2 86% now) comes before a potential one (risk for falls).','prioritization')
add('2026-12-23','B','see-first-red-flags','teal',
    H('NEW','SUDDEN','SEE THEM FIRST','4 RED FLAGS',c1='red',c2='orange',join='+'),
    '4 findings you see first.',
    LS('SEE FIRST',[('Chest pain','+ sweating','red','Chest pain with sweating.'),('Sudden','shortness of breath','orange','Sudden shortness of breath.'),
                    ('New','confusion','pink','New confusion.'),('Noisy breathing','stridor','yellow','Stridor.')]),
    P(('NEW + SUDDEN','red'),('= FIRST','yellow')),'New and sudden goes first.',
    ['chest','sudden','new','stridor.'],'4 Red Flags: Who You See First',
    'New or sudden changes come first: chest pain with diaphoresis, sudden dyspnea, new confusion, stridor.','prioritization')
# ---------------- Dec 24 ----------------
add('2026-12-24','A','pneumo-vs-hemothorax','teal',
    H('AIR','BLOOD','CHEST','TRACHEA SHIFTS = TENSION',c1='cyan',c2='red',join='or'),
    'Air or blood in the chest?',
    VS(dict(icon='○',name='PNEUMO',color='cyan'),dict(icon='●',name='HEMO',color='red'),
       [('L','Air in the chest','Pneumothorax: air,'),('L','Hyperresonant','hyperresonant,'),('L','Tension: trachea shifts','tension pushes the trachea away.'),
        ('R','Blood in the chest','Hemothorax: blood,'),('R','Dull to percussion','dull to percussion.')]),
    P(('TRACHEA SHIFTS','cyan'),('= TENSION','red'),('EMERGENCY','yellow')),'Trachea shifts? Tension. Emergency.',
    ['air,','blood,','trachea','dull'],'Pneumothorax vs Hemothorax',
    'Pneumothorax: air, hyperresonant; tension pneumothorax shifts the trachea away and is an emergency. Hemothorax: blood, dull to percussion.','medsurg')
add('2026-12-24','B','incentive-spirometer','teal',
    H('SLOW','10x AN HOUR','INCENTIVE SPIROMETER','HOW TO TEACH IT',c1='cyan',c2='green',join='+'),
    'Incentive spirometer. Teach it right.',
    LS('TEACH',[('Seal lips','around mouthpiece','cyan','Seal the lips.'),('Inhale','slow and deep','green','Breathe in slow and deep.'),
                ('Hold','3–5 seconds','orange','Hold 3 to 5 seconds.'),('Repeat','10 times an hour','pink','10 times an hour while awake.')]),
    P(('SLOW IN','cyan'),('NOT FAST','red')),'Slow in, not fast.',
    ['slow','hold','10'],'Incentive Spirometer Teaching',
    'Seal lips, inhale slowly and deeply, hold 3–5 seconds, repeat about 10 times an hour while awake.','respiratory')
# ---------------- Dec 25 ----------------
add('2026-12-25','A','cbc-normals','purple',
    H('150K','400K','CBC NORMALS','PLATELETS 150 TO 400',c1='cyan',c2='green',join='to'),
    'CBC normals you have to know.',
    LS('NORMAL CBC',[('WBC','5,000–10,000','cyan','White count: 5,000 to 10,000.'),('Hgb (F)','12–16 g/dL','pink','Hemoglobin, female: 12 to 16.'),
                     ('Hgb (M)','14–18 g/dL','blue','Male: 14 to 18.'),('Platelets','150,000–400,000','green','Platelets: 150,000 to 400,000.')]),
    P(('PLATELETS < 50K','red'),('BLEEDING RISK','yellow')),'Platelets under 50,000? Bleeding precautions.',
    ['white','hemoglobin,','platelets:'],'CBC Normal Values',
    'WBC 5,000–10,000; hemoglobin 12–16 (female), 14–18 (male); platelets 150,000–400,000. Ranges vary by lab.','labvalues')
add('2026-12-25','B','hypo-vs-hypercalcemia','purple',
    H('LOW Ca','HIGH Ca','CALCIUM','STONES, BONES, GROANS',c1='blue',c2='orange'),
    'Low calcium or high calcium?',
    VS(dict(icon='↓',name='LOW Ca',color='blue'),dict(icon='↑',name='HIGH Ca',color='orange'),
       [('L','Twitching, tetany','Low calcium: twitching, tetany,'),('L','Positive Chvostek','positive Chvostek.'),
        ('R','Weak, sluggish','High calcium: weak and sluggish,'),('R','Kidney stones','kidney stones,'),('R','Constipation','constipation.')]),
    P(('HIGH Ca','orange'),('STONES, BONES','yellow'),('GROANS','yellow')),'High calcium: stones, bones, groans.',
    ['twitching,','tetany,','stones,','constipation.'],'Hypocalcemia vs Hypercalcemia',
    'Low calcium: twitching, tetany, positive Chvostek/Trousseau. High calcium: weakness, kidney stones, constipation ("stones, bones, groans").','electrolytes')
# ---------------- Dec 26 ----------------
add('2026-12-26','A','appendicitis','teal',
    H('RLQ','PAIN STOPS','APPENDICITIS','SUDDEN RELIEF = RUPTURE',c1='orange',c2='red',join='then'),
    'Appendicitis pain suddenly stops. Good news?',
    LS('APPENDICITIS',[('Pain','McBurney\'s point','orange','Pain at McBurney\'s point.'),('Where','right lower quadrant','pink','Right lower quadrant.'),
                       ('Avoid','heat, laxatives','cyan','No heat, no laxatives.'),('Pain suddenly stops','RUPTURE','red','Pain suddenly stops? It may have ruptured.')]),
    P(('SUDDEN RELIEF','red'),('= RUPTURE','yellow')),'Sudden relief can mean rupture. Report it.',
    ['mcburney\'s','heat,','ruptured.'],'Appendicitis: When the Pain Stops',
    'Appendicitis: RLQ pain at McBurney\'s point; no heat or laxatives. Sudden relief of pain can signal perforation: report it.','medsurg')
add('2026-12-26','B','uc-vs-crohns','teal',
    H('UC','CROHN\'S','IBD','CROHN\'S SKIPS AROUND',c1='red',c2='orange'),
    'Ulcerative colitis or Crohn\'s?',
    VS(dict(icon='▬',name='UC',color='red'),dict(icon='▪ ▪',name='CROHN\'S',color='orange'),
       [('L','Colon only','U C: colon only,'),('L','Continuous','continuous,'),('L','Bloody diarrhea','bloody diarrhea.'),
        ('R','Mouth to anus','Crohn\'s: mouth to anus,'),('R','Skip lesions','skip lesions.')]),
    P(('CROHN\'S','orange'),('SKIPS AROUND','yellow')),'Crohn\'s skips around.',
    ['colon','continuous,','bloody','skip'],'Ulcerative Colitis vs Crohn\'s',
    'UC: colon only, continuous, bloody diarrhea. Crohn\'s: anywhere from mouth to anus, with skip lesions.','medsurg')
# ---------------- Dec 27 ----------------
add('2026-12-27','A','pregnancy-signs','plum',
    H('PROBABLE','POSITIVE','PREGNANCY SIGNS','POSITIVE = SEE THE BABY',c1='orange',c2='green',join='or'),
    'Presumptive, probable or positive sign?',
    LS('PREGNANCY SIGNS',[('Presumptive','she notices','pink','Presumptive: she notices. Missed period, nausea.'),('Probable','examiner finds','orange','Probable: the examiner finds. Hegar\'s, a positive test.'),
                          ('Positive','proof of baby','green','Positive: proof of the baby. Heart tones, ultrasound.')]),
    P(('POSITIVE','green'),('= SEE THE BABY','yellow')),'Positive means you can see the baby.',
    ['presumptive:','probable:','positive:'],'Pregnancy Signs: Presumptive, Probable, Positive',
    'Presumptive: what she notices (missed period, nausea). Probable: what the examiner finds (Hegar\'s, Chadwick\'s, positive test). Positive: proof of the baby (fetal heart tones, ultrasound).','maternity')
add('2026-12-27','B','croup-vs-epiglottitis','plum',
    H('BARK','DROOL','CROUP vs EPIGLOTTITIS','STOP MIXING UP',c1='cyan',c2='red',join='or'),
    'Bark or drool? Croup or epiglottitis.',
    VS(dict(icon='🐕',name='CROUP',color='cyan'),dict(icon='💧',name='EPIGLOTTITIS',color='red'),
       [('L','Barking cough','Croup: barking cough,'),('L','Gradual','gradual onset.'),
        ('R','Drooling','Epiglottitis: drooling,'),('R','Sudden, high fever','sudden high fever.'),('R','Nothing in mouth','Nothing in the mouth.')]),
    P(('DROOLING?','red'),('AIRWAY EMERGENCY','yellow')),'Drooling? Airway emergency.',
    ['barking','drooling,','sudden','nothing'],'Croup vs Epiglottitis',
    'Croup: barking cough, gradual onset. Epiglottitis: drooling, sudden high fever, tripod position: nothing in the mouth, airway emergency.','peds')
# ---------------- Dec 28 ----------------
add('2026-12-28','A','opioid-od-vs-withdrawal','navy',
    H('PINPOINT','DILATED','OPIOIDS','PINPOINT = TOO MUCH',c1='red',c2='cyan',join='or'),
    'Opioid overdose or withdrawal? Look at the pupils.',
    VS(dict(icon='•',name='TOO MUCH',color='red'),dict(icon='●',name='WITHDRAWAL',color='cyan'),
       [('L','Pinpoint pupils','Overdose: pinpoint pupils,'),('L','Slow breathing','slow breathing.'),('L','Naloxone','Give naloxone.'),
        ('R','Dilated pupils','Withdrawal: dilated pupils,'),('R','Yawning, runny nose','yawning, runny nose,'),('R','Diarrhea','diarrhea.')]),
    P(('PINPOINT','red'),('= TOO MUCH','yellow')),'Pinpoint means too much.',
    ['pinpoint','dilated','naloxone.'],'Opioid Overdose vs Withdrawal',
    'Overdose: pinpoint pupils, slow breathing; give naloxone. Withdrawal: dilated pupils, yawning, runny nose, diarrhea.','pharmacology')
add('2026-12-28','B','communication-blockers','navy',
    H('WHY?','DON\'T WORRY','THERAPEUTIC COMMUNICATION','4 ANSWERS TO AVOID',c1='red',c2='orange',join='+'),
    '4 answers to cross out on the NCLEX.',
    LS('CROSS THESE OUT',[('"Why...?"','puts them on defense','red','Asking why.'),('"Don\'t worry"','false reassurance','orange','False reassurance.'),
                          ('"You should..."','giving advice','pink','Giving advice.'),('New topic','changing subject','cyan','Changing the subject.')]),
    P(('NEVER ASK','red'),('WHY','yellow')),'Never ask why. Reflect the feeling.',
    ['why.','reassurance.','advice.','subject.'],'Therapeutic Communication: 4 Answers to Avoid',
    'Cross out answers that ask "why," give false reassurance, give advice or change the subject. Reflect the client\'s feelings instead.','psych')
# ---------------- Dec 29 ----------------
add('2026-12-29','A','neutropenic-precautions','teal',
    H('NO FLOWERS','NO RAW FOOD','NEUTROPENIA','PROTECT THE CLIENT',c1='pink',c2='green',join='+'),
    'Low white cells. Protect your client.',
    LS('NEUTROPENIC',[('Fresh flowers','not allowed','pink','No fresh flowers or plants.'),('Raw fruits, veggies','avoid','green','No raw fruits or vegetables.'),
                      ('Room','private','cyan','Private room.'),('Visitors','no sick visitors','orange','No sick visitors.')]),
    P(('ANC < 1,000','red'),('PROTECT THEM','yellow')),'A N C under 1,000? Protect them. Policies vary.',
    ['flowers','raw','private','sick'],'Neutropenic Precautions',
    'Neutropenic precautions: no fresh flowers or plants, avoid raw produce, private room, no sick visitors. Follow facility policy.','infectioncontrol')
add('2026-12-29','B','kernig-vs-brudzinski','teal',
    H('KERNIG','BRUDZINSKI','MENINGITIS','K = KNEE, B = BEND NECK',c1='orange',c2='cyan'),
    'Kernig or Brudzinski? Never mix them up.',
    VS(dict(icon='K',name='KERNIG',color='orange'),dict(icon='B',name='BRUDZINSKI',color='cyan'),
       [('L','K = Knee','Kernig: knee.'),('L','Can\'t straighten it','Pain when straightening the knee.'),
        ('R','Bend the neck','Brudzinski: bend the neck,'),('R','Hips and knees flex','hips and knees flex.')]),
    P(('DROPLET','cyan'),('PRECAUTIONS','yellow')),'Bacterial meningitis: droplet precautions.',
    ['knee.','neck,','droplet'],'Kernig vs Brudzinski Sign',
    'Kernig: pain/resistance straightening the knee. Brudzinski: flexing the neck makes hips and knees flex. Bacterial meningitis: droplet precautions.','infectioncontrol')
# ---------------- Dec 30 ----------------
add('2026-12-30','A','hyperkalemia-treatment','purple',
    H('K 6.8','CALCIUM FIRST','HIGH POTASSIUM','TREATMENT ORDER',c1='red',c2='yellow',join=''),
    'Potassium 6.8. What goes first?',
    LS('TREATMENT ORDER',[('1. Protect heart','calcium gluconate','yellow','First, calcium gluconate protects the heart.'),('2. Shift K in','insulin + dextrose','green','Then insulin with dextrose shifts it into cells.'),
                          ('3. Remove K','binder / dialysis','cyan','Then remove it. Binders or dialysis.')]),
    P(('CALCIUM','yellow'),('PROTECTS','yellow'),('THE HEART','red')),'Calcium protects the heart first.',
    ['calcium','insulin','dialysis.'],'High Potassium: Treatment Order',
    'Hyperkalemia: calcium gluconate to stabilize the heart, insulin + dextrose to shift potassium into cells, then remove it (binders, diuretics or dialysis), per orders.','electrolytes')
add('2026-12-30','B','albuterol-vs-steroid','purple',
    H('ALBUTEROL','STEROID','ASTHMA INHALERS','RESCUE FIRST',c1='cyan',c2='orange'),
    'Two inhalers. Which goes first?',
    VS(dict(icon='⚡',name='ALBUTEROL',color='cyan'),dict(icon='🛡',name='STEROID',color='orange'),
       [('L','Rescue inhaler','Albuterol: rescue,'),('L','Opens airways fast','opens the airways fast.'),('L','Use first','Use it first.'),
        ('R','Controller','Steroid: controller,'),('R','Rinse mouth after','rinse your mouth after.')]),
    P(('ALBUTEROL FIRST','cyan'),('STEROID SECOND','orange')),'Albuterol first. Steroid second.',
    ['rescue,','first.','controller,','rinse'],'Albuterol vs Steroid Inhaler: Which First?',
    'Albuterol (rescue bronchodilator) first, then the inhaled steroid (controller); rinse the mouth after the steroid to prevent thrush.','respiratory')
# ---------------- Dec 31 ----------------
add('2026-12-31','A','iv-fluid-types','teal',
    H('ISO','HYPO','IV FLUIDS','HYPO = HIPPO',c1='green',c2='cyan',join='vs'),
    'IV fluids. Iso, hypo, or hyper?',
    LS('IV FLUIDS',[('Isotonic','0.9% NS, LR','green','Isotonic: normal saline, lactated Ringer\'s.'),('Hypotonic','0.45% NS','cyan','Hypotonic: half normal saline. Cells swell.'),
                    ('Hypertonic','3% NaCl','orange','Hypertonic: 3 percent saline. Pulls fluid out.')]),
    P(('HYPO = HIPPO','cyan'),('CELLS SWELL','yellow')),'Hypo, hippo. Cells swell.',
    ['isotonic:','hypotonic:','hypertonic:','swell.'],'IV Fluids: Isotonic, Hypotonic, Hypertonic',
    'Isotonic: 0.9% NS, LR. Hypotonic: 0.45% NS, cells swell ("hypo = hippo"). Hypertonic: 3% NaCl pulls fluid out of cells.','ivfluids')
add('2026-12-31','B','infiltration-vs-phlebitis','teal',
    H('COOL','WARM','IV SITE','COOL = INFILTRATION',c1='cyan',c2='red',join='or'),
    'Cool or warm IV site?',
    VS(dict(icon='❄',name='INFILTRATION',color='cyan'),dict(icon='🔥',name='PHLEBITIS',color='red'),
       [('L','Cool, pale','Infiltration: cool, pale,'),('L','Swollen','swollen.'),
        ('R','Warm, red','Phlebitis: warm, red,'),('R','Hard, cord-like vein','a hard, cord like vein.')]),
    P(('EITHER WAY','yellow'),('STOP + REMOVE IV','red')),'Either way: stop the infusion and remove the I V.',
    ['cool,','warm,','swollen.','cord'],'Infiltration vs Phlebitis',
    'Infiltration: cool, pale, swollen. Phlebitis: warm, red, cord-like vein. Either way, stop the infusion and remove the IV.','ivfluids')
# ---------------- Jan 1 ----------------
add('2027-01-01','A','priority-rules','navy',
    H('ABC','UNSTABLE','PRIORITY RULES','4 RULES FOR THE NEW YEAR',c1='red',c2='orange',join='+'),
    '4 priority rules for your NCLEX year.',
    LS('WHO GOES FIRST',[('ABCs','airway first','red','A B Cs. Airway first.'),('Acute','over chronic','orange','Acute over chronic.'),
                         ('Actual','over potential','pink','Actual over potential.'),('Unstable','over stable','cyan','Unstable over stable.')]),
    P(('UNSTABLE','red'),('GOES FIRST','yellow')),'Unstable always goes first.',
    ['airway','acute','actual','unstable'],'4 NCLEX Priority Rules',
    'ABCs first, acute over chronic, actual over potential, unstable over stable.','prioritization')
add('2027-01-01','B','warfarin-vitamin-k','purple',
    H('VITAMIN K','CONSISTENT','WARFARIN DIET','DON\'T AVOID IT',c1='green',c2='yellow',join=''),
    'On warfarin. Avoid leafy greens?',
    LS('WARFARIN TEACHING',[('Leafy greens','keep it consistent','green','Leafy greens: keep it consistent.'),('INR checks','as ordered','cyan','I N R checks as ordered.'),
                            ('Watch for','bleeding, bruising','red','Watch for bleeding and bruising.'),('Soft toothbrush','electric razor','pink','Soft toothbrush, electric razor.')]),
    P(('CONSISTENT','green'),('NOT ZERO','yellow')),'Consistent, not zero.',
    ['consistent.','bleeding','inr'],'Warfarin Diet: Consistent Vitamin K',
    'On warfarin, keep vitamin K intake consistent (don\'t eliminate greens), get INR checks, watch for bleeding, use a soft toothbrush and electric razor.','pharmacology')
# ---------------- Jan 2 ----------------
add('2027-01-02','A','deficit-vs-overload','teal',
    H('TOO DRY','TOO WET','FLUID BALANCE','1 KG = 1 LITER',c1='orange',c2='cyan',join='or'),
    'Fluid deficit or fluid overload?',
    VS(dict(icon='↓',name='DEFICIT',color='orange'),dict(icon='↑',name='OVERLOAD',color='cyan'),
       [('L','Fast pulse, low BP','Deficit: fast pulse, low pressure,'),('L','Dark urine','dark urine,'),('L','Weight down','weight down.'),
        ('R','Crackles','Overload: crackles,'),('R','JVD, edema','J V D, edema,'),('R','Weight up','weight up.')]),
    P(('1 KG','cyan'),('= 1 LITER','yellow')),'1 kilogram equals 1 liter of fluid.',
    ['crackles,','edema,','weight','liter'],'Fluid Volume Deficit vs Overload',
    'Deficit: tachycardia, low BP, concentrated urine, weight loss. Overload: crackles, JVD, edema, weight gain. 1 kg ≈ 1 L.','medsurg')
add('2027-01-02','B','daily-weights','teal',
    H('2–3 LB','A DAY','HEART FAILURE','CALL THE PROVIDER',c1='red',c2='orange',join=''),
    'Heart failure daily weights. When do you call?',
    LS('DAILY WEIGHTS',[('Same time','morning, after voiding','cyan','Same time, in the morning after voiding.'),('Same scale','same clothes','green','Same scale, same clothes.'),
                        ('Report','2–3 lb in a day','red','Report 2 to 3 pounds in a day,'),('Or','5 lb in a week','orange','or 5 pounds in a week.')]),
    P(('2–3 LB A DAY','red'),('CALL','yellow')),'2 to 3 pounds in a day? Call.',
    ['same','2','3','5'],'Heart Failure Daily Weights',
    'Weigh at the same time (morning, after voiding), same scale and clothing. Report a gain of 2–3 lb in a day or 5 lb in a week, or as instructed.','heartfailure')
# ---------------- Jan 3 ----------------
add('2027-01-03','A','fontanels','plum',
    H('BULGING','SUNKEN','FONTANELS','PRESSURE OR DRY',c1='red',c2='cyan',join='vs'),
    'Bulging or sunken fontanel?',
    VS(dict(icon='▲',name='BULGING',color='red'),dict(icon='▼',name='SUNKEN',color='cyan'),
       [('L','High ICP','Bulging: high pressure in the head.'),('L','Report now','Report it now.'),
        ('R','Dehydration','Sunken: dehydration.'),('R','Check diapers','Check wet diapers.')]),
    P(('ANTERIOR','yellow'),('CLOSES 12–18 MO','yellow')),'The front one closes at 12 to 18 months.',
    ['pressure','dehydration.','12','18'],'Fontanels: Bulging vs Sunken',
    'Bulging fontanel: increased ICP (when the infant is calm and upright). Sunken: dehydration. Anterior closes 12–18 months, posterior by about 2–3 months.','peds')
add('2027-01-03','B','engorgement-vs-mastitis','plum',
    H('ENGORGED','MASTITIS','BREASTFEEDING','MASTITIS? KEEP FEEDING',c1='orange',c2='red'),
    'Engorgement or mastitis?',
    VS(dict(icon='●●',name='ENGORGED',color='orange'),dict(icon='●',name='MASTITIS',color='red'),
       [('L','Both breasts','Engorgement: both breasts,'),('L','Full, firm','full and firm.'),
        ('R','One breast','Mastitis: usually one breast,'),('R','Red, wedge-shaped','red wedge shaped area,'),('R','Fever, flu-like','fever, flu like.')]),
    P(('KEEP','yellow'),('BREASTFEEDING','yellow')),'Mastitis? Keep breastfeeding.',
    ['both','one','fever,','breastfeeding.'],'Engorgement vs Mastitis',
    'Engorgement: both breasts, full and firm. Mastitis: usually one breast, red wedge-shaped area, fever, flu-like; keep breastfeeding or pumping.','maternity')
# ---------------- Jan 4 ----------------
add('2027-01-04','A','lithium-vs-valproate','navy',
    H('LITHIUM','VALPROATE','MOOD STABILIZERS','VALPROATE = LIVER',c1='cyan',c2='orange'),
    'Lithium or valproate? What do you monitor?',
    VS(dict(icon='Li',name='LITHIUM',color='cyan'),dict(icon='VPA',name='VALPROATE',color='orange'),
       [('L','Drug levels','Lithium: drug levels,'),('L','Sodium, fluids','sodium and fluids,'),('L','Kidneys, thyroid','kidneys and thyroid.'),
        ('R','Liver tests','Valproate: liver tests,'),('R','Platelets','platelets,'),('R','Pancreas','pancreas.')]),
    P(('VALPROATE','orange'),('= LIVER','yellow')),'Valproate? Check the liver.',
    ['sodium','kidneys','liver','platelets,'],'Lithium vs Valproate Monitoring',
    'Lithium: serum levels, sodium/fluid intake, kidney and thyroid function. Valproate: liver function, platelets, pancreatitis signs.','psych')
add('2027-01-04','B','seizure-precautions','navy',
    H('TIME IT','SIDE-LYING','SEIZURE','NOTHING IN THE MOUTH',c1='yellow',c2='cyan',join='+'),
    'Seizure. What do you do?',
    LS('DURING A SEIZURE',[('Time it','start to end','yellow','Time it.'),('Protect','move objects away','cyan','Move things away. Protect the head.'),
                           ('Turn','side-lying after','green','Turn to the side.'),('Mouth','nothing in it','red','Nothing in the mouth.')]),
    P(('NOTHING','red'),('IN THE MOUTH','yellow')),'Never put anything in the mouth.',
    ['time','side.','nothing'],'Seizure: What to Do',
    'Time it, protect the head and move objects away, turn to the side, never put anything in the mouth.','neuro')
# ---------------- Jan 5 ----------------
add('2027-01-05','A','sterile-vs-clean','teal',
    H('STERILE','CLEAN','TECHNIQUE','INTO STERILE SPACE = STERILE',c1='cyan',c2='green'),
    'Sterile or clean technique?',
    VS(dict(icon='✚',name='STERILE',color='cyan'),dict(icon='✓',name='CLEAN',color='green'),
       [('L','Urinary catheter','Sterile: urinary catheter,'),('L','Central line dressing','central line dressing.'),
        ('R','NG tube','Clean: N G tube,'),('R','Enema','enema.')]),
    P(('STERILE BODY','cyan'),('SPACE?','cyan'),('STERILE','yellow')),'Going into a sterile space? Sterile technique.',
    ['sterile:','clean:','catheter,','enema.'],'Sterile vs Clean Technique',
    'Sterile technique for entering sterile spaces or lines (urinary catheter, central line dressing). Clean technique for NG tube insertion and enemas.','infectioncontrol')
add('2027-01-05','B','pressure-injury-stages','teal',
    H('STAGE 1','STAGE 4','PRESSURE INJURY','DOESN\'T BLANCH = STAGE 1',c1='pink',c2='red',join='to'),
    'Pressure injury stages in 15 seconds.',
    LS('STAGES',[('Stage 1','red, doesn\'t blanch','pink','Stage 1: red, doesn\'t blanch.'),('Stage 2','blister, partial','orange','Stage 2: blister, partial thickness.'),
                 ('Stage 3','fat visible','yellow','Stage 3: full thickness, fat visible.'),('Stage 4','bone, muscle','red','Stage 4: bone or muscle.')]),
    P(('PRESS IT','yellow'),('STAYS RED?','red'),('STAGE 1','pink')),'Press it. Stays red? Stage 1.',
    ['stage','blanch.','bone'],'Pressure Injury Stages',
    'Stage 1: nonblanchable redness. Stage 2: partial thickness/blister. Stage 3: full thickness, fat visible. Stage 4: bone, tendon or muscle exposed.','medsurg')

if __name__ == '__main__':
    import json, os
    os.makedirs('cfgs', exist_ok=True)
    for e in E:
        e2 = dict(e); e2['kind'] = e['kind']
        json.dump(e2, open(f"cfgs/{e['id']}.json", 'w'), indent=1, ensure_ascii=False)
    print(len(E), 'configs')
