//
//  Extensions.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/2/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation

// Date toString formatter extension.
extension Date
{
    func toString( dateFormat format  : String ) -> String
    {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = format
        return dateFormatter.string(from: self)
    }

}
