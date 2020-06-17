//
//  EnvironmentKeys.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/16/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation
import SwiftUI

struct AccountManagerKey: EnvironmentKey {
    static let defaultValue: AccountManager = AccountManager(NetworkManager())
}

struct AudioControllerKey: EnvironmentKey {
    static let defaultValue: AudioController = AudioController()
}

extension EnvironmentValues {
    var accountManager: AccountManager {
        get {
            return self[AccountManagerKey.self]
        }
        set {
            self[AccountManagerKey.self] = newValue
        }
    }
    
    var audioController: AudioController {
        get {
            return self[AudioControllerKey.self]
        }
        set {
            self[AudioControllerKey.self] = newValue
        }
    }
}
