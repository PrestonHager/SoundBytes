//
//  PostPlayingOverlay.swift
//  Sound Bytes
//
//  Created by Preston Hager on 9/1/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct PostPlayingOverlay: View {
    @Binding var soundbite: SoundBite
    
    var body: some View {
        // We must wrap the conditional views in a constant view (HStack) or the compile whines
        HStack {
            if self.soundbite.playing {
                // if there's something playing
                HStack(spacing: 30) {
                    Button(action: {}) {
                        Image(systemName: "gobackward.30")
                            .imageScale(.large)
                    }.padding()
                    Button(action: {
                        self.soundbite.playing = false
                    }) {
                        Image(systemName: "pause.fill")
                            .imageScale(.large)
                    }.padding()
                    Button(action: {}) {
                        Image(systemName: "goforward.30")
                            .imageScale(.large)
                    }.padding()
                }
                // Make the button colors the primary color instead of blue.
                .foregroundColor(.primary)
            } else {
                // if there's nothing playing
                Text("")
            }
        }
    }
}

struct PostPlayingOverlay_Previews: PreviewProvider {
    @State static var debugSoundBite: SoundBite = SoundBite(playing: true, title: "Post", text: "Post text goes here.", createdAt: Date())
    
    static var previews: some View {
        PostPlayingOverlay(soundbite: $debugSoundBite)
    }
}
