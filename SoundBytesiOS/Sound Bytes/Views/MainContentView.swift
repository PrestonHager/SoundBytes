//
//  ContentView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/8/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct MainContentView: View {
    @State var posts: [SoundBite] = []
    @State private var selectedPost = 0
    @State private var currentTab = 1
    
    var window: UIWindow?

    var body: some View {
        CustomTabView(totalTabs: 3, initialIndex: 2) {
            ProfileView(window: self.window)
                .customTab()
            MainView(posts: self.$posts)
                .customTab()
            NewPostView(posts: self.$posts)
                .customTab()
        }
    }
    
    func addPost(post: SoundBite) -> MainContentView {
        self.posts.append(post)
        return self
    }
}

#if DEBUG
struct MainContentView_Previews: PreviewProvider {
    static let debugPosts = [
        SoundBite(title: "Test 1", text: "This is the first test post in a list of posts for soundbytes.", createdAt: Date()),
        SoundBite(playing: true, title: "Test 2", text: "And this is the second post. Click the post to play.", createdAt: Date()),
        SoundBite(title: "My First Post", text: "I'm still just testing.", createdAt: Date())
    ]
    
    static var previews: some View {
        MainContentView(posts: debugPosts).environmentObject(AudioController()).environmentObject(AccountManager(NetworkManager()))
    }
}
#endif
