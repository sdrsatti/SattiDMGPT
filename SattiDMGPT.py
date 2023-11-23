# ''' 
# This program is uploaded to git and then pushed to https://sattiafibchatgpt.streamlit.app
# After this program is saved, run from cmd from this directory:
#     git commit -a -m "Main"
#     git push
# This is will update git and then automatically update streamlit.
# '''


from openai import OpenAI
import streamlit as st
import time

client = OpenAI()

assistant = client.beta.assistants.create(
    name="SattiDMAI",
    instructions="You are a senior endocrinologist with a specialized interest in the diagnosis and management of diabetes. Give complete and through answers using the files uploaded and only answer medical questions.",
    tools=[{"type": "retrieval"}],
    file_ids=['file-GFSQ4TYFjfsoEFi3mwhWMsAL'],
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()

def getanswer(question):

  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content= question
  )

  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Give complete and through answers using the files uploaded and only answer medical questions"
  )

  while run.status != "completed":
      time.sleep(1)
      run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
  )

  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )

  answer = messages.data[0].content[0].text.value

  return(answer)


st.set_page_config(page_title='Satti Diabetes GPT', page_icon='robot')


st.header('Satti DM GPT')
st.write('by S. D. Satti, MD, FACC, FHRS - me@sattimd.com')
st.write("This is an extension of OpenAI's ChatGPT with additional training using Standards of Care in Diabetes—2023 Guidelines.")
st.write('')

base_prompt = "Give specific answers. In a separate paragraph, at the end give an itemized list the individual references for the following: "
input_prompt = st.text_area(label='What is your query:', key='user_input')

prompt = input_prompt

if st.button(label='Submit'):
    if input_prompt != '':
        st.write("Thinking...(may take up to a minute)")
        answer = getanswer(prompt)
        st.write(answer)

