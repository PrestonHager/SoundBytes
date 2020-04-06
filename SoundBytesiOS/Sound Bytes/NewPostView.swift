//
//  NewPostView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/26/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct NewPostView: View {
    // A binding to the array of SoundBites.
    var posts: Binding<[SoundBite]>
    // The audio recorder and player is an observed object.
    @ObservedObject var audioController: AudioController
    
    @State var showRecordingFail = false
    
    var body: some View {
        NavigationView {
            VStack {
                List {
                    ForEach(audioController.recordings.indices, id: \.self) { index in
                        RecordingRowView(audioController: self.audioController, recording: Binding(
                            get: { return self.audioController.recordings[index] },
                            set: { newValue in return self.audioController.recordings[index] = newValue }
                        ), clearAllRecordings: self.clearAllRecordings)
                    }
                    .onDelete(perform: self.deleteRecording)
                }
                // Record and Stop Button
                Button(action: {
                    if (self.audioController.recording) {
                        self.audioController.stop()
                    } else {
                        if (self.audioController.playing) {
                            self.audioController.stop()
                        }
                        self.clearAllRecordings()
                        self.showRecordingFail = !self.audioController.record()
                    }
                }) {
                    Image(systemName: self.audioController.recording ? "square.fill" : "mic.fill")
                        .imageScale(.large)
                        .padding()
                        .foregroundColor(audioController.recording ? .red : .primary)
                }
                .padding()
            }
            .navigationBarTitle(Text("Drafts"))
            .alert(isPresented: $showRecordingFail) {
                Alert(title: Text("Recording Failed"), message: Text("Sound Bytes failed to record. Maybe the microphone permission isn't turned on."), dismissButton: .default(Text("OK")))
            }
        }
    }
    
    func clearAllRecordings() {
        // This is kinda hacky, maybe there's a better solution?
        var newRecordings = [Recording]()
        for recording in audioController.recordings {
            var recording = recording
            recording.playing = false
            newRecordings.append(recording)
        }
        audioController.recordings = newRecordings
        audioController.objectWillChange.send(audioController)
    }
    
    private func deleteRecording(at offsets: IndexSet) {
        // Delete each file first.
        for index in Array(offsets) {
            audioController.deleteRecording(fileURL: audioController.recordings[index].fileURL)
        }
        // Ensure no audio is playing then we can delete the recording.
        audioController.stop()
        audioController.recordings.remove(atOffsets: offsets)
        // Update the view by sending an objectWillChange signal.
        audioController.objectWillChange.send(audioController)
    }
}

#if DEBUG
struct NewPostView_Previews: PreviewProvider {
    @State static var debugPosts: [SoundBite] = []
    
    static var previews: some View {
        NewPostView(posts: $debugPosts, audioController: AudioController())
    }
}
#endif
