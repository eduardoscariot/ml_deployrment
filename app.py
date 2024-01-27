import streamlit as st
import data_handler 
import util
import matplotlib.pyplot as plt
import pandas as pd
import pickle

if not util.check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.title('App dos dados do Titanic')
data_analyses_on = st.toggle('Exibir análise dos dados')
dados = data_handler.load_data()
model = pickle.load(open('./models/model.pkl', 'rb'))

if data_analyses_on:

    st.dataframe(dados)

    st.header("Histograma das idades")
    fig = plt.figure()
    plt.hist(dados['Age'], bins=30)
    plt.xlabel("Idade")
    plt.ylabel("Quantidade")
    st.pyplot(fig)

    st.header("Sobreviventes")
    st.bar_chart(dados.Survived.value_counts())

st.header('Preditor de sobrevivência')

# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    classes = ["1st", "2nd", "3rd"]
    p_class = st.selectbox('Ticket class', classes)

with col2:
    classes = ["Male", "Female"]
    sex = st.selectbox('Sex', classes)

with col3:
    age = st.number_input("Age in year", step=1, min_value=0)

# Row 2
col1, col2, col3 = st.columns([2,2,1])
with col1:
    sib_sp = st.number_input("Number of sibilings / spouses aboard", step=1, min_value=0)

with col2:
    par_ch = st.number_input("Number of parents / children aboard", step=1, min_value=0)

with col3:
    fare = st.number_input("Passenger fare")

# Row 3
col1, col2 = st.columns(2)
with col1:
    classes = ['Cherbourg', 'Queenstown', 'Southampton']
    embarked = st.selectbox('Port of Embarkation', classes)

with col2:
    submit = st.button("Verificar")

p_class_map = {
    '1st': 1, 
    '2nd': 2, 
    '3rd': 3
}
sex_map = {
    'Male': 0,
    'Female': 1,
}
embarked_map = {
    'Cherbourg': 0, 
    'Queenstown': 1, 
    'Southampton': 2
}
passageiro = {}
if submit or 'survived' in st.session_state:
    passageiro = {
        'Pclass': p_class_map[p_class],
        'Sex': sex_map[sex],
        'Age': age,
        'SibSp': sib_sp,
        'Parch': par_ch,
        'Fare': fare,
        'Embarked': embarked_map[embarked]
    }

    st.write(passageiro)

    values = pd.DataFrame([passageiro])
    st.dataframe(values)

    results = model.predict(values)

    if len(results) == 1:
        survived = int(results[0])

        if survived == 1:
            st.subheader("Passageiro sobreviveu! 🙌😎")
            if 'survived' not in st.session_state:
                st.balloons()
        else:
            st.subheader("Passageiro não sobreviveu. 😢")
            if 'survived' not in st.session_state:
                st.snow()

        st.session_state['survived'] = survived

    if passageiro and 'survived' in st.session_state:
        st.write("A predição está correta?")

        col1, col2, col3 = st.columns([1,1,5])
        with col1:
            correct_prediction = st.button("👍")
        with col2:
            wrong_prediction = st.button("👎")
        
        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo seu feedback. "
            if wrong_prediction:
                message += "Iremos utilizar esses dados para melhorar nosso modelo."
            
            if correct_prediction:
                passageiro['CorrectPrediction'] = True
            elif wrong_prediction:
                passageiro['CorrectPrediction'] = False
            
            passageiro['Survived'] = st.session_state['survived']
            st.write(message)
            
            data_handler.save_prediction(passageiro)


    col1, col2, col3 = st.columns(3)

    with col2:
        new_test = st.button("Iniciar nova análise")

        if new_test and 'survived' in st.session_state:
            del st.session_state['survived']
            st.rerun()
    
accuracy_prediction_on = st.toggle("Exibir acurácia")

if accuracy_prediction_on:
    predictions = data_handler.get_all_predictions()

    num_total_predictions = len(predictions)
    correct_predictions = 0
    total = 0
    accuracy_hist = []
    for index, passageiro in enumerate(predictions):
        total = total + 1
        if passageiro['CorrectPrediction'] == True:
            correct_predictions += 1
        
        temp_accuracy = correct_predictions / total if total else 0
        accuracy_hist.append(round(temp_accuracy, 2))

    accuracy = correct_predictions / num_total_predictions if num_total_predictions else 0

    st.metric("Acurácia", round(accuracy, 2))
    # st.write(accuracy_hist)
    #st.write(results)

    st.subheader("Histórico de acurácia")
    st.line_chart(accuracy_hist)


