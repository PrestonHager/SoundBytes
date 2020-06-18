//
//  LoginView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/6/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import UIKit
import SwiftUI
import Combine

struct LoginView: View {
    @Environment(\.accountManager) var accountManager: AccountManager
    @Environment(\.audioController) var audioController: AudioController
    var window: UIWindow?

    @State var username: String = "TestUser"
    @State var password: String = "Password#1"
    
    @State var disabled: Bool = false
    
    private var loginSink: AnyCancellable? = nil
    
    init(window: UIWindow? = nil) {
        self.window = window
        self.loginSink = accountManager.$userAvailable.sink(receiveValue: self.loginCallback)
    }
    
    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal)
            TextField("Password", text: $password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding(.horizontal)
            Button(action: {
                if (!self.disabled) {
                    // disable the buttons and text boxes temporarily.
                    self.disabled = true
                    self.accountManager.login(self.username, self.password)
                }
            }) {
                Text("Login")
                    .padding()
            }
        }
        .navigationBarTitle("Login")
    }
    
    func loginCallback(value: Bool) {
        print("Callback accessed with the value of \(value)")
        if (value) {
            DispatchQueue.main.async {
                let contentView = MainContentView(window: self.window)
                self.window!.rootViewController = UIHostingController(rootView: contentView)
            }
        } else {
            self.disabled = false
            // TODO: show error for failure to log in.
        }
        print("Currently disabled: \(self.disabled)")
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView().environment(\.accountManager, AccountManager(NetworkManager())).environment(\.audioController, AudioController())
    }
}
