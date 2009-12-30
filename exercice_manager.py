# -*- coding: utf-8 -*-
from xml.dom.minidom import getDOMImplementation, parse


class ExerciceLoader(object):

    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        rc = rc.strip()
        return rc


    def Load(self, path):
        dom = parse(path)
        xml_paths = dom.getElementsByTagName("paths")[0]
        self.videoPath = self.getText(xml_paths.getElementsByTagName("video")[0].childNodes)
        self.exercicePath = self.getText(xml_paths.getElementsByTagName("exercice")[0].childNodes)

        print  self.videoPath
        print  self.exercicePath

        xml_progress = dom.getElementsByTagName("progress")[0]
        self.currentSequence = int(self.getText(xml_progress.getElementsByTagName("current_sequence")[0].childNodes))
        self.currentWord = int(self.getText(xml_progress.getElementsByTagName("current_word")[0].childNodes))

        xml_sequences = xml_progress.getElementsByTagName("sequences")[0]

        self.progress = []

        for xml_sequence in xml_sequences.getElementsByTagName("sequence"):
            id = int(self.getText(xml_sequence.getElementsByTagName("id")[0].childNodes))
            state = self.getText(xml_sequence.getElementsByTagName("state")[0].childNodes)
            words = []

            if state == "in_progress":
                xml_words = xml_sequence.getElementsByTagName("words")[0]
                for xml_world in xml_words.getElementsByTagName("word"):
                    words.append(self.getText(xml_world.childNodes))

            self.progress.append((id, state, words))

        dom.unlink()

        return True


    def UpdateSequenceList(self, sequenceList):

        for (id, state, words) in self.progress:
            sequence = sequenceList[id]
            if state == "done":
                sequence.CompleteAll()
            elif state == "in_progress":
                i = 0
                for word in words:
                    sequence.GetWorkList()[i] = word
                    i = i+1

    def GetCurrentSequence(self):
        return self.currentSequence

    def GetCurrentWord(self):
        return self.currentWord

    def GetVideoPath(self):
        return self.videoPath

    def GetExercicePath(self):
        return self.exercicePath

class ExerciceSaver(object):

    def Save(self):
        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "perroquet", None)
        root_element = newdoc.documentElement

        # Version
        xml_version = newdoc.createElement("version")
        xml_version.appendChild(newdoc.createTextNode("1.0.0"))
        root_element.appendChild(xml_version)

        # Paths
        xml_paths = newdoc.createElement("paths")

        xml_video_paths = newdoc.createElement("video")
        xml_video_paths.appendChild(newdoc.createTextNode(self.videoPath))
        xml_paths.appendChild(xml_video_paths)

        xml_exercice_paths = newdoc.createElement("exercice")
        xml_exercice_paths.appendChild(newdoc.createTextNode(self.exercicePath))
        xml_paths.appendChild(xml_exercice_paths)


        if self.correctionPath != "":
            xml_correction_paths = newdoc.createElement("correction")
            xml_correction_paths.appendChild(newdoc.createTextNode(self.correctionPath))
            xml_paths.appendChild(xml_correction_paths)

        root_element.appendChild(xml_paths)

        # Progress
        xml_progress = newdoc.createElement("progress")

        xml_current_sequence = newdoc.createElement("current_sequence")
        xml_current_sequence.appendChild(newdoc.createTextNode(str(self.sequenceId)))
        xml_progress.appendChild(xml_current_sequence)

        xml_current_word = newdoc.createElement("current_word")
        xml_current_word.appendChild(newdoc.createTextNode(str(self.sequenceList[self.sequenceId].GetActiveWordIndex())))
        xml_progress.appendChild(xml_current_word)

        xml_sequences = newdoc.createElement("sequences")
        id = 0
        for sequence in self.sequenceList:
            if sequence.IsValid():
                xml_sequence = newdoc.createElement("sequence")
                xml_sequence_id = newdoc.createElement("id")
                xml_sequence_id.appendChild(newdoc.createTextNode(str(id)))
                xml_sequence.appendChild(xml_sequence_id)
                xml_sequence_state = newdoc.createElement("state")
                xml_sequence_state.appendChild(newdoc.createTextNode("done"))
                xml_sequence.appendChild(xml_sequence_state)

                xml_sequences.appendChild(xml_sequence)
            elif not sequence.IsEmpty():
                xml_sequence = newdoc.createElement("sequence")
                xml_sequence_id = newdoc.createElement("id")
                xml_sequence_id.appendChild(newdoc.createTextNode(str(id)))
                xml_sequence.appendChild(xml_sequence_id)
                xml_sequence_state = newdoc.createElement("state")
                xml_sequence_state.appendChild(newdoc.createTextNode("in_progress"))
                xml_sequence.appendChild(xml_sequence_state)

                xml_sequence_words = newdoc.createElement("words")

                for word in sequence.GetWorkList():
                    xml_sequence_word = newdoc.createElement("word")
                    xml_sequence_word.appendChild(newdoc.createTextNode(word))
                    xml_sequence_words.appendChild(xml_sequence_word)

                xml_sequence.appendChild(xml_sequence_words)

                xml_sequences.appendChild(xml_sequence)

            id = id +1
        xml_progress.appendChild(xml_sequences)

        root_element.appendChild(xml_progress)


        xml_string = newdoc.toprettyxml()

        f = open(self.outputPath, 'w')
        f.write(xml_string)
        f.close()

    def SetPath(self, path):
        self.outputPath = path

    def SetVideoPath(self, path):
        self.videoPath = path

    def SetExercicePath(self, path):
        self.exercicePath = path

    def SetCorrectionPath(self, path):
        self.correctionPath = path

    def SetCurrentSequence(self, id):
        self.sequenceId = id

    def SetSequenceList(self, sequenceList):
        self.sequenceList = sequenceList