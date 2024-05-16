import os
import random
from pathlib import Path
import json

from openai import OpenAI

client = OpenAI()

FEATURE_CALL_OPENAI = True

filename = 'audio2.txt'

message_prompts = """
Find important conversations in the list of sentences

Instructions for finding important sentences:
Do not give different output every time
Go through all the sentences first and then decide which sentences are important
Give me exactly 20 important sentences
Do not give more than 20 sentences
Do not give less than 20 sentences
Dont do any spelling corrections
Dont modify the original sentences
Do not merge sentences
Do not summarise
Make sure not to change the order of sentences
do not put number before sentences in the output
do not put empty lines in the output
do not modify the sentences
Add newline between sentenses in the output
Dont alter case sensitivity
Dont duplicate same sentences
"""


def validateSubtitle(inPutTxt, OutPutTxt):
    for outputLine in OutPutTxt:
        textMatchFound = 0
        for inputLine in inPutTxt:
            # print ("outputLine", outputLine, "inputLine", inputLine)
            if (outputLine == inputLine):
                textMatchFound = 1
                break

        print("textMatchFound", textMatchFound)


def getSubtitleNumbers(inPutTxt, OutPutTxt):
    subTitleNumbers = []
    for outputLine in OutPutTxt:
        subTitleCount = 0
        for inputLine in inPutTxt:
            # print ("outputLine", outputLine, "inputLine", inputLine)
            if (outputLine == inputLine):
                subTitleNumbers.append(subTitleCount)
                break
            subTitleCount = subTitleCount + 1
    return (subTitleNumbers)


def GetImportantSubtitleNumbers(filename):
    filename_without_extention, filename_extension = os.path.splitext(filename)

    subtitle_mod_output_file_srt = filename_without_extention+"_mod.srt"
    subtitle_mod_output_file_txt = filename_without_extention+"_mod.txt"
    print("filename_without_extention", filename_without_extention,
          "filename_extension", filename_extension)

    if FEATURE_CALL_OPENAI:
        with open(filename, 'r') as file1:
            subtitletxt = file1.read()

        random.seed(123)  # Change the seed value as needed
        # temperature = random.uniform(0.7, 1.0)
        temperature = 0.9
        top_p = 1.0

        # print ("subtitletxt", subtitletxt);
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": message_prompts},
                {"role": "user", "content": subtitletxt}
            ],
            temperature=temperature,
            top_p=top_p
        )

        output_file_txt_1 = completion.choices[0].message.content.strip()
        print("AI Response", output_file_txt_1)

        output_file_txt_2 = output_file_txt_1.splitlines()
        print("AI Response", output_file_txt_2)

        with open(subtitle_mod_output_file_txt, 'w') as file1:
            file1.write(output_file_txt_1)

    with open(filename, 'r') as file1:
        input_file_txt = file1.readlines()

    input_file_txt = [line.strip() for line in input_file_txt]

    with open(subtitle_mod_output_file_txt, 'r') as file2:
        output_file_txt = file2.readlines()

    output_file_txt = [line.strip() for line in output_file_txt]
    output_file_txt = [line.strip()
                       for line in output_file_txt if line.strip()]

    # print ("input_file_txt")
    # print (input_file_txt)
    print("output_file_txt")
    print(output_file_txt)

    validateSubtitle(input_file_txt, output_file_txt)
    subTitleNumbers = getSubtitleNumbers(input_file_txt, output_file_txt)
    # remove duplicates as some time same text is there in subtitle file
    subTitleNumbers = list(set(subTitleNumbers))
    # sort as AI some times gives the text in different order
    subTitleNumbers.sort()
    # print ("subTitleNumbers output", subTitleNumbers)
    return subTitleNumbers


def extract_highlights(session):
    filename = session['audio_srt_path']
    num_of_subtitles = 0
    segIds = []
    while True:
        segIds = GetImportantSubtitleNumbers(filename)
        num_of_subtitles = len(segIds)
        print("num_of_subtitles", num_of_subtitles,
              "subTitleNumbers output", segIds)

        if (num_of_subtitles > 10):
            break

    segIds_path = Path(session['dir']) / "segIds.json"

    with open(str(segIds_path), 'w') as f:
        f.write(json.dumps(segIds))

    session['segIds_path'] = segIds_path
    session['segIds'] = segIds

    return segIds


if __name__ == "__main__":
    subs1 = extract_highlights('./dl/N9zpRvFRmj8/audio.srt')
    print("subTitleNumbers output", subs1)
