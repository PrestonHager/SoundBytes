//
//  Modifiers.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/20/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation
import SwiftUI

struct FormTextFieldStyle: ViewModifier {
    func body(content: Content) -> some View {
        return content
            .padding(8)
            .foregroundColor(.black)
            .background(Color(hex: "#ddd"))
            .cornerRadius(5.0)
            .shadow(radius: 5)
    }
}

struct ActionButtonStyle: ViewModifier {
    func body(content: Content) -> some View {
        return content
            .frame(minWidth: 0, maxWidth: .infinity)
            .font(.headline)
            .foregroundColor(.white)
            .background(Color(hex: "#fb3cf0"))
            .cornerRadius(15.0)
            .shadow(radius: 5)
            .padding(.horizontal, 60)
            .padding(.vertical, 15)
    }
}
