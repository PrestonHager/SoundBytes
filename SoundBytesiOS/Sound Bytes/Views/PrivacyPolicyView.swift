//
//  PrivacyPolicyView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 6/1/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct PrivacyPolicyView: View {
    @Environment(\.presentationMode) var presentationMode: Binding<PresentationMode>

    var body: some View {
        NavigationView {
            VStack(alignment: .leading) {
                Text("Here in lies the content of the privacy policy for Sound Bytes.")
            }
            .frame(minWidth: 0, maxWidth: .infinity)
            .navigationBarTitle("Terms and Conditions", displayMode: .inline)
            .navigationBarItems(trailing: Button(action: {
                self.presentationMode.wrappedValue.dismiss()
            }) {
                Text("Done")
            })
        }
    }
}

struct PrivacyPolicyView_Previews: PreviewProvider {
    static var previews: some View {
        PrivacyPolicyView()
    }
}
