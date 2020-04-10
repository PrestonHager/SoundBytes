//
//  ResponseData.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/9/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation

struct ResponseData: Codable {
    let code: Int
    let error: String!
    
    let accessToken: String!
    let refreshToken: String!
    let issuedAt: Int!
    let expiresAt: Int!
    
    private enum CodingKeys: String, CodingKey {
        case code = "cod"
        case error = "err"
        
        case accessToken = "tkn"
        case refreshToken = "rt"
        case issuedAt = "iat"
        case expiresAt = "exp"
    }
}
