import random

from voice_handler import Recoder
import os
import uuid
import yaml
from csv_handler import CSVHandler
from zipfile import ZipFile

MULT_TIMES = 3


def start():
    with open('voice-list.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    try:
        os.mkdir("wavs")
    except FileExistsError:
        pass
    try:
        os.mkdir("wavs/speakers")
    except FileExistsError:
        pass
    speaker = input("Please enter your name: ")
    name_prefix = "wavs/speakers/" + speaker + "/"

    try:
        os.mkdir(name_prefix)
    except FileExistsError:
        print("Speaker already exists")
        return

    counter = 0
    try:
        recoder = Recoder()
    except OSError:
        print("Please check your microphone")
        return
    csv = CSVHandler(speaker + ".csv")

    for d in data["data"]:
        try:
            for i in range(MULT_TIMES):
                print("\n\n-------------------- Round " + str(i + 1 + counter*MULT_TIMES) + " / " +
                      str(len(data["data"])*MULT_TIMES) + " --------------------")
                print("Please readout: \033[1m\"" + data["prefix"][random.randrange(0, len(data["prefix"]))] +
                      d["script"] + "\"\033[0m")
                recName = name_prefix + d["script"].replace(" ", "-") + "-" + str(uuid.uuid4()) + ".wav"
                input("Press ENTER to start the recording")
                recoder.start(recName)
                input("Press ENTER to stop the recording")
                recoder.stop()
                csv.append_line(recName, speaker, d["script"], d["action"], d["object"])
            counter += 1

        except KeyboardInterrupt:
            break

    recoder.close()
    csv.save()
    zip_name = speaker + '.zip'
    with ZipFile(zip_name, 'w') as zipObj:
        zipObj.write(speaker + '.csv')
        zipObj.write("wavs/speakers/" + speaker, "wavs/speakers/" + speaker)
        for _, _, files in os.walk("wavs/speakers/" + speaker):
            for file in files:
                zipObj.write("wavs/speakers/" + speaker + "/" + file, "wavs/speakers/" + speaker + "/" + file)

    print("\n\nThis is the ending of audio collection. \nThe zip file is located at \033[1m" + zip_name + "\033[0m")
    print("Thank you for your contribution!")


if __name__ == "__main__":
    start()
