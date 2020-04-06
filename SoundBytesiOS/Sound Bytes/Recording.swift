//
//  Recording.swift
//  Sound Bytes
//
//  Created by Preston Hager on 1/27/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation

struct Recording: Identifiable, Hashable {
    var id = UUID()
    
    var playing = false
    
    var name: String
    let fileURL: URL
    let createdAt: Date
}
