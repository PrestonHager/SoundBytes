//
//  SignupContentView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/20/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct SignupContentView: View {
    var window: UIWindow?
    
    var body: some View {
        VStack {
            SignupView(window: window!)
        }
        .background(LinearGradient(gradient: Gradient(colors: [Color(hex: "#fb4aff"), Color(hex: "#65e8ff")]), startPoint: .top, endPoint: .bottom)
        .edgesIgnoringSafeArea(.all))
    }
}

struct SignupContentView_Previews: PreviewProvider {
    static var previews: some View {
        SignupContentView(window: UIWindow())
    }
}
