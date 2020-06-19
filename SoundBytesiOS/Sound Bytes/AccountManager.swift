//
//  AccountManager.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/9/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation

class AccountManager: ObservableObject {
    var networkManager: NetworkManager
    let defaults = UserDefaults.standard
    
    init(_ networkManager: NetworkManager) {
        self.networkManager = networkManager
    }
    
    @Published var userAvailable = false {
        willSet {
            self.objectWillChange.send()
        }
    }
    
    @Published var requestError: String? = nil {
        willSet {
            self.objectWillChange.send()
        }
    }

    func checkCurrent() -> Bool {
        let currentUser = self.defaults.string(forKey: "CurrentUser")
        if (currentUser == nil) {
            return false
        }
        return check(currentUser ?? "")
    }
    
    func checkAll() {
        let users = self.defaults.stringArray(forKey: "AllUsers") ?? []
        for user in users {
            if (!check(user)) {
                self.removeUser(user)
            }
        }
        if (users.isEmpty) {
            self.userAvailable = false
        } else {
            // All our tests passed, and it must be saved credentials.
            self.userAvailable = true
        }
    }
    
    func check(_ username: String) -> Bool {
        let accessToken = self.defaults.string(forKey: "\(username)AccessToken")
        if (accessToken == nil) {
            return false
        } else {
            let expirationTime = self.defaults.integer(forKey: "\(username)TokenExpirationTime")
            let currentTime = Date().toSeconds()
            if (expirationTime < currentTime) {
                // Is expired and we must refresh.
                return self.refresh()
            }
        }
        return true
    }
    
    func refresh() -> Bool {
        return false
    }
    
    func logoutAll() {
        let users = self.defaults.stringArray(forKey: "AllUsers") ?? []
        for user in users {
            self.logout(user)
        }
    }
    
    func logoutCurrent() {
        let currentUser = self.defaults.string(forKey: "CurrentUser") ?? ""
        self.logout(currentUser)
    }
    
    func logout(_ username: String) {
        print(username)
        self.defaults.set(nil, forKey: "\(username)AccessToken")
        self.defaults.set(nil, forKey: "\(username)RefreshToken")
        self.defaults.set(nil, forKey: "\(username)TokenIssueTime")
        self.defaults.set(nil, forKey: "\(username)TokenExpirationTime")
        self.removeUser(username)
        self.userAvailable = false
        print(self.defaults.stringArray(forKey: "AllUsers") as Any)
    }

    func login(_ username: String, _ password: String) {
        guard var url = ProcessInfo.processInfo.environment["LAMBDA_ENDPOINT"] else {
            return
        }
        url += "/dev/auth"
        let json = [
            "username": username,
            "password": password
        ]
        let data = try! JSONSerialization.data(withJSONObject: json, options: [])
        networkManager.post(url: url, data: data, onCompletion: {response in
            print(response)
            // TODO: move this to the keychain or something more secure.
            self.defaults.set(response.accessToken, forKey: "\(username)AccessToken")
            self.defaults.set(response.refreshToken, forKey: "\(username)RefreshToken")
            self.defaults.set(response.issuedAt, forKey: "\(username)TokenIssueTime")
            self.defaults.set(response.expiresAt, forKey: "\(username)TokenExpirationTime")
            self.addUser(username)
        }, onError: { response in
            self.requestError = response.error
            self.userAvailable = false
        }, onDecodingError: { data in
            self.requestError = "Decoding error.\n" + String(decoding: data, as: UTF8.self)
            self.userAvailable = false
        })
    }
    
    func signup(_ email: String, _ username: String, _ password: String) {
        
    }
    
    private func addUser(_ username: String) {
        self.defaults.set(username, forKey: "CurrentUser")
        var users = self.defaults.stringArray(forKey: "AllUsers") ?? []
        users.append(username)
        print(users)
        self.defaults.set(users, forKey: "AllUsers")
        self.userAvailable = true
    }
    
    private func removeUser(_ username: String) {
        if (self.defaults.string(forKey: "CurrentUser") == username) {
            self.defaults.set(nil, forKey: "CurrentUser")
        }
        let users = (self.defaults.stringArray(forKey: "AllUsers") ?? []).filter { $0 != username }
        self.defaults.set(users, forKey: "AllUsers")
    }
}
