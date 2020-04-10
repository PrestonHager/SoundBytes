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
    
    var body: some View {
        Text("Login")
    }
    
    func loginAction() {
        let url = ProcessInfo.processInfo.environment["LAMDA_ENDPOINT"]! + "create-account"
        let json = [
            "username": "TestUser",
            "passowrd": "Password#1",
            "email": "email@example.com"
        ]
        let data = try! JSONSerialization.data(withJSONObject: json, options: [])
        networkManager.post(url: url, data: data)
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
    }
}
