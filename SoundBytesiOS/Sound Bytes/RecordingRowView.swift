//
//  RecordingRowView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/3/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct RecordingRowView: View {
    var audioController: AudioController
    @Binding var recording: Recording
    
    var clearAllRecordings: () -> Void
    
    @State var showRenaming = false
    
    init(audioController: AudioController, recording: Binding<Recording>, clearAllRecordings: @escaping () -> Void) {
        self.audioController = audioController
        self._recording = recording
        self.clearAllRecordings = clearAllRecordings
        NotificationCenter.default.addObserver(forName: Notification.Name("audioPlayerDidFinishPlayingSuccessfully"), object: nil, queue: nil, using: audioPlayerFinished(notification:))
    }
    
    var body: some View {
        HStack {
            if (!showRenaming) {
                Text(recording.name)
                    .foregroundColor(.primary)
                Spacer()
                Image(systemName: recording.playing ? "square.fill" : "play.fill")
                    .imageScale(.large)
                    .padding()
                    .foregroundColor(.primary)
                    // We add the tap gesture here so we can make a simultaneous long press gesture.
                    .onTapGesture {
                        if (self.recording.playing) {
                            self.audioController.stop()
                            self.recording.playing = false
                        } else {
                            self.clearAllRecordings()
                            self.recording.playing = self.audioController.play(recording: self.recording)
                        }
                    }
            } else {
                TextField("Enter a title.", text: $recording.name)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .autocapitalization(.words)
                    .environment(\.isEnabled, true)
                Image(systemName: "checkmark")
                    .imageScale(.large)
                    .padding()
                    .foregroundColor(.primary)
                    .onTapGesture {
                        self.showRenaming = false
                    }
            }
        }
        .simultaneousGesture(LongPressGesture()
            .onEnded({ _ in
                self.showRenaming = true
            })
        )
    }
    
    func audioPlayerFinished(notification: Notification) {
        recording.playing = false
        // TODO: is this the only way to update the view?
        audioController.objectWillChange.send(audioController)
    }
}

struct RecordingRowView_Previews: PreviewProvider {
    @State static var debugRecording = Recording(name: "Test Recording", fileURL: URL(fileURLWithPath: "file.m4a"), createdAt: Date())

    static var previews: some View {
        RecordingRowView(audioController: AudioController(), recording: $debugRecording, clearAllRecordings: debugClearAllRecordings)
    }
    
    static func debugClearAllRecordings() {
        
    }
}
