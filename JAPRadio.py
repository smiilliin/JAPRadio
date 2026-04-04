# Auto-generated from JAPRadio.ipynb

#%pip install langchain langchain-openai openai

import os
from env import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

import json
import os
from datetime import datetime

FILE_PATH = "topics.json"

def load_topics():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topics(topics):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

def save_script(script, topic, now):
    if not os.path.exists("scripts"):
        os.mkdir("scripts")

    data = {
        "time": now,
        "topic": topic,
        "script": script
    }

    filename = f"scripts/{now}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

previous_topics = load_topics()
print("[ Loaded previous topics ]")
for topic in previous_topics:
    print(topic)

condition_topic = f"""
일본어 라디오에서 사용할 주제를 1개 생성하라.

[조건]
- JLPT N5 청취자가 이해할 수 있는 쉬운 주제
- 일상적이고 공감 가능한 내용
- 너무 추상적이거나 어려운 개념 금지

[출력 규칙]
- 오직 "주제 한 줄"만 출력
- 불필요한 설명, 따옴표, 번호, 줄바꿈 금지
- 20자 이내로 작성

[중복 방지]
- 아래 주제들과 의미적으로 겹치지 않도록 할 것:
{previous_topics}
"""
condition_script = """
이 대본을 JLPT N5 수준 청취자를 위한 일본어 라디오 스크립트로 재작성하라.

[목표]
- 일본어 초급 학습자가 듣고 이해할 수 있는 자연스러운 라디오

[언어 수준]
- JLPT N5 수준의 어휘와 문법을 우선 사용
- 불가피하게 어려운 표현이 포함될 경우 최대 10개 이하로 제한
- 어려운 단어는 가능한 쉬운 표현으로 바꾼다

[스타일]
- 캐주얼하고 부드러운 말투 사용 (친근한 라디오 진행자 느낌)
- 청자에게 말을 거는 표현 포함 (예: みなさん、どうですか？)
- 딱딱한 설명체 금지

[문장 구조]
- 문장은 짧고 말하듯이 작성
- 한 문장에 하나의 정보만 전달
- 자연스러운 호흡을 위해 「、」「。」 적절히 사용

[청해 최적화]
- 발음하기 어려운 한자, 외래어, 숫자는 가능한 한 풀어서 표현
- 의미 단위로 끊어 읽기 쉽게 구성

[재미 요소]
- 가벼운 감정 표현 또는 공감 요소 포함
- 청취자가 상황을 상상할 수 있도록 묘사 추가

[학습 요소]
- 라디오에서 사용된 핵심 일본어 표현 2~3개 설명
- 각 표현의 의미와 사용 상황을 간단히 설명
- 비슷한 쉬운 표현 1개 추가 소개 (선택)
- 핵심 문장 1개를 제시하고 따라 말해볼 수 있도록 유도
- 라디오 마무리에 청취자가 자신의 경험과 연결해 생각해볼 수 있는 질문 1개 추가

[출력 형식]
- 일본어 라디오 대본 형태로 출력
- 불필요한 설명 없이 대본만 출력
"""

condition_tts = """
이 대본을 TTS용 일본어 라디오 스크립트로 재작성하라.

조건:
1. JLPT N5 수준 청취자가 이해 가능해야 한다
2. 발음이 자연스럽도록 어려운 한자, 영어, 숫자를 풀어쓴다
3. 문장은 짧고 말하듯이 작성한다
4. 쉼표(、)와 마침표(。)를 사용해 호흡을 만든다
5. 라디오 진행자처럼 부드럽고 따뜻한 말투로 작성한다
6. 청자에게 말을 거는 표현을 포함한다
7. 감정 표현을 자연스럽게 포함한다
8. 필요하다면 (間), (笑) 등의 발화 표현을 사용한다
"""

from langgraph.graph import StateGraph
from typing import TypedDict, Optional
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


class GraphState(TypedDict):
    topic: Optional[str]
    script: Optional[str]

def topic_node(state: GraphState) -> GraphState:
    print("\n[Topic Agent INPUT]")
    print(state)

    output =  llm.invoke(condition_topic).content
    state["topic"] = output

    print("\n[Topic Agent OUTPUT]")
    print(output)

    return state

def script_node(state: GraphState) -> GraphState:
    print("\n[Script Agent INPUT]")
    print(state)

    output = llm.invoke(f"${condition_script}\n{state['topic']}로 일본어 대본 작성").content
    state["script"] = output

    print("\n[Script Agent OUTPUT]")
    print(output)

    return state

def rewrite_node(state):
    new_script = llm.invoke(
        f"{condition_tts}\대본을 수정:\n{state['script']}"
    ).content

    state["script"] = new_script
    print("\n[Rewrite OUTPUT]")
    print(new_script)

    return state


graph = StateGraph(GraphState)

graph.add_node("topic", topic_node)
graph.add_node("script", script_node)
graph.add_node("rewrite", rewrite_node)


graph.set_entry_point("topic")

graph.add_edge("topic", "script")
graph.add_edge("script", "rewrite")


app = graph.compile()

result = app.invoke(GraphState(topic=None, script=None))
print(result)

script, topic = result["script"], result["topic"]

now = datetime.now().strftime("%Y%m%d_%H%M%S")

previous_topics.append(topic)
save_topics(previous_topics)
save_script(script, topic, now)

from openai import OpenAI
import os
from datetime import datetime

client = OpenAI()

def save_tts(script, now):
    if not os.path.exists("audio"):
        os.mkdir("audio")

    filename = f"audio/{now}.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # 또는 "verse", "aria" 등
        input=script
    )

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"🎧 음성 저장 완료: {filename}")

    return filename


def preprocess_for_tts(script):
    return script \
        .replace("（間）", "、") \
        .replace("（笑）", "（わらい）")

# from pydub import AudioSegment

# def mix_bgm(tts_file, bgm_file, output_file):
#     voice = AudioSegment.from_file(tts_file)
#     bgm = AudioSegment.from_file(bgm_file)

#     # BGM 길이를 음성에 맞춤 (loop)
#     if len(bgm) < len(voice):
#         times = len(voice) // len(bgm) + 1
#         bgm = bgm * times

#     bgm = bgm[:len(voice)]

#     # 🔥 볼륨 줄이기 (중요)
#     bgm = bgm - 20  # dB 줄임

#     # 합치기
#     mixed = voice.overlay(bgm)

#     mixed.export(output_file, format="mp3")

#     print(f"🎶 BGM 포함 완료: {output_file}")

audio_script = preprocess_for_tts(result["script"])
save_tts(audio_script, now)

