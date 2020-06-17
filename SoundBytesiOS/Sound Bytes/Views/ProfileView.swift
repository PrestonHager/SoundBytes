//
//  ProfileView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/26/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import SwiftUI

struct ProfileView: View {
    @Environment(\.presentationMode) var presentationMode: Binding<PresentationMode>
    @Environment(\.accountManager) var accountManager: AccountManager
    @Environment(\.audioController) var audioController: AudioController

    var window: UIWindow?
    
    var body: some View {
        VStack {
            Text("Profile View")
            Button(action: {
                self.accountManager.logoutCurrent()
                let contentView = LoginContentView(window: self.window).environmentObject(self.audioController).environmentObject(self.accountManager)
                self.window!.rootViewController = UIHostingController(rootView: contentView)
//                self.presentationMode.wrappedValue.dismiss()
            }) {
                Text("Logout")
                    .padding()
            }
        }
    }
}

#if DEBUG
struct ProfileView_Previews: PreviewProvider {
    static var previews: some View {
        ProfileView()
            .environmentObject(AccountManager(NetworkManager()))
    }
}
#endif
