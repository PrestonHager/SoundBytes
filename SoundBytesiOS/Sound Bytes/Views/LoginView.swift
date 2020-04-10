//
//  LoginView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/6/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct LoginView: View {
    let networkManager = NetworkManager()
    
    @State var username: String = "TestUser"
    @State var password: String = "Password#1"
    
    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            TextField("Password", text: $password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            Button(action: loginAction) {
                Text("Login")
                    .padding()
            }
        }
    }
    
    func loginAction() {
        let url = ProcessInfo.processInfo.environment["LAMBDA_ENDPOINT"]! + "auth"
        let json = [
            "username": username,
            "password": password
        ]
        let data = try! JSONSerialization.data(withJSONObject: json, options: [])
        networkManager.post(url: url, data: data) {response in
            if (response.error != nil) {
                print("Error: " + response.error)
            } else {
                print(response)
                // TODO: move this to the keychain or something more secure.
                let defaults = UserDefaults.standard
                defaults.set(response.accessToken, forKey: "AccessToken")
                defaults.set(response.refreshToken, forKey: "RefreshToken")
                defaults.set(response.issuedAt, forKey: "TokenIssueTime")
                defaults.set(response.expiresAt, forKey: "TokenExpirationTime")
            }
        }
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
    }
}
