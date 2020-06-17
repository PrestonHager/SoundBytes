//
//  MainView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 5/27/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct MainView: View {
    @Binding var posts: [SoundBite]
    
    var body: some View {
        VStack {
            List {
                ForEach(posts, id: \.self) { post in
                    Post(soundbite: post)
                }
            }
        }
    }
}

struct MainView_Previews: PreviewProvider {
    @State static var debugPosts = [
        SoundBite(title: "Test 1", text: "This is the first test post in a list of posts for soundbytes.", createdAt: Date()),
        SoundBite(playing: true, title: "Test 2", text: "And this is the second post. Click the post to play.", createdAt: Date()),
        SoundBite(title: "My First Post", text: "I'm still just testing.", createdAt: Date())
    ]

    static var previews: some View {
        MainView(posts: $debugPosts)
    }
}
