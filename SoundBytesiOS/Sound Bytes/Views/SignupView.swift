//
//  SignupView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/1/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct SignupView: View {
    @Environment(\.accountManager) var accountManager: AccountManager
    @Environment(\.audioController) var audioController: AudioController

    var window: UIWindow?
    
    @State var email: String = ""
    @State var username: String = ""
    @State var password: String = ""
    @State var confirmPassword: String = ""
    @State var agreeToTerms = false
    
    @State var showSheet = false
    @State var activeSheet: ActiveSheet? = nil
    
    @State var showErrorMessage = false
    @State var errorMessage: String = ""
    
    var body: some View {
        VStack {
            Text("Signup")
                .font(.largeTitle)
                .foregroundColor(.white)
            Spacer()
            VStack {
                Button(action: {}) {
                    Text("Continue with Apple")
                        .padding()
                }
                    .modifier(ActionButtonStyle())
            }
            Divider()
                .padding([.horizontal, .bottom])
            VStack(spacing: 15) {
                TextField("Email", text: $email)
                    .modifier(FormTextFieldStyle())
                TextField("Username", text: $username)
                    .modifier(FormTextFieldStyle())
                SecureField("Password", text: $password)
                    .modifier(FormTextFieldStyle())
                SecureField("Confirm Password", text: $confirmPassword)
                    .modifier(FormTextFieldStyle())
            }
                .padding([.leading, .trailing], 30)
            HStack {
                Image(systemName: agreeToTerms ? "checkmark.square.fill" : "square")
                    .imageScale(.large)
                    .onTapGesture {
                        self.agreeToTerms.toggle()
                    }
                    .offset(y: -8)
                VStack {
                    HStack(spacing: 4) {
                        Text("I agree to the")
                        Button(action: {
                            self.showSheet.toggle()
                            self.activeSheet = .termsAndConditions
                        }) {
                            Text("terms and conditions")
                        }
                    }
                    HStack(spacing: 4) {
                        Text("and")
                        Button(action: {
                            self.showSheet.toggle()
                            self.activeSheet = .privacyPolicy
                        }) {
                            Text("privacy policy")
                        }
                    }
                }
                    .foregroundColor(.black)
            }
                .padding(.top)
            Button(action: self.signupAction) {
                Text("Signup")
                    .padding()
            }
                .modifier(ActionButtonStyle())
            Spacer()
        }
        .sheet(isPresented: $showSheet) {
            if self.activeSheet == .termsAndConditions {
                TermsAndConditionsView()
            } else {
                PrivacyPolicyView()
            }
        }
        .alert(isPresented: $showErrorMessage) {
            Alert(title: Text("Error in Signup"), message: Text(errorMessage), dismissButton: .default(Text("Ok")))
        }
    }
    
    func signupAction() {
        // Check that all the fields are valid.
        if (verifyFields()) {
            self.accountManager.signup(self.email, self.username, self.password)
            if (self.accountManager.userAvailable) {
                let contentView = MainContentView(window: self.window).environmentObject(self.audioController).environmentObject(self.accountManager)
                self.window!.rootViewController = UIHostingController(rootView: contentView)
            } else {
                // TODO: Show the signup error.
                self.errorMessage = "An error occured."
                self.showErrorMessage = true
            }
        }
    }
    
    func verifyFields() -> Bool {
        if (self.email.isEmpty) {
            self.errorMessage = "You must provide a valid email address."
            self.showErrorMessage = true
        } else if (self.username.count < 3) {
            self.errorMessage = "Your username must be at least 3 characters long."
            self.showErrorMessage = true
        } else if (self.password != self.confirmPassword) {
            // the passwords don't match
            self.errorMessage = "The passwords you put in do not match."
            self.showErrorMessage = true
        } else if (!self.agreeToTerms) {
            // need to agree to the privacy policy
            self.errorMessage = "You must agree to the terms and conditions and privacy policy to sign up."
            self.showErrorMessage = true
        } else {
            return true
        }
        return false
    }
}

enum ActiveSheet {
    case termsAndConditions, privacyPolicy
}

struct SignupView_Previews: PreviewProvider {
    static var previews: some View {
        SignupContentView(window: UIWindow())
    }
}
