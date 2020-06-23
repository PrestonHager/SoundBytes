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
                LoginView(window: window!)
                NavigationLink(destination: SignupContentView(window: window!)) {
                    Text("Don't have an account? Sign Up")
                        .foregroundColor(.black)
                        .font(.system(size: 18))
                        .padding()
                }
            }
            .navigationViewStyle(StackNavigationViewStyle())
            .background(LinearGradient(gradient: Gradient(colors: [Color(hex: "#fb4aff"), Color(hex: "#65e8ff")]), startPoint: .top, endPoint: .bottom)
            .edgesIgnoringSafeArea(.all))
//            .navigationBarTitle(Text("Sound Bytes"))
            // TODO: add a background for the splash page.
        }
    }
}

struct LoginContentView_Previews: PreviewProvider {
    static var previews: some View {
        LoginContentView(window: UIWindow())
    }
}
