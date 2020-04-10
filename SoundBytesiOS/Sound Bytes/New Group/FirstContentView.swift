//
//  LoginView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/6/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct FirstContentView: View {
    var body: some View {
        NavigationView {
            VStack {
                Text("Welcome to Sound Bytes!\nAre you new or do you already have an account?")
                    .multilineTextAlignment(.center)
                    .padding()
                NavigationLink(destination: SignupView()) {
                    Text("Signup")
                    .padding()
                }
                NavigationLink(destination: LoginView()) {
                    Text("Login")
                    .padding()
                }
            }
            .navigationBarTitle(Text("Sound Bytes"))
            // TODO: add a background for the splash page.
        }
    }
}

struct FirstContentView_Previews: PreviewProvider {
    static var previews: some View {
        FirstContentView()
    }
}
