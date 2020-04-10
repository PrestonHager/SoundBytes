//
//  NewPostDraftView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/5/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct NewPostDraftView: View {
    @Environment(\.presentationMode) var presentationMode: Binding<PresentationMode>
    @Binding var recording: Recording
    
    var body: some View {
        VStack {
            Spacer()
            Text(recording.name)
            Spacer()
            Button(action: {
                // Post the recording and return to the ContentView page.
                self.presentationMode.wrappedValue.dismiss()
                self.presentationMode.wrappedValue.dismiss()
            }) {
                Text("Post")
                .font(.title)
                .padding()
            }
        }
        .navigationBarTitle(Text("Edit Post"))
    }
}

struct NewPostDraftView_Previews: PreviewProvider {
    @State static var debugRecording = Recording(name: "Test Recording", fileURL: URL(fileURLWithPath: "file.m4a"), createdAt: Date())
    
    static var previews: some View {
        NewPostDraftView(recording: $debugRecording)
    }
}
