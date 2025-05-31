import os
import chainlit as cl
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Keywords to identify postpartum-related questions
POSTPARTUM_KEYWORDS = [
    "postpartum", "baby","bacha", "delivery", "diet", "hygiene", "health", "nutrition",
    "mental", "mother", "breastfeeding", "newborn", "care", "exercise", "sleep",
    "recovery", "infection", "multivitamin", "pain", "medicine", "nazar", "wazan",
      "postpartum", "delivery", "c-section", "normal delivery", "newborn", "baby",
    "breastfeeding", "lactation", "milk supply", "nifas", "bleeding", "mother", "mom",
    "new mom", "maternity", "sleep", "diet", "food", "nutrition", "multivitamin", "rest",
    "recovery", "stitches", "mental health", "depression", "baby blues", "exercise",
    "weight loss", "abdominal pain", "infection", "urine", "stool", "constipation",
    "diaper", "crying", "mother care", "suten", "safai", "hygiene", "safai ka khayal",
    "naf ka dard", "seene ka dard", "doodh", "dard", "neend", "kamzori", "weakness",
    "postnatal", "pain", "wazn", "doodh pilana", "urine infection", "hormones", "pait",
    "hygiene", "bacha", "bachi", "doodh", "seena", "pain", "takleef", "nind", "neend", "kamzori",
"thakan", "weight", "wazan", "diet", "infection", "jalan", "sujan", "dard", "pait", "bukhar",
"tabiyat", "bhukh", "khana", "doctor", "medicine", "dawa", "breastfeeding", "diaper", "kapray",
"kapde", "daant", "muh", "garmi", "sardee", "zukam", "khansi", "pet", "dast", "qabz", "exercise",
"rest", "tension", "depression", "mood", "pareshaani", "badan", "pair", "gardan", "kamar",
"jism", "paon", "zakhm", "stitches", "operation", "cesarean", "delivery", "breast", "malish",
"roona", "hormonal", "motapa", "vitamin", "calcium", "anemia", "blood", "mental", "anxiety",
"milk", "crying", "sleep", "immunity", "checkup", "vitamins", "relax", "meditation", "therapy",
"cleanliness", "suthra", "feeding", "immunization", "pani", "neonatal", "childcare", "weightgain",
"baby", "newborn", "stitch", "feedingtime", "babycare", "immunesystem", "nutrition", "fatigue",
"birth", "postnatal", "postpartum", "infectioncontrol", "babyfood", "milkproduction",
"bodypain", "physicalactivity", "water", "iron", "multivitamin", "resttime", "healthtips",
"healthcheck", "bloodloss", "naps", "sleepdeprivation", "milkflow", "mastitis", "engorgement",
"breastpump", "formula", "diarrhea", "constipation", "swelling", "painrelief", "breastmilk",
"milkquality", "nursing", "breastcare", "breastfeedingproblems", "newmom", "momhealth",
"childhealth", "babyweight", "babysleep", "babyfeeding", "postpartumdepression",
"weightloss", "postbirth", "labour", "birthinjury", "breastinfection", "mastitispain",
"colostrum", "milkletdown", "babymassage", "babysafety", "childdevelopment", "babycries",
"babycaretips", "breastmilkstorage", "breastmilkexpression", "babyskin", "babybath",
"breastmilkcomposition", "lactation", "lactationconsultant", "newbornfeeding", "babygrowth",
"breastfeedingadvice", "babyschedule", "postpartumcare", "babyweightgain", "babydiet",
"babynutrition", "momrest", "breastmilkintake", "breastfeedingfrequency", "breastfeedingduration",
"babysucking", "babytongue", "milkproductionissues", "breastfeedingpositions",
"breastfeedingcomfort", "milkallergy", "breastfeedingchallenges", "babybonding", "momnutrition",
"babysafetyfirst", "babyhealthcare", "breastfeedingtechniques", "newbornhealth", "babynutritiontips",
"breastfeedingbenefits", "babysleeppatterns", "newmomcare", "babyweighttracking",
"babysleeptraining", "breastfeedingproblemsolutions", "babyfeedingmethods", "babysupport",
"babymonitoring", "momhealthtips", "babysafetyawareness", "breastfeedinghygiene",
"breastmilkpreservation", "breastfeedingproblemsolving", "babymilksupply", "babymilkintake",
"babysuckling", "breastfeedingnutrition", "babyfeedingfrequency", "babyweightmonitoring",
"babysleeproutine", "breastfeedingcomforttips", "breastfeedingpositionsafety", "postpartumrecovery",
"babysleepenvironment", "mommentalhealth", "breastfeedingcounseling", "babyfeedingadvice",
"babynutritionadvice", "momselfcare", "babysafetymeasures", "postpartumweightloss",
"breastfeedingsupport", "breastfeedingproblemsolvingtips", "babymilksupplyissues",
"breastfeedingeducation", "babysleepissues", "momhealthsupport", "breastfeedingawareness",
"babynutritionguidance", "babysafetyeducation", "momhealtheducation"

    


]

# Check if user input is related to postpartum
def is_postpartum_question(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in POSTPARTUM_KEYWORDS)

# Generate strict prompt for Gemini
def generate_prompt(user_input: str) -> str:
    return f"""
You are a helpful assistant created only to support postpartum women.
Your responsibilities are:
- Giving health, diet, and hygiene advice to new mothers
- Helping with breastfeeding, baby care, and recovery
- Responding only in English or Roman Urdu (same as user)

⚠️ Do not answer if the topic is not related to postpartum women.

User message: "{user_input}"
Answer in the same language.
"""

# Greeting message
@cl.on_chat_start
async def start():
    await cl.Message(content="👩‍🍼 Assalamualaikum! Main aapki postpartum health assistant hoon. Diet, hygiene ya baby care ke baray mein poochhiye!").send()

# Message handler
@cl.on_message
async def handle(message: cl.Message):
    user_input = message.content

    if not is_postpartum_question(user_input):
        await cl.Message(content="❌ Maaf kijiye, main sirf postpartum aur new moms ke health se related sawalon ke jawab deti hoon.").send()
        return

    try:
        prompt = generate_prompt(user_input)
        response = model.generate_content(prompt)
        await cl.Message(content=response.text).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()
