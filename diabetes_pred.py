import streamlit as st
import pickle

st.title('Predicting type II diabetes')
# Disclaimer chunk
disclaimer_spot = st.beta_container()
disclaimer = """A computer is never a substitute for a conversation with your doctor. This app
may help you get a handle on your likely type II diabetes risk, but a high
probability doesn't mean you're going to develop type II diabetes, nor does a
low result mean you're safe from type II diabetes. In all cases, your best bet
for staying healthy is to get moving every day (30 minutes of exercise
throughout the day is the goal) and eat plenty of plants.

You can read more about type II diabetes here.

## Sanity check:
If you have one or two of following symptoms, at least talk to your doctor on your next visit. If you have several of them, please make an appointment as soon as possible!
* Increased thirst and frequent urination
* Increased hunger and unintended weight loss without a big change in physical
  activity
* Fatigue
* Blurred vision
* Slow-healing sores
* Frequent infections
* Patches of dark skin, usually in the armpits and around the neck
"""
sanity = st.checkbox('I understand that this is a portfolio project from a data science student and is no substitute for a consulation with my primary care provider.')
if not sanity:
    disclaimer_spot.write(disclaimer)

# Initially setting to 0 because slider itself is nested inside an if statement
preg_slider = 0

# Sidebar content shows up after sanity box is checked
if sanity:
    age_slider = st.sidebar.slider('age', min_value = 18, max_value = 100, value = 50, key = 'age_slider')
    if (age_slider < 21) or (age_slider > 81):
        st.write('Nobody in your age range was in the training set; be particularly skeptical about the results!')
    bmi_slider = st.sidebar.slider('BMI', min_value = 15, max_value = 80, value = 27, key = 'bmi_slider')
    if (bmi_slider < 19) or (bmi_slider > 67):
        st.write('Nobody in your BMI range was in the training set; be particularly skeptical about the results!')
    bp_checkbox = st.sidebar.checkbox('Add blood pressure?')
    if bp_checkbox:
        st.sidebar.write('Enter your blood pressure (systolic over diastolic) below:')
        sysbp_entry = st.sidebar.number_input('systolic', value = 120)
        diabp_entry = st.sidebar.number_input('diastolic', max_value = sysbp_entry, value = 80)
        if sysbp_entry > 180 or diabp_entry > 120:
            st.write('*You need to see a doctor immediately about your blood pressure!*')
        elif sysbp_entry > 140 or diabp_entry > 90:
            st.write('You should talk to a doctor about your blood pressure.')
    f_checkbox = st.sidebar.checkbox('Hormonally female?*', key = 'f_checkbox')
    if f_checkbox:
        preg_slider = st.sidebar.slider('pregnancies', min_value = 0, max_value = 15, value = 0, key = 'preg_slider')
    hormone_checkbox = st.sidebar.checkbox('What does "hormonally female" mean?')

    # Hormone explainer
    hormone_explainer =  """
        ## Why "hormonally female?*"
        *Your hormones play a big role in the development of diabetes. Your results are
        more likely to be correct if you select "hormonally female" in any of the
        following cases:

        1. Assigned female at birth and have not taken anything to block estrogen (e.g.
        hormone blockers, some medications for endometriosis) over the few several
        years.
        2. You've been taking supplmental estrogen for at least a few years, for
        whatever reason. If you're not sure or you're in an edge case (recently
        started hormone blockers or went off hormone blockers), it may be useful for
        you to look at your results both with the box checked and with it unchecked
        so you can get an idea of the range of your risk prediction.
        """
    if hormone_checkbox:
        st.write(hormone_explainer)

    # Predicting something!
    pickle_in = open('logreg1.pkl', 'rb')
    classifier1 = pickle.load(pickle_in)
    pickle_in = open('logreg2.pkl', 'rb')
    classifier2 = pickle.load(pickle_in)
    def classifier_abm(age, bmi, male):
        return classifier1.predict_proba([[age_slider, bmi_slider, not(f_checkbox)]])[0][1]
    def classifier_abmd(age, bmi, male, diabp):
        return classifier2.predict_proba([[age_slider, bmi_slider, not(f_checkbox), diabp_entry]])[0][1]

    score_explainer = """More detail coming later, but a score above 0.5 means you're at above-average risk of developing type II diabetes, while a score of 0.5 means you're at a below-average risk of developing type II diabetes. In all cases, moving every day and eating plenty of plants will tend to lead to better health. If your risk is higher, try to prioritize exercise and a more plant-rich diet; you should also ask your doctor about your diabetes risk the next time you're in.

    Anyone can develop type II diabetes; be good to yourself so you can lower your risk!
    """

    if preg_slider > 0:
        pass
    elif not bp_checkbox:
        result = classifier_abm(age_slider, bmi_slider, not(f_checkbox))
        if st.button('predict my score'):
            st.success(f'The model puts you at a {round(result, 2)} score')
            st.write(score_explainer)

    else:
        result = classifier_abmd(age_slider, bmi_slider, not(f_checkbox), diabp_entry)
        if st.button('predict my score'):
            st.success(f'The model puts you at a {round(result, 2)} score')
            st.write(score_explainer)
