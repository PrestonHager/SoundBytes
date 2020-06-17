//
//  LoginView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/6/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct LoginContentView: View {
    var window: UIWindow?
    
    var body: some View {
        NavigationView {
            VStack {
                Text("Welcome to Sound Bytes!\nAre you new or do you already have an account?")
                    .font(.system(size: 24))
                    .multilineTextAlignment(.center)
                    .padding()
                NavigationLink(destination: SignupView()) {
                    Text("Signup")
                    .font(.system(size: 18))
                    .padding()
                }
                NavigationLink(destination: LoginView(window: window!)) {
                    Text("Login")
                    .font(.system(size: 18))
                    .padding()
                }
            }
            .navigationBarTitle(Text("Sound Bytes"))
            // TODO: add a background for the splash page.
        }
    }
}

struct LoginContentView_Previews: PreviewProvider {
    static var previews: some View {
        LoginContentView(window: UIWindow())
    }
}
