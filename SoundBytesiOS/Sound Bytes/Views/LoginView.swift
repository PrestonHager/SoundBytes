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

    @ObservedObject private var kGuardian = KeyboardGuardian(textFieldCount: 2)
    
    @State var username: String = "TestUser"
    @State var password: String = "Password#1"
    
    @State var disabled: Bool = false
    
    @State var showLoginError = false
    @State var loginErrorMessage: String! = nil
    
    private var loginSink: AnyCancellable? = nil
    private var loginErrorSink: AnyCancellable? = nil
    
    init(window: UIWindow? = nil) {
        self.window = window
        self.loginSink = accountManager.$userAvailable.sink(receiveValue: self.loginCallback)
        self.loginErrorSink = accountManager.$requestError.sink(receiveValue: self.loginErrorCallback)
    }
    
    var body: some View {
        VStack {
            Text("Sound Bytes")
                .foregroundColor(.white)
                .font(.largeTitle)
                .shadow(radius: 10)
            Image("soundbytesicon")
                .resizable()
                .frame(width: 256.0, height: 256.0)
                .clipShape(Circle())
                .shadow(radius: 10)
                .overlay(Circle().stroke(Color(hex: "#fb3cf0"), lineWidth: 3))
                .padding()
            Spacer()
            VStack(spacing: 15) {
                TextField("Username", text: $username)
                    .modifier(FormTextFieldStyle())
                    .background(GeometryGetter(rect: $kGuardian.rects[0]))
                SecureField("Password", text: $password)
                    .modifier(FormTextFieldStyle())
                    .background(GeometryGetter(rect: $kGuardian.rects[0]))
            }
                .padding([.leading, .trailing], 30)
            HStack {
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
                    .modifier(ActionButtonStyle())
            }
            Spacer()
        }
        .offset(y: kGuardian.slide).animation(.easeInOut(duration: 1.0))
        .alert(isPresented: $showLoginError) {
            Alert(title: Text("Login Error"), message: Text(self.loginErrorMessage ?? "No error to show."), dismissButton: .default(Text("Ok")))
        }
        .onAppear { self.kGuardian.addObserver() }
        .onDisappear { self.kGuardian.removeObserver() }
    }
    
    func loginCallback(value: Bool) {
        print("Callback accessed with the value of \(value)")
        if (value) {
            DispatchQueue.main.async {
                let contentView = MainContentView(window: self.window)
                self.window!.rootViewController = UIHostingController(rootView: contentView)
            }
        } else {
            DispatchQueue.main.async {
                self.disabled = false
                // TODO: show error for failure to log in.
                self.loginErrorMessage = self.accountManager.requestError
                self.showLoginError = true
            }
        }
        print("Currently disabled: \(self.disabled)")
    }
    
    func loginErrorCallback(value: String?) {
        print("Error callback accessed with value of \(value ?? "nil")")
        if (value != nil) {
            DispatchQueue.main.async {
                self.loginErrorMessage = self.accountManager.requestError
                self.showLoginError = true
                print(self.showLoginError)
                print(self.loginErrorMessage ?? "nil")
            }
        }
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginContentView(window: UIWindow())
    }
}
