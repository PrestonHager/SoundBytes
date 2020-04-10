//
//  Post.swift
//  Sound Bytes
//
//  Created by Preston Hager on 8/26/19.
//  Copyright © 2019 Hager Family. All rights reserved.
//

import Foundation

struct SoundBite: Hashable, Codable, Identifiable {
    var id = UUID()
    var playing: Bool = false
    var title: String
    var text: String
//    let fileURL: URL
    let createdAt: Date
}
