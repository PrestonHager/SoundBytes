//
//  SwipeMainView.swift
//  Sound Bytes
//
//  Created by Preston Hager on 5/27/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import SwiftUI

struct CustomTabView<Content>: View where Content: View {
    private var tabSize: CGFloat = UIScreen.main.bounds.width
    @State private var currentIndex: Int
    @State private var lastOffset: CGFloat!
    @State private var offset: CGFloat!
    private var initialOffset: CGFloat

    var totalTabs: Int
    var content: Content

    init(totalTabs: Int, initialIndex: Int, @ViewBuilder content: @escaping () -> Content) {
        self.content = content()
        self.totalTabs = totalTabs
        self._currentIndex = State(initialValue: (initialIndex-1))
        self.initialOffset = tabSize*(CGFloat(totalTabs)-1)/2
        self._offset = State(initialValue: calculateOffset())
        self._lastOffset = State(initialValue: calculateOffset())
    }

    func calculateOffset() -> CGFloat {
        return (-self.tabSize * CGFloat(self.currentIndex)) + self.initialOffset
    }
    
    var body: some View {
        HStack(spacing: 0) {
            self.content
        }
        .offset(x: self.offset)
        .contentShape(Rectangle())
        .highPriorityGesture(DragGesture()
            .onChanged { gesture in
                self.offset = self.lastOffset + gesture.translation.width
            }
            .onEnded { value in
                if value.translation.width > 50 {
                    self.changeTab(direction: .left)
                } else if value.translation.width < 50 {
                    self.changeTab(direction: .right)
                } else {
                    self.offset = self.calculateOffset()
                }
            })
        .animation(.default)
    }
    
    func changeTab(direction: Direction) {
        // Increase/decrease the current index.
        switch direction {
            case .left:
                self.currentIndex -= 1
                break
        case .right:
            self.currentIndex += 1
            break
        }
    
        // Correct the index in case it's too big/little.
        if (self.currentIndex < 0) {
            self.currentIndex = 0
        }
        if (self.currentIndex >= self.totalTabs) {
            self.currentIndex = self.totalTabs - 1
        }
        
        // Finially, calculate the offsets.
        self.offset = calculateOffset()
        self.lastOffset = calculateOffset()
    }
}

enum Direction {
    case left
    case right
}

extension View {
    func customTab() -> some View {
        self.frame(minWidth: UIScreen.main.bounds.width, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity, alignment: .center)
    }
}

struct CustomTabView_Previews: PreviewProvider {
    static var previews: some View {
        CustomTabView(totalTabs: 4, initialIndex: 1) {
            Text("The content of the first tab item.")
                .customTab()
            Text("The content of the second tab item.")
                .customTab()
            Text("Third View Content!")
                .customTab()
            Text("Fourth")
                .customTab()
        }
    }
}
