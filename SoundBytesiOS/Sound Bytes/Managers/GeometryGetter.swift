//
//  GeometryGetter.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/21/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

// Technically this was taken from this Stack Overflow post:
// https://stackoverflow.com/questions/56491881/move-textfield-up-when-the-keyboard-has-appeared-in-swiftui
// To that end, thank you kontiki for making such wonderful SwiftUI code!

import Foundation
import SwiftUI

struct GeometryGetter: View {
    @Binding var rect: CGRect

    var body: some View {
        GeometryReader { geometry in
            Group { () -> AnyView in
                DispatchQueue.main.async {
                    self.rect = geometry.frame(in: .global)
                }

                return AnyView(Color.clear)
            }
        }
    }
}
