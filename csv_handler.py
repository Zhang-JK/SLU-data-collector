import csv


class CSVHandler(object):
    def __init__(self, name):
        self.name = name
        self.file = open(name, 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["", "path", "speakerId", "transcription", "action", 'object', "location"])
        self.counter = 0

    def append_line(self, path, speaker_id, transcription, action, obj):
        line = [str(self.counter), path, speaker_id, transcription, action, obj, "none"]
        self.counter += 1
        self.writer.writerow(line)

    def save(self):
        self.file.close()
