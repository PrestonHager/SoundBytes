//
//  Post.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/26/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct Post: View {
    @State var soundbite: SoundBite
    
    var body: some View {
        // each post is a profile picture with a title and body
        // clicking on the post will activate a button
        // TODO: and play the audio associated with the post
        HStack {
            // Profile Picture
            // TODO: replace image to be dynamic
            Image("preston")
                .resizable()
                .frame(width: 64, height: 64)
                .mask(Circle())
                .overlay(Circle()
                    .stroke(Color.primary, lineWidth: 1.0)
                    .colorInvert())
                .shadow(color: .primary, radius: 1.0, x: 0.0, y: 0.0)
                .padding(.trailing, 15)
            // The button wraps just the text, but seems to actually fill the entire post including picture
            Button(action: {
                if (!self.soundbite.playing) {
                    self.soundbite.playing = true
                }
            }) {
                // The actual text which is taken from the soundbite
                VStack(alignment: .leading) {
                    Text(soundbite.title)
                        .font(.title)
                        .padding(.bottom, .zero)
                    Text(soundbite.text)
                }
            }
            // And change the frame to fill the full width, and opacity and overlay if it's playing
            .frame(minWidth: 0, maxWidth: .infinity, alignment: .topLeading)
            // Change the opacity and overlay if it's currently playing.
            .opacity(soundbite.playing ? 0.3 : 1)
            .overlay(PostPlayingOverlay(soundbite: $soundbite))
            // This foregroundColor overrides the default button's blue color.
            .foregroundColor(.primary)
        }
    }
}

#if DEBUG
struct Post_Previews: PreviewProvider {    
    static var previews: some View {
        Post(soundbite: SoundBite(title: "Post", text: "Post text goes here.", time: Date()))
    }
}
#endif
