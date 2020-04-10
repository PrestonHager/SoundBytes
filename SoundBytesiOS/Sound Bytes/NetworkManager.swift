//
//  NetworkManager.swift
//  Sound Bytes
//
//  Created by Preston Hager on 4/6/20.
//  Copyright © 2020 Hager Family. All rights reserved.
//

import Foundation

class NetworkManager {
    let session = URLSession.shared

    func get(url: String) {
        let url = URL(string: url)!
        
        let task = session.dataTask(with: url) { data, response, error in
            if (self.validate(data: data, response: response, error: error)) {
                // Do something
            }
        }
        
        task.resume()
    }
    
    func post(url: String, data: Data, _ completion: @escaping (ResponseData) -> Void) {
        // Make JSON into a Data object by doing:
        // try! JSONSerialization.data(withJSONObject: data, options: [])
        let url = URL(string: url)!
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = session.uploadTask(with: request, from: data) { data, response, error in
            if (self.validate(data: data, response: response, error: error)) {
                let json = try! JSONDecoder().decode(ResponseData.self, from: data!)
                // Do something
                completion(json)
            }
        }
        
        task.resume()
    }
    
    func validate(data: Data?, response: URLResponse?, error: Error?) -> Bool {
        guard let response = response as? HTTPURLResponse else {
            return false
        }
        if (400...499).contains(response.statusCode) {
            print("Client error!")
            print(try! JSONSerialization.jsonObject(with: data!, options: []))
            return false
        }
        if (500...599).contains(response.statusCode) {
            print("Server error!")
            print(try! JSONSerialization.jsonObject(with: data!, options: []))
            return false
        }
        guard let mime = response.mimeType, mime == "application/json" else {
            print("Wrong MIME type!")
            return false
        }
        do {
            let json = try JSONSerialization.jsonObject(with: data!, options: [])
            print(json)
        } catch {
            print("JSON error: \(error.localizedDescription)")
            return false
        }
        return true
    }
}
