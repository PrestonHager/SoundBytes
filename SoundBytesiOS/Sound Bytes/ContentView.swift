//
//  ContentView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/8/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @State var posts: [SoundBite] = []
    
    var body: some View {
        NavigationView {
            VStack {
                // Posts
                List {
                    ForEach(posts, id: \.self) { post in
                        Post(soundbite: post)
                    }
                }
            }
            .navigationBarTitle(Text("Sound Bytes"))
            .navigationBarItems(leading:
                // add a leading item (usually on the left) for the user's profile
                NavigationLink(destination: ProfileView()) {
                    Image(systemName: "person.fill")
                    .resizable()
                    .frame(width: 24.0, height: 24.0)
                    .foregroundColor(.blue)
                }, trailing:
                // add a trailing item (on the right) for adding a new post
                NavigationLink(destination: NewPostView()) {
                    Image(systemName: "plus")
                        .resizable()
                        .frame(width: 24.0, height: 24.0)
                        // the typical font is too light for my taste so it's made bolder
                        .font(Font.system(.body).bold())
                        // the buttons are made blue fitting with the typical apple style.
                        .foregroundColor(.blue)
                })
        }
    }
    
    func addPost(post: SoundBite) -> ContentView {
        self.posts.append(post)
        return self
    }
}

#if DEBUG
struct ContentView_Previews: PreviewProvider {
    static let debugPosts = [
        SoundBite(title: "Test 1", text: "This is the first test post in a list of posts for soundbytes.", time: Date()),
        SoundBite(playing: true, title: "Test 2", text: "And this is the second post. Click the post to play.", time: Date()),
        SoundBite(title: "My First Post", text: "I'm still just testing.", time: Date())
    ]
    
    static var previews: some View {
        ContentView(posts: debugPosts)
    }
}
#endif
