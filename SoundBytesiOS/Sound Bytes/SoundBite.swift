//
//  Post.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/26/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import Foundation

struct SoundBite : Hashable, Codable, Identifiable {
    var id = UUID()
    var playing: Bool = false
    var title: String
    var text: String
    // Note: don't have Void in structs, it cuauses memory problems
    // var audio = Void.self
    var time: Date
}
